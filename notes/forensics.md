# Forensics Notes

## Beginner Checklist

- Start with file type, magic bytes, metadata, and embedded files.
- Preserve original artifacts.
- Keep generated outputs only when they prove or explain the solve path.

## Audio

WAV triage order (cheapest → most expensive):

1. **Metadata** — `exiftool file.wav`. Check for hidden comments or custom fields.
2. **Waveform** — open in Audacity. Look for irregular patterns, silence with blips, or suspicious structure.
3. **Spectrogram** — track dropdown → Spectrogram. Flags/images hidden in frequency space are invisible in the waveform. Increase window size (4096–8192) for sharper resolution. Most common audio CTF technique.
4. **LSB steganography** — hidden data in the least significant bit of each sample. Tools: `steghide`, Python script.
5. **Audio-encoded signals** — actually listen. Morse (short/long beeps), DTMF (phone tones), fax handshake. Decode what you hear.

> Example: [Cybersplash Transmission](../events/2026/cybersplash/misc/transmission/README.md) — flag drawn as text in spectrogram.

## Image

- **Appended data (JPEG):** data hidden after `FF D9` end marker. Check with `xxd file.jpg | tail -20`. Renderers stop at `FF D9`; the bytes after are invisible to viewers but still in the file.
- **PNG IHDR tampering:** IHDR width/height can be reduced to hide pixel rows/columns. Check by decompressing IDAT (`zlib.decompress`) and comparing size against declared dimensions. Patch IHDR and recalculate CRC to restore.
- **QR code damage:** QR codes have error correction (up to 30% recoverable). Always try scanning before attempting manual repair.

> Example: [Cybersplash Image Repair](../events/2026/cybersplash/misc/image-repair/README.md)

## Repo Examples

- [TCP1P Skibidi Format](../events/2024/tcp1p/forensics/skibidi-format/README.md)
- [Cybersplash image repair](../events/2026/cybersplash/misc/image-repair/README.md)
- [Cybersplash Spectrogram WaveAudio](../events/2026/cybersplash/misc/transmission/README.md)
