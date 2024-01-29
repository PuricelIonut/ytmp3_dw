import os
import argparse
import pathlib
import sys
from pytube import YouTube, Playlist

# Download song function
def download_song(video_url, output_dir):
    if determine_url_type(video_url) == 'song':
        try:
            if not os.path.isfile(output_dir) and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            yt = YouTube(video_url)
            valid_filename = ''.join(e for e in yt.title if e.isalnum() or e in ' .-_')
            file_path = os.path.join(output_dir, f'{valid_filename}.mp3')

            if os.path.exists(file_path):
                print(f'The song "{valid_filename}.mp3" already exists in the output directory.')
                return

            audio_streams = yt.streams.filter(only_audio=True)
            audio_streams = sorted(audio_streams, key=lambda s: s.abr, reverse=True)

            if not audio_streams:
                print('No audio streams found for this video.')
                return

            audio_streams[0].download(output_path=output_dir, filename=f'{valid_filename}.mp3')
            print(f'Successfully downloaded: {valid_filename}.mp3')
        except Exception as e:
            print(f'Error occurred: {str(e)}')
    else:
        print('Invalid YouTube song URL.')
        sys.exit()

# Download playlist songs function
def download_playlist(playlist_url, output_dir):
    if determine_url_type(playlist_url) == 'playlist':
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        
            pl = Playlist(playlist_url)
            video_urls = pl.video_urls
            
            for video_url in video_urls:
                yt = YouTube(video_url)
                valid_filename = ''.join(e for e in yt.title if e.isalnum() or e in ' .-_')
                file_path = os.path.join(output_dir, f'{valid_filename}.mp3')

                if os.path.exists(file_path):
                    print(f'The song "{valid_filename}.mp3" already exists in the output directory.')
                    continue

                audio_streams = yt.streams.filter(only_audio=True)
                audio_streams = sorted(audio_streams, key=lambda s: s.abr, reverse=True)

                if not audio_streams:
                    print(f'No audio streams found for the video: {valid_filename}')
                    continue

                audio_streams[0].download(output_path=output_dir, filename=f'{valid_filename}.mp3')
                print(f'Successfully downloaded: {valid_filename}.mp3')
        except Exception as e:
            print(f'Error occurred: {str(e)}')
    else:
        print('Invalid YouTube playlist URL.')
        sys.exit()
        
# URL format check function
def determine_url_type(url):
    if "playlist" in url and "list=" in url:
        return "playlist"
    elif "watch?v=" in url:
        return "song"
    else:
        return None
 
# Get the args stored
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YouTube MP3 Downloader')
    parser.add_argument('mode', choices=['song', 'playlist'], help='Download mode (song or playlist)')
    parser.add_argument('url', help='URL of the YouTube video or playlist')
    parser.add_argument('output', help='Output directory',nargs='?', default=pathlib.Path(__file__).parent.resolve())
    args = parser.parse_args()
         
# Run the script based on mode and make sure the program stops on keyboardi interrupt
try:
    if args.mode == 'song':
        download_song(args.url, args.output)
    elif args.mode == 'playlist':
        download_playlist(args.url, args.output)
except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
    