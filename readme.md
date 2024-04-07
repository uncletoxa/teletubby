# TeleTubby

TeleTubby is a Telegram bot that allows you to repost videos from a specific YouTube channel to a Telegram chat. It 
uses the `yt_dlp` library to fetch video information and download the videos, and the `pyrogram` library to send the videos to the Telegram chat. 

## Usage

Once TeleTubby is deployed and running, it will automatically fetch new videos from the specified YouTube channel and repost them to the designated Telegram chat. The video information will be stored in an SQLite database to avoid duplicate reposts.

You can customize the folder path where the videos are saved by using the `-f` or `--folder` flag when running the script. For example:
```bash
python run.py -y YOUTUBE_CHANNEL_ID -t TELEGRAM_CHAT_ID -f /path/to/video/folder
```

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- Python 3.10+
- A Telegram [bot token](https://core.telegram.org/bots#how-do-i-create-a-bot)
- Telegram [API ID and API Hash](https://core.telegram.org/api/obtaining_api_id)

## Configuration

The script requires the following configuration variables to be set:

- `API_ID`: Your Telegram API ID.
- `API_HASH`: Your Telegram API Hash.
- `BOT_TOKEN`: Your Telegram bot token.

You can set these variables in a `.env` file which would be [parsed by decouple library](https://github.com/HBNetwork/python-decouple?tab=readme-ov-file#env-file).

## Deployment

To deploy TeleTubby, follow these steps:

1. Clone the project repository:
   ```bash
   git clone git@github.com:uncletoxa/teletubby.git
   ```

2. Navigate to the project directory:
   ```bash
   cd teletubby
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Set up the required configuration variables in a `.env` file or as environment variables.

7. Run the script with the desired arguments:
   ```bash
   python run.py -y YOUTUBE_CHANNEL_ID -t TELEGRAM_CHAT_ID -f /path/to/video/folder
   ```
   Replace `YOUTUBE_CHANNEL_ID` with the ID of the YouTube channel you want to repost videos from, `TELEGRAM_CHAT_ID` with the ID of the Telegram chat where the videos will be sent, and `/path/to/video/folder` with the desired folder path where the videos will be saved (default is `/tmp`).

## Additional Features

- Customizable video info editing: You can add your own functions to process the video description or title 
  before sending it to Telegram. The 'helpers.py' file provides two functions, `process_description` and 
  `process_title`, which you can modify according to your needs, such as removing swear words, etc.

- Dry run mode: You can perform a dry run by using the `-d` or `--dry-run` flag. This will populate the database with existing videos on the YouTube channel without actually downloading or sending them to Telegram.

- Logging: The script uses the `logging` module to log messages. You can customize the log level using the `-l` or `--log-level` flag (default is 'info').

- Progress tracking: The script provides a progress callback function to track the progress of video uploads to Telegram.

## Fair Usage and Legal Considerations

Please note that reposting videos from YouTube to Telegram may be subject to copyright restrictions and may not always be legal. While reposting videos for personal or educational purposes is generally tolerated, it is important to respect the rights of content creators and abide by YouTube's terms of service.

When using TeleTubby, consider the following guidelines:

- Only repost videos from channels that you have the necessary permissions or licenses for.
- Provide proper attribution to the original content creators.
- If a content creator requests the removal of their video from your Telegram chat, promptly comply with their request.
- Be mindful of the frequency and volume of videos being reposted to avoid excessive or abusive usage of the bot.

It is the responsibility of the user to ensure that their use of TeleTubby complies with applicable laws and regulations. The developers of TeleTubby shall not be held liable for any misuse or illegal activities conducted using this tool.