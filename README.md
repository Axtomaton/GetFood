# PREREQUISITES

## Please install the follow libraries 
You can do so with `pip install <name of library>`. Alternatively you can use `pip -r install requirements.txt`

Python (>3.7)
Beautifulsoup4
Requests
tabulate
discord

# How to run the CLI
run `python getmyfood.py --BotToken=<Enter Bot Token> --ChannelID=<Enter Channel ID>`
- You can get the BotToken by signing up at `https://discord.com/developers/applications`, this is the private key for your bot.
- Channel ID is the ID for the text channel that you want the bot to send the message to. This is obtained by enabling developer mode
in the discord settings and right clicking your desired channel.

# How to run the CLI Online/ Acknowledges
- You can run this via AWS EC2, GCP Computer Engine, etc. I've tried that EC2 works quite well with tmux. 
- If you want to have it send the message through SMS instead of through Discord, you can simply modify the script to run through
a third-party API. I've tried working with smtplib but that method seems to be obsolete, however, you can try with AWS SNS and calling it via boto3. 