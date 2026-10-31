"""Known-by-structure checks: indices the dropper feeds to require()/process.platform."""
from decode_hook import decode

def test_node_module_names():
    assert decode(0x1B) == "crypto"
    assert decode(0x1C) == "fs"
    assert decode(0x1D) == "path"
    assert decode(0x1A) == "child_process"

def test_platform_gate():
    assert decode(0x19) == "win32"
