# YouTube MP3 Downloader
## Overview

Download either a single YouTube song or an entire playlist in MP3 format. It utilizes the `pytube` library to interact with YouTube and download the audio content.

## Prerequisites

Make sure you have the following dependencies installed:

- [pytube](https://github.com/pytube/pytube)
- [tkinter](https://docs.python.org/3/library/tkinter.html) (GUI version) 

You can install them using the following command:

pip install pytube

## Command-line ("ytmp3.py") usage: 
  "python youtube_downloader.py <mode> <url> <output_directory>"

<mode>: Specify the download mode, either 'song' or 'playlist'.
<url>: Provide the URL of the YouTube video or playlist you want to download.
<output_directory>: Optional. Specify the output directory where the MP3 files will be saved. If not provided, the default is the script's parent directory.

eg. :
  python youtube_downloader.py song <song_url> <output_directory>
  python youtube_downloader.py playlist <playlist_url> <output_directory>

## GUI version ("ytmp3ui.py"):
  A much user friendly version of the script. I made a simple GUI using tkinter.

## Features:
  Can easily pick between a song or a playlist, easy way to browse files to pick a path, download button and stop button. All the actions are displayed in a log window for the user to see the progress.

## URL Format
  The script determines whether the provided URL is for a song or a playlist. It checks for the presence of "playlist" and "list=" for playlists and "watch?v=" for songs.

## Output
  For single songs, the script downloads the corresponding MP3 file and saves it in the specified output directory.
  For playlists, the script iterates through the playlist, downloads each song, and saves them in the output directory.

##Note
  - The script ensures that the filenames are valid by removing special characters from the YouTube video titles.
  - If a downloaded song already exists in the output directory, the script skips the download for that particular song.
  - The script stops gracefully on a keyboard interrupt.
  
