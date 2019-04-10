# Author: Alexander Senger
# Version: 0.0.1

import eyed3
import os
import sys
import time

import logging
logging.basicConfig(level=logging.ERROR)

# tracks folder
MUSIC_PATH = os.path.join(os.getcwd(), "tracks")

# additional not needed string extensions in the file title
appendix = [
  " (Original Mix)",
  " (Extended Mix)"
]

def reconstructDataOutOfFilename(fileString):

  # replace all underscores
  test = fileString.replace("_", " ")
  # detect the file extension
  fileExtension = test.split(".")[1]
  # remove the file extension
  test = test[:-(len(fileExtension)+1)] # +1 for the dot at the end
  # remove all numbers
  test = ''.join([i for i in test if not i.isdigit()])
  # remove all hyphens
  artistName, trackName = test.split(" - ")

  # prepare the artistName
  artistName = artistName.replace("-", "")
  artistName = artistName.replace("and", "&")
  artistName = artistName.lstrip(' ')  # removes first white space

  # prepare the trackName
  for element in appendix:
    if trackName.title().endswith(element):
      trackName = trackName[:-(len(element))]
      break

  return artistName.title(), trackName.title()

def renameFile(artistName, trackName, fileString, newFileString):

  # only rename the file if the filenames are unidentical
  if fileString != newFileString:
    src = MUSIC_PATH + os.sep + fileString
    dst = MUSIC_PATH + os.sep + newFileString

    print(f"[{fileString}] -> [{newFileString}]")

    try:
      os.rename(src, dst)
    except OSError:
      print(f'Error: File in use [{fileString}]')


def examineFileString(artistNameTag, trackNameTag, fileString, audiofile):

  if (artistNameTag and trackNameTag):
    artistName = artistNameTag
    trackName = trackNameTag
  else:
    artistName, trackName = reconstructDataOutOfFilename(fileString)
    # this is even possible when the properties window is open and the file is in use, but the window needs a reload
    # check later on if it's .mp3 before writing it in tags
    audiofile.tag.artist = artistName
    audiofile.tag.title = trackName
    audiofile.tag.save()
    
  newFileString = f"{artistName} - {trackName}.mp3"
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

  artistName, trackName, newFileString = examineFileString(artistNameTag, trackNameTag, fileString, audiofile)

  renameFile(artistName, trackName, fileString, newFileString)

def findMusicFiles():
  # scan files in the directory
  fileNameList = [f for f in os.listdir(MUSIC_PATH) if os.path.isfile(os.path.join(MUSIC_PATH, f))]
  musicFiles = []
  for file in fileNameList:
    # endswith can be extended by e.g. (('.mp3', '.flac'))
    if file.lower().endswith('.mp3'):
      musicFiles.append(file)
  return musicFiles

def main():
  
  musicFiles = findMusicFiles()
  for musicFileString in musicFiles:
    audiofile = eyed3.load(os.path.join(MUSIC_PATH, musicFileString))
    # TODO: if musicFileString endswith .wav/.mp3/.flac
    adjustFile(audiofile, musicFileString)
  print('Done')

if __name__ == '__main__':
  executionStartTime = time.time()
  main()
  executionEndTime = time.time()
  print(f'Execution time: {executionEndTime - executionStartTime}s')
