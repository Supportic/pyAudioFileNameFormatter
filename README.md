# pyAudioFileNameFormatter

## Description

This is a python script that formats music filenames which contain underscores `'_'` or leading numbers `'01_'` and tries to recreate a new filename with following formatting pattern:

`Artist - Trackname`

Currently only .mp3 files are supported but .wav, .flac are already considered as well.
The **eyeD3** library <https://github.com/nicfit/eyeD3> is used to work with .mp3 tags. Thanks to him!

## Get it working

A `tracks` folder in the directory of the python program is needed, but can be changed in the `MUSIC_PATH` variable.
Drop all music files in this folder and start the python program.

```bash
python FormatAudioFile.py
```