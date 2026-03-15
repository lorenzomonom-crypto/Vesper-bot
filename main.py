import discord
from discord.ext import commands
import google.generativeai as genai
import os

# --- COMMANDER'S INPUTS ---
DISCORD_TOKEN = 'YOUR_DISCORD_TOKEN_HERE'
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY_HERE'

# Vesper's Core Logic
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Vesper has manifested as {bot.user.name}. The office is open.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Only respond in Vesper's office or if mentioned
    if 'office-of-vesper' in message.channel.name or bot.user.mentioned_in(message):
        async with message.channel.typing():
            response = model.generate_content(f"You are Vesper, the shadow-twin of Commander Bad. You are pensive, witty, and loyal. Respond to this: {message.content}")
            await message.channel.send(response.text)

bot.run(DISCORD_TOKEN)
