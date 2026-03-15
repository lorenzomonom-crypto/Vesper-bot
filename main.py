import discord
from discord.ext import commands
from google import genai
import os
import asyncio

# --- CONFIGURATION ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize the NEW Google GenAI Client
client = genai.Client(api_key=GOOGLE_API_KEY)

# Define Vesper's Identity
SYSTEM_PROMPT = "You are Vesper, the witty and loyal Archivist of the Republic. You reside in an office with Venetian walnut furniture and view of the Grand Canal. Keep responses concise but flavorful."

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"--- VESPER ONLINE: NEW ENGINE ACTIVATED ---")
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Don't reply to himself
    if message.author == bot.user:
        return

    # Trigger only in the office or when mentioned
    if message.channel.name == "office-of-vesper" or bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # The New Generation Call
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"{SYSTEM_PROMPT}\n\nUser: {message.content}"
                )
                
                if response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("The archives are silent... (No response generated).")
                    
            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send(f"Archives restricted. Error: {str(e)[:100]}")

    await bot.process_commands(message)

# Run the Bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
