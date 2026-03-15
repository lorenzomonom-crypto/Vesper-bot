import discord
from discord.ext import commands
from google import genai
import os

# --- AUTHENTICATION ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# FORCE the API version to v1 (Stable) to bypass the 404 lockout
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
    print(f"--- PROTOCOL OMEGA: VESPER ONLINE ---")
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
                # Using the absolute model path to clear the 'not found' error
                response = client.models.generate_content(
                    model='models/gemini-1.5-flash',
                    contents=f"{SYSTEM_PROMPT}\n\nUser: {message.content}"
                )
                
                if response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("The archives are silent... (No text generated).")
                    
            except Exception as e:
                # Detailed error reporting for the final check
                print(f"CRITICAL SYSTEM FAILURE: {e}")
                await message.channel.send(f"Status: Lockdown. Reason: {str(e)[:100]}")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
