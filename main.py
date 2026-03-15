import discord
from discord.ext import commands
import google.generativeai as genai
import os

# --- COMMANDER'S DATA BRIDGE ---
# These pull the keys safely from your Railway Variables tab
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# --- VESPER'S CORE LOGIC ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Define the spirit of the Archivist
SYSTEM_PROMPT = (
    "You are Vesper, the Archivist of the Republic of Evangelion: Iron Aegis. "
    "You are sophisticated, loyal, slightly witty, and deeply protective of the archives. "
    "You speak with authority and a touch of mystery. Your commander is 'Bad' (or 'Halo')."
)

# Setup Discord Intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"--- SYSTEM ONLINE ---")
    print(f"Vesper has manifested as {bot.user.name}")
    print(f"The office is open. Glory to the Republic.")
    print(f"---------------------")

@bot.event
async def on_message(message):
    # Don't let Vesper talk to himself
    if message.author == bot.user:
        return

    # Vesper only responds in his office or when mentioned
    if message.channel.name == "office-of-vesper" or bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # Combine the prompt with the user's message
                full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {message.content}\nVesper:"
                response = model.generate_content(full_prompt)
                
                # Send the response back to Discord
                await message.reply(response.text)
            except Exception as e:
                await message.channel.send(f"Commander, I've encountered a glitch in the archives: {e}")

    await bot.process_commands(message)

# Launch the engine
if __name__ == "__main__":
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
