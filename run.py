import argparse
import logging
import os
import sqlite3

import uvloop
import yt_dlp
from decouple import config
from pyrogram import Client

from helpers import process_description, process_title

DB_NAME = 'videos.db'

API_ID = config('API_ID', cast=int)
API_HASH = config('API_HASH')
BOT_TOKEN = config('BOT_TOKEN')


def progress(current, total, video_id):
    logging.info(f"loading {video_id}: {current * 100 / total:.1f}%")


def record_video_to_db(conn, id, title):
    conn.execute("INSERT INTO videos(video_id, title) VALUES(?, ?)",
                 (id, title))
    logging.info(f'Video {id}, {title} has been added')


def fetch_and_notify(app, yt_channel_id, tg_chat_id, folder_path, dry_run,
                     adjust_description=lambda x: x,
                     adjust_title=lambda x: x):
    ydl_opts = {'quiet': True, 'extract_flat': True, 'outtmpl': f'{folder_path}/%(id)s.%(ext)s', 'format': 'mp4'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    video_id TEXT PRIMARY KEY,
                    title TEXT); """)

            result = ydl.extract_info(f'https://www.youtube.com/{yt_channel_id}/videos', download=False)

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
                                video_title_fmt = f"<b>{adjust_title(video['title'])}</b>"
                                video_description_adj = adjust_description(video['description'])
                                video_description_fmt = (
                                    f"\n{video_description_adj}" if video_description_adj else "")

                                logging.info(f'Sending {video_id} to {tg_chat_id}')
                                app.send_video(
                                    chat_id=tg_chat_id,
                                    video=file_path,
                                    caption=video_title_fmt + video_description_fmt,
                                    progress=progress,
                                    progress_args=(video_id,)
                                )
                                logging.info(f'Video {video_id} has been sent')
                                record_video_to_db(conn, video_id, video_title)

                            except Exception as e:
                                logging.error(f'Error occurred while sending video {video_id}: {str(e)}')

                            finally:
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                                    logging.info(f'Video file {file_path} has been removed')
                        else:
                            record_video_to_db(conn, video_id, video_title)


def main(app):
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--yt-channel-id', required=True)
    parser.add_argument('-t', '--tg-chat-id', required=True)
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-l', '--log-level', default='info')
    parser.add_argument('-f', '--folder', default='/tmp', help='Folder path to save videos (default: /tmp)')

    args = parser.parse_args()
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log_level)
    logging.basicConfig(level=numeric_level, format='%(name)s: %(asctime)s - %(levelname)s - %(message)s')

    fetch_and_notify(
        app,
        args.yt_channel_id,
        args.tg_chat_id,
        args.folder,
        args.dry_run,
        adjust_description=process_description,
        adjust_title=process_title)
    logging.info(f"Job finished")


if __name__ == '__main__':
    uvloop.install()
    with Client("teletubby", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
        main(app)
