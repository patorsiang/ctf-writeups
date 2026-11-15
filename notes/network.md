# Network Notes

## Triage playbook (easy, ≤1 page)

Fill from drills — each new line must cite the drill that taught it.

First look at a capture (tools checked by `tools/check_kit.sh`):

- `tshark -r cap.pcap -q -z io,phs`: which protocols are in the capture.
- `tshark -r cap.pcap -q -z conv,tcp`: who talks to whom, and how much.
- `tshark -r cap.pcap -Y http.request -T fields -e http.host -e http.request.uri`: HTTP requests.
- Wireshark → Statistics → Protocol Hierarchy; Follow → TCP Stream on the largest conversation.
- Wireshark → File → Export Objects → HTTP (also SMB, TFTP) to pull out transferred files.
- `strings -n 6 cap.pcap | grep -i flag`: the cheap check, done before anything clever.

## Repo Examples
