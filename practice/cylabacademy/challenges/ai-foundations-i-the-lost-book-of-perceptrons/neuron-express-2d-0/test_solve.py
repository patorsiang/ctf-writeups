"""Tests for Neuron Express 2D-0.

Two properties matter, and they are different things:

  correctness - the recovered parameters must agree with the hidden perceptron
                on ALL 441 grid points, because that is what the server checks,
                not merely on the handful of points we probed;
  budget      - we must reach that state inside 128 probes.

Parameter equality is deliberately NOT asserted: many (w1, w2, b) triples
describe the same boundary and the server accepts any of them.
"""

from __future__ import annotations

import random

import pytest

from solve import (
    MAX_PROBES,
    SERVER_BUDGET,
    VersionSpace,
    active_solve,
    grid,
    parse_bit,
    predict,
    solve_weights,
    verify,
)


POINTS = grid()


def labels_for(params):
    return {p: predict(params, *p) for p in POINTS}


def oracle_for(params, counter=None):
    def oracle(x, y):
        if counter is not None:
            counter.append((x, y))
        return predict(params, x, y)

    return oracle


# --- active probing: the property that actually wins the challenge ----------


@pytest.mark.parametrize(
    "truth",
    [
        (1, 0, -2),
        (1, 1, 0),
        (3, -2, 5),
        (-1, 4, -7),
        (0, 1, 3),
        (2, 3, -1),
        (7, 5, 33),
        (5, -5, 12),
        (0, 0, 1),
        (0, 0, -1),
    ],
)
def test_active_solve_generalises_beyond_the_points_it_probed(truth):
    calls: list = []
    found, observations = active_solve(oracle_for(truth, calls), verbose=False)
    assert verify(found, labels_for(truth)) == [], "wrong on unprobed grid points"
    assert len(observations) < len(POINTS), "should not need the whole grid"
    assert len(calls) == len(observations), "no point probed twice"


@pytest.mark.parametrize(
    "truth", [(1, 1, 0), (0, 1, 3), (7, 5, 33), (13, -8, 41), (1, 0, -2)]
)
def test_stays_inside_the_server_probe_budget(truth):
    _, observations = active_solve(oracle_for(truth), verbose=False)
    assert len(observations) <= MAX_PROBES < SERVER_BUDGET


def test_random_perceptrons_are_all_recoverable_within_budget():
    rng = random.Random(0xC0FFEE)
    worst = 0
    for _ in range(25):
        truth = (rng.randint(-8, 8), rng.randint(-8, 8), rng.randint(-40, 40))
        found, observations = active_solve(oracle_for(truth), verbose=False)
        assert verify(found, labels_for(truth)) == [], truth
        worst = max(worst, len(observations))
    assert worst < SERVER_BUDGET, f"worst case {worst} exceeds budget"


def test_a_non_separable_oracle_never_yields_a_self_contradicting_fit():
    """The correctness guarantee is conditional, and this pins the condition.

    Unanimity among survivors proves correctness only because a genuine
    perceptron is itself always a survivor. Against an oracle that is not
    linearly separable there is no such anchor, so the solver may settle on a
    fit that is wrong off-sample. What it must never do is return a fit that
    contradicts an answer it was actually given.
    """
    def liar(x, y):
        return 1 if (x + y) % 2 == 0 else 0  # parity: not linearly separable

    try:
        found, observations = active_solve(liar, verbose=False)
    except RuntimeError:
        return  # ran out of hypotheses, also an acceptable outcome
    assert verify(found, observations) == []


def test_contradictory_observations_leave_no_survivors():
    """b >= 0 at the origin, quiet either side on x: no line can do that."""
    space = VersionSpace()
    for point, bit in [((0, 0), 1), ((1, 0), 0), ((-1, 0), 0)]:
        space.observe(point, bit)
    assert space.survivors() == []


# --- version space mechanics ------------------------------------------------


def test_probing_never_grows_the_hypothesis_set():
    space = VersionSpace()
    truth = (3, -2, 5)
    previous = len(space.survivors())
    for point in [(-10, -10), (10, 10), (4, 0), (0, 4), (2, 2)]:
        space.observe(point, predict(truth, *point))
        current = len(space.survivors())
        assert current <= previous
        previous = current


def test_settled_is_false_while_survivors_still_disagree():
    space = VersionSpace()
    space.observe((10, 10), 1)
    assert not space.settled(space.label_vectors(space.survivors()))


def test_bias_window_rejects_a_contradictory_direction():
    """A direction that cannot separate the observations must be dropped."""
    space = VersionSpace()
    space.observe((5, 0), 1)
    space.observe((6, 0), 0)  # impossible for any direction with w1 >= 0
    d = space.dirs.index((1, 0))
    assert space.bias_window(d) is None


# --- closed-form fit on already-known labels --------------------------------


@pytest.mark.parametrize(
    "truth", [(1, 0, -2), (1, 1, 0), (3, -2, 5), (0, 1, 3), (0, 0, 1), (0, 0, -1)]
)
def test_solve_weights_reproduces_behaviour(truth):
    labels = labels_for(truth)
    found = solve_weights(labels)
    assert found is not None
    assert verify(found, labels) == []


def test_scaled_parameters_are_simplified():
    """(2,4,6) and (1,2,3) are the same line; return the simple one."""
    assert solve_weights(labels_for((2, 4, 6))) == (1, 2, 3)


def test_solve_weights_rejects_an_empty_observation_set():
    with pytest.raises(ValueError):
        solve_weights({})


def test_verify_catches_a_wrong_candidate():
    assert verify((1, -1, 0), labels_for((1, 1, 0))) != []


# --- protocol parsing -------------------------------------------------------


@pytest.mark.parametrize(
    "response,expected",
    [
        ("The neuron fires! [7/128] (x,y)>", 1),
        ("The neuron stays quiet. [7/128] (x,y)>", 0),
        ("3,4 -> 1\n[7/128] (x,y)>", 1),
        ("3,4 -> 0\n[7/128] (x,y)>", 0),
    ],
)
def test_parse_bit_reads_the_verdict(response, expected):
    assert parse_bit(response) == expected


def test_parse_bit_reports_a_closed_connection_clearly():
    """Budget exhaustion shows up as an empty read; it must not look like noise."""
    with pytest.raises(ConnectionError):
        parse_bit("")


def test_parse_bit_rejects_noise():
    with pytest.raises(ValueError):
        parse_bit("Bounds: [-10, 10]\n(x,y)>")
