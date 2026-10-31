"""Offline tests for solve.py's parsing logic, run against the realm export
actually captured during the live solve (artifacts/realm-helios.json).

The live target VM was torn down after capture, so these tests cover the
part of the chain that doesn't need the network: picking the right user out
of the realm export. The network leg (path traversal -> login -> /vault) was
exercised against the live host during the session; its actual HTTP
responses are quoted in README.md.
"""

import json
import pathlib

import pytest

from solve import find_platform_admin

ARTIFACT = pathlib.Path(__file__).parent / "artifacts" / "realm-helios.json"


@pytest.fixture
def realm_export():
    return json.loads(ARTIFACT.read_text())


def test_finds_the_platform_admin_user(realm_export):
    username, password = find_platform_admin(realm_export)
    assert username == "k.thepsuwan"
    assert password == "Wq5-Helios-Platform-2026-nH"


def test_does_not_pick_a_staff_only_user():
    # Known-bad case: a realm export where the only enabled user lacks
    # platform-admin must not be returned as if it were valid.
    fake_export = {
        "users": [
            {
                "username": "r.vongkham",
                "enabled": True,
                "realmRoles": ["default-roles-helios", "staff"],
                "credentials": [
                    {"type": "password", "value": "irrelevant", "temporary": False}
                ],
            }
        ]
    }
    with pytest.raises(LookupError):
        find_platform_admin(fake_export)


def test_skips_disabled_platform_admin_users():
    fake_export = {
        "users": [
            {
                "username": "disabled.admin",
                "enabled": False,
                "realmRoles": ["platform-admin"],
                "credentials": [
                    {"type": "password", "value": "nope", "temporary": False}
                ],
            },
            {
                "username": "k.thepsuwan",
                "enabled": True,
                "realmRoles": ["platform-admin", "staff"],
                "credentials": [
                    {"type": "password", "value": "real-one", "temporary": False}
                ],
            },
        ]
    }
    username, password = find_platform_admin(fake_export)
    assert username == "k.thepsuwan"
    assert password == "real-one"
