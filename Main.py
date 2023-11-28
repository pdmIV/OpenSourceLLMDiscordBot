import discord
from discord.ext import commands
import requests

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual bot token from the Discord Developer Portal
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Define the API URL and headers
API_URL = "https://api-inference.huggingface.co/models/MBZUAI/LaMini-GPT-1.5B"
HEADERS = {"Authorization": "Bearer API_KEY "}

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.guild_messages = True
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def whoami(ctx):
    await ctx.send("I am SqlaeshBot")
    
@bot.command()
async def ask(ctx, *, question):
    try:
        payload = {
            "inputs": question
        }
        response = query(payload)

        if isinstance(response, list) and len(response) > 0:
            generated_text = response[0].get('generated_text', 'No response found')
            if generated_text == 'No response found':
                generated_text = response[0].get('message', 'No response found')
            await ctx.send(generated_text)
        else:
            await ctx.send("No response found")

    except Exception as exception:
        print(exception)
        await ctx.send("An error occurred during text generation. Please try again later.")

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()
    
# Run the bot
bot.run(TOKEN)
