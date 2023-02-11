import openai
import telebot
from config import YOUR_TBOT_TOKEN, YOUR_OAPI_KEY

# Initialize the ChatGPT and DALL-E models
openai.api_key = YOUR_OAPI_KEY
model_engine = "text-davinci-003"

# Create a TeleBot instance
bot = telebot.TeleBot(YOUR_TBOT_TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """
                    <b>Xin chào!</b> Tôi là siêu trí tuệ <b>ChatGPT</b> tôi giúp gì cho bạn! (Hỏi ít thôi kẻo hết tiền thằng duchu)""", parse_mode='html')
    
@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
        if "help" in message.text.lower():
            bot.send_message(message.chat.id, """
Here are the Available command(s)
<b>1: /Start to start the bot</b>
<b>2: /help to get this help text again</b>
<b>3: /generate_image to generate image based on the description you provided</b>\n                        
<i>Note: This bot is still in beta phase and is available for free only for testing purposes.</i>\n
<pre>This bot is created by</pre>\n<b>Arbind Singh</b>
<b>You can Follow me on</b>\n<a href='https://github.com/habitual69'>Github</a>""",parse_mode='html')
            
        # Check if the user is requesting an image
        elif "generate_image" in message.text.lower():
            # Use the DALL-E model to generate an image
            image_url = openai.Image.create(
            prompt=f"{message.text}",
            size="1024x1024",
            n=1,
            response_format="url"
            ).data[0].url
            bot.send_photo(message.chat.id, image_url)
        else:
        # Use the ChatGPT model to generate a response
            response = openai.Completion.create(
            engine=model_engine,
            prompt=f"User: {message.text}\nBot: ",
            max_tokens=3000,
            n=1,
            temperature=0.7,
            ).choices[0].text

            # If the response is too long, send the remaining part as next message
            if len(response) > 4096:
                bot.send_message(message.chat.id, response[:4096] + '...')
                bot.send_message(message.chat.id, response[4096:])
            else:
                # Send the generated response to the user
                bot.send_message(message.chat.id, response)
def run_bot():
    try:
        # Start the bot
        bot.polling(none_stop=True, timeout=123)
    except Exception as e:
        # If the bot crashes, print the error message and start the bot again
        print(e)
        run_bot()

# Run the bot indefinitely
while True:
    run_bot()
