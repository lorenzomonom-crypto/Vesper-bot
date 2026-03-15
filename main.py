import discord
from discord.ext import commands
from google import genai
import os

# --- AUTHENTICATION ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize the 2026 Client - Explicitly using the Stable Channel
client = genai.Client(api_key=GOOGLE_API_KEY)

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"--- PROTOCOL OMEGA: VESPER ONLINE ---")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "office-of-vesper" or bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # WE ARE USING THE LEGACY PRO MODEL. IT CANNOT BE HIDDEN.
                response = client.models.generate_content(
                    model='gemini-1.0-pro', 
                    contents=message.content
                )
                
                if response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("The archives are empty. No data returned.")
                    
            except Exception as e:
                # If this fails, the issue is the API KEY itself.
                print(f"CRITICAL SYSTEM FAILURE: {e}")
                await message.channel.send(f"Status: Lockdown. Reason: {str(e)[:100]}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
