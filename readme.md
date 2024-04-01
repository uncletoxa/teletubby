# TeleTubby

TeleTubby is a telegram bot that allows you to repost videos from a specific YouTube channel to a Telegram channel. It uses the `yt_dlp` library to fetch video information and download the videos, and the `telegram-send` command-line tool to send the videos to the Telegram channel.

## Usage

Once the TeleTubby is deployed and the cron job is set up, it will automatically fetch new videos from the specified YouTube channel and repost them to the Telegram channel. The video information will be stored in the SQLite database to avoid duplicate reposts.

You can customize the folder path where the videos are saved by using the `-f` or `--folder` flag when running the script. For example:
```bash
python run.py -c CHANNEL_ID -f /path/to/video/folder
```

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- Python 3.10+
- Spare [Telegram bot](https://core.telegram.org/bots#how-do-i-create-a-bot)

## Deployment

To deploy the TeleTubby, follow these steps:

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

6. Configure the `telegram-send` tool by following the instructions provided in its [documentation](https://github.com/rahiel/telegram-send?tab=readme-ov-file#installation):
   ```bash
   telegram-send --configure
   ```

7. Perform a dry run to populate the database with existing videos on the YouTube channel:
   ```bash
   python run.py -c CHANNEL_ID --dry-run
   ```
   Replace `CHANNEL_ID` with the ID of the YouTube channel you want to repost videos from.

8. Set up a cron job to run the script periodically. Create a bash script with the following content:
   ```bash
   #!/usr/bin/env bash

   set -e

   cd "$HOME/teletubby/"  # path to the folder with the project
   source .venv/bin/activate
   python run.py -c CHANNEL_ID -f /path/to/video/folder
   ```
   Replace `CHANNEL_ID` with the ID of the YouTube channel you want to repost videos from, and `/path/to/video/folder` with the desired folder path where the videos will be saved (default is `/tmp`).

   Make the bash script executable:
   ```bash
   chmod +x script.sh
   ```

   Add the script to your crontab to run it periodically, for example, every 30 minutes:
   ```
   */30 * * * * /path/to/script.sh
   ```

## Fair Usage and Legal Considerations

Please note that reposting videos from YouTube to Telegram may be subject to copyright restrictions and may not always be legal. While reposting videos for personal or educational purposes is generally tolerated, it is important to respect the rights of content creators and abide by YouTube's terms of service.

When using TeleTubby, consider the following guidelines:

* Only repost videos from channels that you have the necessary permissions or licenses for.
* Provide proper attribution to the original content creators.
* If a content creator requests the removal of their video from your Telegram channel, promptly comply with their request.
* Be mindful of the frequency and volume of videos being reposted to avoid excessive or abusive usage of the bot.

It is the responsibility of the user to ensure that their use of TeleTubby complies with applicable laws and regulations. The developers of TeleTubby shall not be held liable for any misuse or illegal activities conducted using this tool.