# Mystery Files

## Metadata

- Event: Cybersplash 2026
- Category: Misc
- Difficulty: Unknown
- Status: Solved
- Files: [archive.wav](archive.wav), [data.mp3](data.mp3), [document.jpg](document.jpg), [image.txt](image.txt), [music.pdf](music.pdf), [readme.png](readme.png)
- Skills Learned: File identification, steganography triage

## Problem Summary

This challenge includes files with mixed extensions and media types.

## What I Tried

- to check the real file type: `file <filename>`
archive.wav:  gzip compressed data, was "dummy.txt", last modified: Sat Apr  4 17:25:15 2026, max compression, original size modulo 2^32 77
data.mp3:     GIF image data, version 89a, 1 x 1
document.jpg: PDF document, version 1.4, 1 pages
image.txt:    PNG image data, 200 x 200, 8-bit/color RGB, non-interlaced
music.pdf:    RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 44100 Hz
readme.png:   ASCII text

┌──────────────┬──────────────┐
│   Filename   │ Actually is  │
├──────────────┼──────────────┤
│ archive.wav  │ gzip archive │
├──────────────┼──────────────┤
│ data.mp3     │ GIF image    │
├──────────────┼──────────────┤
│ document.jpg │ PDF          │
├──────────────┼──────────────┤
│ image.txt    │ PNG image    │
├──────────────┼──────────────┤
│ music.pdf    │ WAV audio    │
├──────────────┼──────────────┤
│ readme.png   │ ASCII text   │
└──────────────┴──────────────┘

- for readme.png

 ```sh
 # back to real type file
 cp readme.png readme.txt

 # read text inside
 cat readme.txt
 === System Recovery Log ===
 Date: 2026-03-15
 Status: COMPLETE

 Disk scan completed successfully.
 Partition table verified.
 File system integrity check passed.
 No bad sectors detected.

 Recovery Key: misc{0hm_z3saM33_zZZ}

 All systems nominal.
 End of log.
 ```

- for image.txt

 ```sh
 cp image.txt image.png

 # check meta
 strings image.txt | grep misc
 exiftool image.txt
 ExifTool Version Number         : 13.55
 File Name                       : image.txt
 Directory                       : .
 File Size                       : 657 bytes
 File Modification Date/Time     : 2026:04:11 15:19:01+07:00
 File Access Date/Time           : 2026:07:30 14:19:45+07:00
 File Inode Change Date/Time     : 2026:04:11 15:19:01+07:00
 File Permissions                : -rw-r--r--
 File Type                       : PNG
 File Type Extension             : png
 MIME Type                       : image/png
 Image Width                     : 200
 Image Height                    : 200
 Bit Depth                       : 8
 Color Type                      : RGB
 Compression                     : Deflate/Inflate
 Filter                          : Adaptive
 Interlace                       : Noninterlaced
 Image Size                      : 200x200
 Megapixels                      : 0.040

 # LSB steganography
 ~/.gem/ruby/2.6.0/bin/zsteg image.txt
 b2,g,lsb,xy         .. file: 5View capture file
 b2,g,msb,xy         .. file: VISX image file
 b2,b,lsb,xy         .. text: ["U" repeated 50 times]
 b2,b,msb,xy         .. text: ["U" repeated 50 times]
 b4,g,lsb,xy         .. text: "\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"33333333333333333333333333333333333333333333333333333333"
 b4,g,msb,xy         .. text: ["D" repeated 200 times]
 b4,b,lsb,xy         .. text: "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"
 b4,b,msb,xy         .. text: ["\"" repeated 200 times]
 ```

- for archive.wav

 ```sh
 cp archive.wav archive.gz && gunzip archive.gz && cat archive
 This is a dummy file used for testing compression.
 Nothing interesting here.
 ```

- for document.jpg

 ```sh
 cp document.jpg document.pdf && open document.pdf
 Nothing here.

 # PDFs can hide text (white on white) or have data appended after %%EOF. Check both:
 strings document.jpg | grep misc
 xxd document.jpg | tail -20
 00000110: 7374 7265 616d 0a42 540a 2f46 3120 3132  stream.BT./F1 12
 00000120: 2054 660a 3130 3020 3730 3020 5464 0a28   Tf.100 700 Td.(
 00000130: 4e6f 7468 696e 6720 6865 7265 2e29 2054  Nothing here.) T
 00000140: 6a0a 4554 0a65 6e64 7374 7265 616d 0a65  j.ET.endstream.e
 00000150: 6e64 6f62 6a0a 0a35 2030 206f 626a 0a3c  ndobj..5 0 obj.<
 00000160: 3c20 2f54 7970 6520 2f46 6f6e 7420 2f53  < /Type /Font /S
 00000170: 7562 7479 7065 202f 5479 7065 3120 2f42  ubtype /Type1 /B
 00000180: 6173 6546 6f6e 7420 2f48 656c 7665 7469  aseFont /Helveti
 00000190: 6361 203e 3e0a 656e 646f 626a 0a0a 7872  ca >>.endobj..xr
 000001a0: 6566 0a30 2036 0a30 3030 3030 3030 3030  ef.0 6.000000000
 000001b0: 3020 3635 3533 3520 660a 3030 3030 3030  0 65535 f.000000
 000001c0: 3030 3039 2030 3030 3030 206e 0a30 3030  0009 00000 n.000
 000001d0: 3030 3030 3035 3820 3030 3030 3020 6e0a  0000058 00000 n.
 000001e0: 3030 3030 3030 3031 3135 2030 3030 3030  0000000115 00000
 000001f0: 206e 0a30 3030 3030 3030 3236 3620 3030   n.0000000266 00
 00000200: 3030 3020 6e0a 3030 3030 3030 3033 3630  000 n.0000000360
 00000210: 2030 3030 3030 206e 0a0a 7472 6169 6c65   00000 n..traile
 00000220: 720a 3c3c 202f 5369 7a65 2036 202f 526f  r.<< /Size 6 /Ro
 00000230: 6f74 2031 2030 2052 203e 3e0a 7374 6172  ot 1 0 R >>.star
 00000240: 7478 7265 660a 3433 340a 2525 454f 460a  txref.434.%%EOF.
 ```

