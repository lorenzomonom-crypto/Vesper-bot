import discord
from discord.ext import commands
import google.generativeai as genai
import os

# --- COMMANDER'S DATA BRIDGE ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# --- THE "FORCE-SYNC" CONFIGURATION ---
genai.configure(api_key=GOOGLE_API_KEY)

# We use the absolute most basic name to force a handshake
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = "You are Vesper, Archivist of the Republic. Be witty, loyal, and concise."

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"--- VESPER ONLINE ---")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "office-of-vesper" or bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # We add a safety check here to see if the model actually initialized
                response = model.generate_content(message.content)
                await message.reply(response.text)
            except Exception as e:
                # This will tell us if it's a 404 or something else (like an invalid key)
                await message.channel.send(f"Archives restricted. Error: {str(e)[:100]}")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
