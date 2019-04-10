# Author: Alexander Senger
# Version: 0.0.1
# Description: A tool that formats music filenames which contains underscores "_"

import eyed3
import os
import sys
import time

import logging
logging.basicConfig(level=logging.ERROR)

# tracks folder
MP3_PATH = os.path.join(os.getcwd(), "tracks")

appendix = [
  " (Original Mix)",
  " (Extended Mix)"
]

def renameFile(artistName, trackName, fileString, newFileString):

  # only rename the file if the filenames are unidentical
  if fileString != newFileString:
    src = MP3_PATH + os.sep + fileString
    dst = MP3_PATH + os.sep + newFileString

    print(f"[{fileString}] -> [{newFileString}]")

    try:
      os.rename(src, dst)
    except OSError:
      print(f'Error: File in use [{fileString}]')

def examineFileString(artistNameTag, trackNameTag, fileString):

  if (artistNameTag and trackNameTag):
    artistName = artistNameTag
    trackName = trackNameTag
    newFileString = f"{artistNameTag} - {trackNameTag}.mp3"
  else:
    #TODO: extraction of artistName and trackName of fileName
    artistName = artistNameTag
    trackName = trackNameTag
    newFileString = fileString

  return artistName, trackName, newFileString

def getArtistNameAndTrackNameFromTag(audiofile):
  if audiofile.tag.artist is None:
    artistName = None
  else:
    artistName = audiofile.tag.artist.lstrip(' ') #remove first white space

  if audiofile.tag.title is None:
    trackName = None
  else:
    trackName = audiofile.tag.title.lstrip(' ') #remove first white space
    for element in appendix:
      if trackName.endswith(element):
        trackName = trackName[:-(len(element))]
        break
    audiofile.tag.title = trackName
    audiofile.tag.save()

  return artistName, trackName

def adjustFile(audiofile, fileString):
  # try to get data from tags
  artistNameTag, trackNameTag = getArtistNameAndTrackNameFromTag(audiofile)

  artistName, trackName, newFileString = examineFileString(artistNameTag, trackNameTag, fileString)

  renameFile(artistName, trackName, fileString, newFileString)

def findMusicFiles():
  # scan files in the directory
  fileNameList = [f for f in os.listdir(MP3_PATH) if os.path.isfile(os.path.join(MP3_PATH, f))]
  musicFiles = []
  for file in fileNameList:
    # endswith can be extended by e.g. (('.mp3', '.flac'))
    if file.lower().endswith('.mp3'):
      musicFiles.append(file)
  return musicFiles

def main():
  
  musicFiles = findMusicFiles()
  for musicFileString in musicFiles:
    audiofile = eyed3.load(os.path.join(MP3_PATH, musicFileString))
    adjustFile(audiofile, musicFileString)

  print('Done')

# if it's our program
if __name__ == '__main__':
  executionStartTime = time.time()
  main()
  executionEndTime = time.time()
  print(f'Execution time: {executionEndTime - executionStartTime}s')
