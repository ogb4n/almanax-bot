import os
import asyncio
from discord.ext import commands, tasks
from discord import app_commands
import discord
from dotenv import load_dotenv
import imgkit
from datetime import timedelta, datetime, date


load_dotenv()
CHANNEL_ID = os.getenv('CHANNEL_ID')
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready', bot.user)
    try:
        synced = await bot.tree.sync()
        if synced:
            print('Slash commands synced')
        else:
            print('Slash commands not synced')
    except Exception as e:
        print(f'Error while syncing slash commands: {e}')
    # almanax_retrieve.start()

async def almanax(interaction: discord.Interaction):
        await interaction.response.defer()
        channel = bot.get_channel(int(CHANNEL_ID)) # The channel id that we want the bot to send message

        img_options = {
        'format': 'jpg',
        'encoding': "UTF-8",
        'crop-w': '455',
        'crop-h': '250',
        'crop-x': '250',
        'crop-y': '455',
        'user-style-sheet': 'hide.css'
        }
        img_path = f'almanax-{date.today().strftime("%d-%m-%Y")}.jpg'
        imgkit.from_url(f'http://www.krosmoz.com/fr/almanax', img_path, options=img_options)

        # Send image to Discord
        print('Send a new Almanax day')
        file = discord.File(img_path)
        await interaction.followup.send("Voici l'Almanax du jour 👌✨:", file=file)

        # Delete img file
        os.remove(img_path)

@tasks.loop(hours=15)
async def almanax_loop():
        await almanax()

@bot.tree.command(name='almanax',description="Vois l'offrande et le bonus du jour")
    await almanax()


if __name__ == '__main__':
    print('Bot is starting')
    bot.run(TOKEN)