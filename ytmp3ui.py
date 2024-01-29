import os
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube, Playlist

def download():
    clear_console()

    video_url = url_entry.get()
    output_dir = output_entry.get()

    if not video_url:
        update_console('❌ Please enter a valid video URL.', color='red')
        return

    if not output_dir or not os.path.isdir(output_dir):
        update_console('❌ Please provide a valid output directory path.', color='red')
        return

    if mode_var.get() == 'song':
        if is_playlist_url(video_url):
            update_console('❌ Please enter a valid song URL, not a playlist URL.', color='red')
            return
        update_console('⏳ Working...', color='blue')
        root.update()
        download_song(video_url, output_dir)
    elif mode_var.get() == 'playlist':
        if not is_playlist_url(video_url):
            update_console('❌ Please enter a valid playlist URL, not a song URL.', color='red')
            return
        update_console('⏳ Working...', color='blue')
        root.update()
        download_playlist(video_url, output_dir)

    update_console('✅ All Done', color='green')


def is_playlist_url(url):
    return 'playlist?list=' in url


def download_song(video_url, output_dir):
    try:
        yt = YouTube(video_url)
        if yt.author in yt.title:
            valid_filename = yt.title
        else:
            valid_filename = yt.author + " - " + yt.title
        file_path = os.path.join(output_dir, f'{valid_filename}.mp3')

        if os.path.exists(file_path):
            update_console(f'⚠️ Skipped existing song: {valid_filename}.mp3', color='orange')
            root.update()
            return

        audio_streams = yt.streams.filter(only_audio=True)
        audio_streams = sorted(audio_streams, key=lambda s: s.abr, reverse=True)

        if not audio_streams:
            update_console('⚠️ No audio streams found for this video.', color='orange')
            return

        audio_streams[0].download(output_path=output_dir, filename=valid_filename + '.mp3')
        update_console(f'✅ Successfully downloaded: {valid_filename}.mp3', color='green')
        root.update()


    except Exception as e:
        update_console(f'❌ Error occurred: {str(e)}', color='red')


def download_playlist(playlist_url, output_dir):
    try:
        pl = Playlist(playlist_url)
        video_urls = pl.video_urls

        for i, video_url in enumerate(video_urls):
            yt = YouTube(video_url)
            if yt.author in yt.title:
                valid_filename = yt.title
            else:
                valid_filename = yt.author + " - " + yt.title
            file_path = os.path.join(output_dir, f'{valid_filename}.mp3')

            if os.path.exists(file_path):
                update_console(f'⚠️ Skipped existing song ({i+1}/{len(video_urls)}): {valid_filename}.mp3', color='orange')
                root.update()
                continue

            audio_streams = yt.streams.filter(only_audio=True)
            audio_streams = sorted(audio_streams, key=lambda s: s.abr, reverse=True)

            if not audio_streams:
                update_console(f'⚠️ No audio streams found for the video: {valid_filename}', color='orange')
                continue

            audio_streams[0].download(output_path=output_dir, filename=valid_filename + '.mp3')
            update_console(f'✅ Successfully downloaded ({i+1}/{len(video_urls)}): {valid_filename}.mp3', color='green')
            root.update()

    except Exception as e:
        update_console(f'❌ Error occurred: {str(e)}', color='red')


def browse_output_directory():
    output_dir = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)


def on_mode_changed(*args):
    mode = mode_var.get()
    if mode == 'song':
        output_entry.config(state='normal')
        browse_button.config(state='normal')
        if is_playlist_url(url_entry.get()):
            url_entry.delete(0, tk.END)
    elif mode == 'playlist':
        output_entry.config(state='normal')
        browse_button.config(state='normal')
        if not is_playlist_url(url_entry.get()):
            url_entry.delete(0, tk.END)


def update_console(message, color='black'):
    console_text.config(state=tk.NORMAL)
    console_text.insert(tk.END, message + '\n', color)
    console_text.tag_configure(color, foreground=color)
    console_text.config(state=tk.DISABLED)
    console_text.see(tk.END)


def clear_console():
    console_text.config(state=tk.NORMAL)
    console_text.delete('1.0', tk.END)
    console_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title('YouTube MP3 Downloader')

# Mode Selection
mode_label = tk.Label(root, text='Mode:')
mode_label.grid(row=1, column=0, sticky='w')

mode_var = tk.StringVar()
mode_var.set('song')
mode_var.trace('w', on_mode_changed)

mode_radio1 = tk.Radiobutton(root, text='Song', variable=mode_var, value='song')
mode_radio1.grid(row=2, column=0, sticky='w')

mode_radio2 = tk.Radiobutton(root, text='Playlist', variable=mode_var, value='playlist')
mode_radio2.grid(row=3, column=0, sticky='w')


# URL Entry
url_label = tk.Label(root, text='URL:')
url_label.grid(row=4, column=0, sticky='w')
url_entry = tk.Entry(root)
url_entry.grid(row=5, column=0, padx=10, pady=5, sticky='we', columnspan=2)

# Output Directory Entry
output_label = tk.Label(root, text='Output Directory:')
output_label.grid(row=6, column=0, sticky='w')
output_entry = tk.Entry(root)
output_entry.grid(row=7, column=0, padx=10, pady=5, sticky='we')
output_entry.insert(0, "Please enter output path...")

# Browse Button
browse_button = tk.Button(root, text='Browse', command=browse_output_directory)
browse_button.grid(row=7, column=1, padx=5, pady=5, sticky='w')

# Console Text
console_text = tk.Text(root, state=tk.DISABLED, width=60, height=10)
console_text.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Download Button
download_button = tk.Button(root, text='Download', command=download, width=10)
download_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

def stop_download():
    root.mainloop()
    update_console(f'⚠️ Download was stopped!', color='orange')
    root.update()

# Stop Button
stop_button = tk.Button(root, text='Stop', command=stop_download, width=10)
stop_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10,)

# Adjust window size
root.columnconfigure(0, weight=1)
root.geometry('500x450')

# Text tag configuration for colors
console_text.tag_config('red', foreground='red')
console_text.tag_config('black', foreground='black')

root.mainloop()

