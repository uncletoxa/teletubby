import logging
import os
import sqlite3
import argparse
import yt_dlp
from subprocess import run, PIPE

DB_NAME = 'videos.db'


def fetch_and_notify(channel_id, folder_path, dry_run):
    ydl_opts = {'quiet': True, 'extract_flat': True, 'outtmpl': f'{folder_path}/%(id)s.%(ext)s', 'format': 'mp4'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    video_id TEXT PRIMARY KEY,
                    title TEXT); """)

            result = ydl.extract_info(f'https://www.youtube.com/{channel_id}/videos', download=False)

            if 'entries' in result:
                for video in result['entries']:
                    video_id = video['id']
                    video_title = video['title']

                    cur.execute("SELECT 1 FROM videos WHERE video_id = ?", (video_id,))
                    exists = cur.fetchone()

                    if not exists:
                        video_url = f"https://www.youtube.com/watch?v={video_id}"

                        if not dry_run:
                            ydl.download((video_url,))

                            file_path = f'{folder_path}/{video_id}.mp4'

                            try:
                                video_title_fmt = f"<b>{video['title']}</b>"
                                video_description_fmt = f"\n{video['description']}" if video['description'] else ''

                                response = run([
                                        "telegram-send",
                                        "--video", file_path,
                                        "--caption", video_title_fmt + video_description_fmt,
                                        "--format", "html",
                                        "--showids"],
                                    text=True, stdout=PIPE, stderr=PIPE)

                                if response.returncode != 0:
                                    raise RuntimeError(
                                        f'Video has not been send:\n{response.stdout}')
                            finally:
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                                    logging.info(f'Video file {file_path} has been removed')

                            conn.execute("INSERT INTO videos(video_id, title) VALUES(?, ?)", (video_id, video_title))
                            logging.info(f'Video {video_id}, {video_title} has been added')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channel-id', required=True)
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-f', '--folder', default='/tmp', help='Folder path to save videos (default: /tmp)')

    args = parser.parse_args()

    fetch_and_notify(args.channel_id, args.folder, args.dry_run)
    logging.info(f"Job finished")
