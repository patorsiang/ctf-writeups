import dns_exfil as d

GUID = "60cb634d-1345-47f0-b256-293afe32b6e9"

def test_host_tag_matches_cfg_query():
    assert d.host_tag(GUID) == "0de039b0"

def test_session_id_matches_exfil_labels():
    k = d.derive_key(d.host_tag(GUID), d.txt_records())
    assert d.session_id(k) == "7019242e"

def test_crc_and_count_match_final_beacon():
    out = d.recover(GUID)
    assert out["n"] == out["n_expected"]
    assert out["crc"] == out["crc_expected"]

def test_hmac_ok_and_result_is_zip():
    out = d.recover(GUID)
    assert out["mac_ok"]
    assert out["plain"][:2] == b"PK"
