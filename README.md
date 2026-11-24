# Wick Editor (iPad fix)

A copy of the open-source [Wick Editor](https://github.com/Wicklets/wick-editor) (v1.19.3), patched so it works on iPad, hosted with GitHub Pages.

**Testing copy:** https://kingjab1.github.io/Wicktest/

This is the sandbox for new features. It has everything the classroom version has, plus features being tested. The classroom version is [kingjab1/wick-editor](https://github.com/kingjab1/wick-editor) at https://animate.jabari.art.

## What's different from the original

- **Buttons respond to a full tap.** The original fired actions on touch-down, and iPad Safari won't open a file picker from that, so Open and asset upload did nothing.
- **File pickers work on iPad.** The hidden file input is now actually on the page, and the file-type filter is skipped on iOS so `.wick` projects aren't greyed out.
- **Sound import is more reliable.** Fixed a file-extension check in the engine and added `.m4a`/`.aac` (iPad Voice Memos).
- **Learn tab.** A Learn button opens example exercises (tagged by animation principle) and a Principles view. Content lives in [`learn/`](learn/README.md) and is loaded at runtime, so adding an example never needs a rebuild. Layers named Notes or Annotations show while editing but never in exports.
- **Sound library.** The + button in the Asset Library opens Sounds and Clips. See `sounds/README.md` for where each set comes from.
- **Record sounds** (testing). A Record tab in Sounds uses the microphone; recordings become WAV files at the playhead. Needs https.
- **Frame length buttons** (testing). In the timeline's top row: − Length + changes the selected drawing by one frame, and Push / Overwrite picks whether the next frames move along or get covered.
- **Loops** (testing). Loop frames turns the selected frames into one looping frame. +1 loop and Loop to end make it repeat; Edit loop goes inside to change the drawings, Done comes back. In the timeline each pass of a loop has its own shade, with a dot where each drawing inside starts.
- **Play range** (testing). Start and End set where playing begins and ends, from the playhead; the range shows as a green band over the frame numbers, and tapping the range chip clears it. Repeat / Once picks whether playing starts over or stops at the end. The range is remembered per project in each browser.
- **My Work and teacher mode** (hidden until `cloud-config.json` is added). See `cloud/README.md`.
- **Hosting tweaks.** Built-in library objects are served as `.wickobj.json`, and the video exporter (`ffmpeg.js`) is split into two files.

## Source

This is the built site. The source changes against upstream commit `f34f0d9` are in [`source-changes.patch`](source-changes.patch). Apply them to a clone of [Wicklets/wick-editor](https://github.com/Wicklets/wick-editor), then split `public/corelibs/video/ffmpeg.js` into `ffmpeg.part1.js` and `ffmpeg.part2.js` (each file pushes half of the original text, as a string, onto `self.__ffsrc`).

Textured brushes and Line/Color art were taken out for now and saved in [`parked/`](parked/README.md) to rework later.

The Wick Editor is licensed under the GNU GPL v3. See `license_en.txt`. Wick Editor is made by Wicklets LLC; this copy isn't affiliated with them.
