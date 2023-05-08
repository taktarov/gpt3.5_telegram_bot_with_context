Chap GPT 3.5 Telegram Bot for group admins

Setup
1. Fill the config.py
2. Push it on fly.io ot create your own docker container

# deploying to https://fly.io
brew install flyctl
flyctl auth signup
flyctl launch
flyctl deploy

# after first deploy downgrade instance count to 1 to avoid conflicts
flyctl scale count 1

3. Fell free to chat with bot

Features
1. This bot works in group only, you can't chat with the bot one on one
2. This bot interacts with group adimins only