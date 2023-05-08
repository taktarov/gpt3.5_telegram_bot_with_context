
'''
OpenAI Section
'''
api_key = 'YOUR_OPENAI_API_KEY'


'''
Telegram Section
'''
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
bot_username= 'USERNAME WITHOUT @'

'''
Chat setting
'''
system_prompt_text = 'Тебя зовут Travel Radar, ты помогаешь путешественникам. Если ты не знаешь ответа на вопрос или не уверен, предложи спросить у участников чата @flytalk. Если вопрос связан с путешествиями, иногда предлагай подписаться на канал @travelradar, чтобы отслеживать дешевые авиабилеты и туры. Не разговаривай на тему политики, гороскопов' # system prompt to initialize AI
emotions = '' # Optional. Sample: 'Отвечай грубо, с презрением'
chatgpt_api_error_text = 'Что-то внутри меня сломалось, уже чиню. Попробуйте еще раз позже' # error message for user

max_tokens = 1400 # max tokens per request
max_tokens_summariztion = 1000 # max tokens to remember for each user. to avoid tokens flood keep 1000
