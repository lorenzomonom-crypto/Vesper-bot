import discord
from discord.ext import commands
from google import genai
import os

# --- AUTHENTICATION ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Use the most direct client initialization
client = genai.Client(api_key=GOOGLE_API_KEY)

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"--- ARCHIVES RESET: VESPER ONLINE ---")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "office-of-vesper" or bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # We use the absolute most compatible model name
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=message.content
                )
                await message.reply(response.text)
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                await message.channel.send(f"Status: Connection failed. Reason: {str(e)[:100]}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
