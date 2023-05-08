# -*- coding: utf-8 -*-
import config
import logging
import logging.handlers

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import TextStartsFilter
from telebot.asyncio_filters import IsReplyFilter

import openai
from tools.count_tokens import num_tokens_from_messages

# logging initialize
filename = 'app.log'
logger = logging.getLogger(f'{config.bot_username}')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.handlers.RotatingFileHandler(filename, maxBytes=3000000, backupCount=1)
handler.setFormatter(formatter)
logger.addHandler(handler)

emotions = config.emotions
system_prompt_text = config.system_prompt_text
chatgpt_api_error_text = config.chatgpt_api_error_text

system_prompt = {"role": "system", "content": f'{system_prompt_text}'}
max_tokens = config.max_tokens
max_tokens_summariztion = config.max_tokens_summariztion


openai.api_key = config.api_key
all_messages = {} 

async def askgpt(message,userid):
    logger.info(f'Request from {userid}, message text: {message}')
    
    _temp_prompt = []
    _temp_sum_prompt = []
    sub_prompt = {"role": "user", "content": f'{message} {emotions}'}
    
    try:
        summarized_prompt = all_messages[userid]
        logger.info(f'Known user {userid}. Data from memory: {summarized_prompt}')
        
        _temp_prompt = summarized_prompt.copy()
        _temp_prompt.insert(0,system_prompt)
        _temp_prompt.append(sub_prompt)
            
    except KeyError:
        all_messages[userid] = []
        logger.info(f'New user {userid}. Create memory')
        _temp_prompt = [system_prompt,sub_prompt]
    
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=_temp_prompt,
        max_tokens = max_tokens,
        temperature = 0.4, # from 0 to 2
        presence_penalty = 0.5,
        frequency_penalty = 0.4
        )
        
        ai_answer = response['choices'][0]['message']['content']
        logger.info(f'GPT responce: {ai_answer}')

        _temp_sum_prompt = all_messages[userid]
        logger.info(f'Get memory: {_temp_sum_prompt}')
        
        _temp_sum_prompt.append(sub_prompt)
        _temp_sum_prompt.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        # token control
        tokens = num_tokens_from_messages(_temp_sum_prompt)
        logger.info(f'Max tokens in memory exceeded {max_tokens_summariztion}. Tokens in memory: {tokens}')

        while num_tokens_from_messages(_temp_sum_prompt) > max_tokens_summariztion:
            logger.info(f'Max tokens in memory exceeded {max_tokens_summariztion}. Cutting memory')
            _temp_sum_prompt = _temp_sum_prompt[2:]

        all_messages[userid] = _temp_sum_prompt
        logger.info(f'Save to memory: {_temp_sum_prompt}')


        return response['choices'][0]['message']['content']
    
    except:
        return chatgpt_api_error_text



bot_token = config.bot_token
bot_username = config.bot_username
bot = AsyncTeleBot(bot_token)

'''
Reply handler
Bot is suitable for groups only
'''
@bot.message_handler(func=lambda message: True, content_types=['text'], chat_types=['supergroup','group'], text_startswith=f'@{bot_username}')
async def process_messages(message):
    txt = message.text
    txt = txt.replace(f'@{bot_username}','')
    
    is_user_admin = await bot.get_chat_member(message.chat.id,message.from_user.id)
    if is_user_admin.status in ('administrator','creator'): # admin message only
        try:
            await bot.send_chat_action(message.chat.id, 'typing')
            txt = str(message.reply_to_message.text) + str(txt) # reply from another user with bot mention
            answer = await askgpt(txt,message.from_user.id)
            await bot.reply_to(message,answer)
        except:
            await bot.send_chat_action(message.chat.id, 'typing') # bot mention
            answer = await askgpt(txt,message.from_user.id)
            await bot.reply_to(message,answer)

'''
Reply handler
'''
@bot.message_handler(content_types=['text'], chat_types=['supergroup','group'], is_reply=True)
async def process_messages2(message):
    txt = message.text
    if message.reply_to_message.from_user.username == bot_username:
        is_user_admin = await bot.get_chat_member(message.chat.id,message.from_user.id) # admin message only
        if is_user_admin.status in ('administrator','creator'):
            await bot.send_chat_action(message.chat.id, 'typing')
            answer = await askgpt(txt,message.from_user.id)
            await bot.reply_to(message,answer)
            
        


bot.add_custom_filter(IsReplyFilter())
bot.add_custom_filter(TextStartsFilter())

import asyncio
while True:
    try:
        asyncio.run(bot.polling())
    except KeyboardInterrupt:
        exit()
    except:
        continue
