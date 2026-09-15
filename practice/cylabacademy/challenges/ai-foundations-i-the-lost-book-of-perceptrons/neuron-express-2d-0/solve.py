#!/usr/bin/env python3
"""Solve CyLab Academy Neuron Express 2D-0.

The service allows only 128 probes but validates a guess against all 441
integer points in [-10, 10]^2, so blind grid probing cannot work. Instead this
narrows the hypothesis space actively: each probe is chosen to split the
surviving candidate perceptrons as evenly as possible, and probing stops as
soon as every survivor agrees on the whole grid, usually after ~20 queries.

That stopping rule is a proof rather than a heuristic, but a conditional one:
a genuine perceptron is always consistent with the answers it gave, so it is
always among the survivors, so unanimity necessarily includes it. The guarantee
rests on the oracle really being a perceptron - against a non-separable oracle
the same rule would happily settle on something unverifiable.

  python3 solve.py --self-test      # prove the solver offline, no network
  python3 solve.py 61967            # probe the live instance and submit
  python3 solve.py 61967 --no-test  # probe only, do not send TEST
"""

from __future__ import annotations

import socket
import sys
from math import gcd


HOST = "aureolin-pixie.cylabacademy.net"
DEFAULT_PORT = 61967
LOW, HIGH = -10, 10
WEIGHT_LIMIT = 20
SERVER_BUDGET = 128
MAX_PROBES = 100  # stay well clear of the server's limit

Point = tuple[int, int]
Params = tuple[int, int, int]


def predict(params: Params, x: int, y: int) -> int:
    """The perceptron rule: w1*x + w2*y + b >= 0 fires, else quiet."""
    w1, w2, b = params
    return 1 if w1 * x + w2 * y + b >= 0 else 0


def grid(low: int = LOW, high: int = HIGH) -> list[Point]:
    return [(x, y) for x in range(low, high + 1) for y in range(low, high + 1)]


def directions(weight_limit: int = WEIGHT_LIMIT) -> list[tuple[int, int]]:
    """Every distinct boundary orientation, one representative each.

    A direction with gcd > 1 is a scaled copy of one already in the list and
    describes the same line, so it is skipped. gcd(0, 0) == 0 keeps the
    degenerate (0, 0) direction, which is what an oracle that always fires (or
    never fires) needs.
    """
    return [
        (w1, w2)
        for w1 in range(-weight_limit, weight_limit + 1)
        for w2 in range(-weight_limit, weight_limit + 1)
        if gcd(abs(w1), abs(w2)) <= 1
    ]


class VersionSpace:
    """The set of perceptrons still consistent with everything observed.

    Parameterised as (direction, bias). For a fixed direction the constraints
    collapse to a closed-form bias window:

        every firing point needs  w1*x + w2*y + b >= 0  ->  b >= -s
        every quiet  point needs  w1*x + w2*y + b <  0  ->  b <= -s - 1

    so a direction survives iff b_lo <= b_hi, and there is no need to search
    over b at all.
    """

    def __init__(self, weight_limit: int = WEIGHT_LIMIT) -> None:
        self.points = grid()
        self.index = {p: i for i, p in enumerate(self.points)}
        self.dirs = directions(weight_limit)
        # Precompute w1*x + w2*y for every direction over the whole grid once.
        self.dots = [
            [w1 * x + w2 * y for x, y in self.points] for w1, w2 in self.dirs
        ]
        # Any bias past this is behaviourally identical to the clamp itself.
        self.bias_limit = weight_limit * max(abs(LOW), abs(HIGH)) * 2 + 1
        self.observations: dict[Point, int] = {}

    def observe(self, point: Point, bit: int) -> None:
        self.observations[point] = bit

    def bias_window(self, d: int) -> tuple[int, int] | None:
        """Feasible [b_lo, b_hi] for direction index d, or None if impossible."""
        dots = self.dots[d]
        b_lo, b_hi = -self.bias_limit, self.bias_limit
        for point, bit in self.observations.items():
            s = dots[self.index[point]]
            if bit == 1:
                b_lo = max(b_lo, -s)
            else:
                b_hi = min(b_hi, -s - 1)
        return None if b_lo > b_hi else (b_lo, b_hi)

    def survivors(self) -> list[Params]:
        """Representatives of the surviving hypotheses.

        Only the two endpoints of each bias window are needed: labels are
        monotone in b (raising b only ever turns a 0 into a 1), so if the
        endpoints agree at a point, every bias between them agrees too.
        """
        out: list[Params] = []
        for d, (w1, w2) in enumerate(self.dirs):
            window = self.bias_window(d)
            if window is None:
                continue
            b_lo, b_hi = window
            out.append((w1, w2, b_lo))
            if b_hi != b_lo:
                out.append((w1, w2, b_hi))
        return out

    def label_vectors(self, survivors: list[Params]) -> list[list[int]]:
        return [[predict(p, x, y) for x, y in self.points] for p in survivors]

    def settled(self, vectors: list[list[int]]) -> bool:
        """True once every survivor predicts the same thing everywhere."""
        return bool(vectors) and all(v == vectors[0] for v in vectors[1:])

    def next_query(self, vectors: list[list[int]]) -> Point | None:
        """The unprobed point whose answer splits the survivors most evenly."""
        total = len(vectors)
        best: Point | None = None
        best_skew: int | None = None
        for i, point in enumerate(self.points):
            if point in self.observations:
                continue
            ones = sum(v[i] for v in vectors)
            skew = abs(2 * ones - total)
            if skew == total:  # every survivor agrees; this probe teaches nothing
                continue
            if best_skew is None or skew < best_skew:
                best, best_skew = point, skew
        return best


