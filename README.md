# pyAudioFileNameFormatter

## Description

This is a python script that formats music filenames which contain underscores `'_'` or leading numbers `'01_'` and tries to recreate a new filename with following formatting pattern:

`Artist - Trackname`

Currently only .mp3 files are supported but .wav, .flac will be considered later as well.
The **eyeD3** module <https://github.com/nicfit/eyeD3> is used to work with .mp3 tags. Thanks to him!

## Get it working

A default `tracks` folder in the directory of the python program is needed, but will be created on the first execution if no other path is defined.
Drop all music files in this folder (`./tracks`) and start the python program.

```console
python FormatAudioFile.py
```

### PATH parameter

You can specify another path in order to perform the trackname transformation.

```bash
python FormatAudioFile.py -p <PATH>
```

**or**

```bash
python FormatAudioFile.py --path <PATH>
```