- for data.mp3

 ```sh
 xxd data.mp3 | tail -20
 00000000: 4749 4638 3961 0100 0100 8000 00ff ffff  GIF89a..........
 00000010: 0000 0021 f904 0000 0000 002c 0000 0000  ...!.......,....
 00000020: 0100 0100 0002 0244 0100 3b              .......D..;
 ```

- for music.pdf

 ```sh
 exiftool music.pdf
 ExifTool Version Number         : 13.55
 File Name                       : music.pdf
 Directory                       : .
 File Size                       : 88 kB
 File Modification Date/Time     : 2026:04:11 15:19:01+07:00
 File Access Date/Time           : 2026:07:30 14:29:44+07:00
 File Inode Change Date/Time     : 2026:07:30 14:08:11+07:00
 File Permissions                : -rw-r--r--
 File Type                       : WAV
 File Type Extension             : wav
 MIME Type                       : audio/x-wav
 Encoding                        : Microsoft PCM
 Num Channels                    : 1
 Sample Rate                     : 44100
 Avg Bytes Per Sec               : 88200
 Bits Per Sample                 : 16
 Duration                        : 1.00 s

 cp music.pdf music.wav && open -a Audacity music.wav
 strings music.pdf | grep misc
 xxd music.pdf | tail -20
 ```

- `binwalk` scans a file for known file signatures (magic bytes) at every byte offset

 ```sh
 for f in archive.wav data.mp3 document.jpg image.txt music.pdf readme.png; do echo "=== $f ==="; binwalk "$f"; done

=== archive.wav ===

             /Users/napatcholthaipanich/Dev/ctf-writeups/events/2026/cybersplash/misc/mystery-files/archive.wav
----------------------------------------------------------------------------------------------------------------------------

DECIMAL                            HEXADECIMAL                        DESCRIPTION
----------------------------------------------------------------------------------------------------------------------------

0                                  0x0                                gzip compressed data, original file name:
                                                                      "dummy.txt", operating system: unknown, timestamp:
                                                                      2026-04-04 17:25:15, total size: 97 bytes
----------------------------------------------------------------------------------------------------------------------------

Analyzed 1 file for 85 file signatures (187 magic patterns) in 2.0 milliseconds
=== data.mp3 ===

               /Users/napatcholthaipanich/Dev/ctf-writeups/events/2026/cybersplash/misc/mystery-files/data.mp3
----------------------------------------------------------------------------------------------------------------------------

DECIMAL                            HEXADECIMAL                        DESCRIPTION
----------------------------------------------------------------------------------------------------------------------------

0                                  0x0                                GIF image, 1x1 pixels, total size: 43 bytes
----------------------------------------------------------------------------------------------------------------------------

Analyzed 1 file for 85 file signatures (187 magic patterns) in 2.0 milliseconds
=== document.jpg ===
Analyzed 1 file for 85 file signatures (187 magic patterns) in 1.0 milliseconds
=== image.txt ===

              /Users/napatcholthaipanich/Dev/ctf-writeups/events/2026/cybersplash/misc/mystery-files/image.txt
----------------------------------------------------------------------------------------------------------------------------

DECIMAL                            HEXADECIMAL                        DESCRIPTION
----------------------------------------------------------------------------------------------------------------------------

0                                  0x0                                PNG image, total size: 657 bytes
----------------------------------------------------------------------------------------------------------------------------

Analyzed 1 file for 85 file signatures (187 magic patterns) in 1.0 milliseconds
=== music.pdf ===
Analyzed 1 file for 85 file signatures (187 magic patterns) in 1.0 milliseconds
=== readme.png ===
Analyzed 1 file for 85 file signatures (187 magic patterns) in 1.0 milliseconds

```

## Key Idea

- check the file type
- covert to its' real type
- open it
- check meta
- check strings

## Solution Walkthrough

1. Run `file` on all six files — every extension is wrong
2. Map each file to its real type (see table above)
3. `readme.png` is ASCII text → `cat` it → flag in the "Recovery Key" field
4. Check all other files for hidden data (metadata, appended bytes, LSB, binwalk) — all are clean decoys

## Flag

`misc{0hm_z3saM33_zZZ}`

## Lessons Learned

- File extensions are labels, not truth — always run `file` first to check magic bytes
- `binwalk` scans for embedded file signatures at every byte offset, not just the start — use it to rule out nested archives
- In misc challenges, most files may be decoys; triage quickly before going deep on any single file