def solve_weights(labels: dict[Point, int], weight_limit: int = WEIGHT_LIMIT) -> Params | None:
    """Simplest integer (w1, w2, b) reproducing a set of already-known labels.

    Ranking by |w1| + |w2| then |b| picks the tidiest of the infinitely many
    valid answers; any positive scaling of a solution is also a solution.
    """
    if not labels:
        raise ValueError("no observations to fit")
    space = VersionSpace(weight_limit)
    for point, bit in labels.items():
        space.observe(point, bit)

    best: Params | None = None
    best_cost: tuple[int, int] | None = None
    for d, (w1, w2) in enumerate(space.dirs):
        window = space.bias_window(d)
        if window is None:
            continue
        b_lo, b_hi = window
        b = min(max(0, b_lo), b_hi)  # the bias in range closest to zero
        cost = (abs(w1) + abs(w2), abs(b))
        if best_cost is None or cost < best_cost:
            best, best_cost = (w1, w2, b), cost
    return best


def verify(params: Params, labels: dict[Point, int]) -> list[Point]:
    """Probed points the candidate gets wrong (empty == the server will accept)."""
    return [p for p, bit in labels.items() if predict(params, *p) != bit]


OPENING = [(-10, -10), (10, 10), (10, -10), (-10, 10), (0, 0)]


def active_solve(oracle, max_probes: int = MAX_PROBES, verbose: bool = True):
    """Probe adaptively until the surviving hypotheses are unanimous.

    `oracle` takes (x, y) and returns 0 or 1. Returns (params, observations).
    """
    space = VersionSpace()
    for point in OPENING:
        space.observe(point, oracle(*point))

    while True:
        survivors = space.survivors()
        if not survivors:
            raise RuntimeError("no hypothesis fits the observations; raise WEIGHT_LIMIT")
        vectors = space.label_vectors(survivors)
        if space.settled(vectors):
            break
        if len(space.observations) >= max_probes:
            raise RuntimeError(
                f"probe budget exhausted with {len(survivors)} hypotheses still standing"
            )
        point = space.next_query(vectors)
        if point is None:
            break
        bit = oracle(*point)
        space.observe(point, bit)
        if verbose:
            print(
                f"  probe {len(space.observations):>3}: {point} -> {bit}"
                f"   ({len(survivors)} hypotheses left)",
                file=sys.stderr,
            )

    params = solve_weights(space.observations)
    if params is None:
        raise RuntimeError("consistent behaviour found but no simple parameters")
    return params, space.observations


# --- network I/O ------------------------------------------------------------


def recv_until_prompt(sock: socket.socket) -> str:
    data = b""
    while True:
        try:
            chunk = sock.recv(4096)
        except socket.timeout:
            break
        if not chunk:
            break
        data += chunk
        text = data.decode("utf-8", "replace")
        if "academy{" in text.lower():
            break
        if text.rstrip().endswith(">"):
            break
    return data.decode("utf-8", "replace")


def parse_bit(response: str) -> int:
    if not response.strip():
        raise ConnectionError("server sent nothing: connection closed or budget spent")
    lowered = response.lower()
    if "fires" in lowered or "-> 1" in lowered:
        return 1
    if "quiet" in lowered or "-> 0" in lowered:
        return 0
    for token in reversed(response.replace(">", " ").split()):
        if token in ("0", "1"):
            return int(token)
    raise ValueError(f"cannot read a verdict from: {response!r}")


def send_line(sock: socket.socket, line: str) -> str:
    sock.sendall(f"{line}\n".encode())
    return recv_until_prompt(sock)


def main() -> int:
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()

    submit = "--no-test" not in args
    ports = [a for a in args if a.isdigit()]
    port = int(ports[0]) if ports else DEFAULT_PORT

    with socket.create_connection((HOST, port), timeout=10) as sock:
        sock.settimeout(5)
        print(recv_until_prompt(sock))

        def oracle(x: int, y: int) -> int:
            return parse_bit(send_line(sock, f"{x},{y}"))

        params, observations = active_solve(oracle)
        w1, w2, b = params
        wrong = verify(params, observations)
        print(
            f"\nsettled after {len(observations)} probes"
            f" (server allows {SERVER_BUDGET})"
        )
        print(f"boundary: {w1}*x1 + {w2}*x2 + {b} >= 0")
        if wrong:
            print("candidate disagrees with the oracle, refusing to submit")
            return 1
        if not submit:
            return 0
        print(send_line(sock, f"TEST {w1} {w2} {b}"))

    return 0


# --- offline proving ground -------------------------------------------------


def self_test() -> int:
    """Fit known perceptrons offline, counting probes. No instance burned."""
    cases: list[Params] = [
        (1, 0, -2),      # the 1D challenge, embedded in 2D
        (1, 1, 0),       # the Neuron Meet 2D-0 diagonal
        (3, -2, 5),
        (-1, 4, -7),
        (0, 1, 3),
        (2, 3, -1),
        (7, 5, 33),
        (0, 0, 1),       # degenerate: always fires
        (0, 0, -1),      # degenerate: never fires
    ]
    points = grid()
    failures = 0
    worst = 0
    for truth in cases:
        labels = {p: predict(truth, *p) for p in points}
        found, observations = active_solve(lambda x, y: predict(truth, x, y), verbose=False)
        wrong = verify(found, labels)  # against the FULL grid, as the server checks
        worst = max(worst, len(observations))
        if wrong:
            failures += 1
        status = "ok" if not wrong else f"FAIL ({len(wrong)} mismatches)"
        print(
            f"  truth {str(truth):>14} -> recovered {str(found):>14}"
            f"  in {len(observations):>3} probes  {status}"
        )
    print(
        "all self-tests passed" if not failures else f"{failures} self-test failure(s)"
    )
    print(f"worst case: {worst} probes (budget {SERVER_BUDGET})")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
