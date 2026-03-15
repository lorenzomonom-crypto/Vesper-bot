import discord
from discord.ext import commands
from google import genai
import os

# --- AUTHENTICATION ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize the 2026-standard Client with Stable v1 Routing
client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={'api_version': 'v1'}
)

# Vesper's Core Identity
SYSTEM_PROMPT = "You are Vesper, the witty and loyal Archivist of the Republic. You reside in an office with Venetian walnut furniture and view of the Grand Canal. Keep responses concise but flavorful."

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"--- ARCHIVES REBORN: VESPER ONLINE ---")
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Prevent self-replying
    if message.author == bot.user:
        return

    # Trigger only in the office or when mentioned
    if message.channel.name == "office-of-vesper" or bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # USING THE UNIVERSAL STABLE MODEL TO KILL THE 404
                response = client.models.generate_content(
                    model='gemini-1.0-pro',
                    contents=f"{SYSTEM_PROMPT}\n\nUser: {message.content}"
                )
                
                if response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("The archives are silent... (No text generated).")
                    
            except Exception as e:
                print(f"Deployment Error: {e}")
                # Shows a snippet of the error in Discord for debugging
                await message.channel.send(f"Archives restricted. Error: {str(e)[:100]}")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
