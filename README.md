Chap GPT 3.5 Telegram Bot for group admins

# Setup
1. Fill the config.py
2. Push it on fly.io ot create your own docker container

## deploying to https://fly.io
- Install flyctl <code>brew install flyctl</code>
- Sign Up <code>flyctl auth signup</code>
= Launch app <code>flyctl launch</code>
- After first deploy downgrade instance count to 1 to avoid conflicts <code>flyctl scale count 1</code>
- Feel free to chat with bot

##Features
1. This bot works for groups/supergroups only, you can't chat with the bot "one on one"
2. This bot interacts with group adimins only
