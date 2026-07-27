# Transmission

## Metadata

- Event: Cybersplash 2026
- Category: Misc
- Difficulty: Unknown
- Status: Solved
- Files: [transmission.wav](transmission.wav)
- Skills Learned: Audio analysis

## Problem Summary

The challenge provides a WAV file.

## What I Tried

1. `exiftool transmission.wav`

    ```txt
    ExifTool Version Number         : 13.55
      File Name                       : transmission.wav
      Directory                       : .
      File Size                       : 484 kB
      File Modification Date/Time     : 2026:04:05 09:29:09+07:00
      File Access Date/Time           : 2026:05:15 22:01:44+07:00
      File Inode Change Date/Time     : 2026:05:15 21:07:21+07:00
      File Permissions                : -rw-r--r--
      File Type                       : WAV
      File Type Extension             : wav
      MIME Type                       : audio/x-wav
      Encoding                        : Microsoft PCM
      Num Channels                    : 1
      Sample Rate                     : 44100
      Avg Bytes Per Sec               : 88200
      Bits Per Sample                 : 16
      Duration                        : 5.48 s
    ```

2. install `brew install --cask audacity`
3. open audacity inspect Waveform
   - 0.0–2.0s: loud signal (~22,000–26,000 amplitude)
   - 2.0–3.8s: quiet (~4,000–5,000 amplitude) — but notice it's not silence, it's low-level noise
   - 3.9–5.4s: medium signal (~10,000–12,000 amplitude)
4. View Spectrogram on the audacity
   - get this ![snapshot](./Screenshot%202569-07-27%20at%2018.08.18.png)
   - increased window size to 4096 for sharper resolution, zoomed in, read the text carefully
   - flag was written in white text across the spectrogram: `misc{7M5_h1du73_m3ssAge?_r3as1dn}`

## Key Idea

hide flag in Spectrogram

## Solution Walkthrough

- open audio to audacity
- view Spectrogram

## Flag

`misc{7M5_h1du73_m3ssAge?_r3as1dn}`

## Lessons Learned

- Audio challenges should start with metadata, waveform, and spectrogram inspection.
