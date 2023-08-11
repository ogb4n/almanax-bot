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
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Starting..."))
    try:
        synced = await bot.tree.sync()
        if synced:
            print('Slash commands synced')
        else:
            print('Slash commands not synced')
    except Exception as e:
        print(f'Error while syncing slash commands: {e}')
    almanax_retrieve.start()


@tasks.loop(hours=15)
async def almanax_retrieve():
        await bot.wait_until_ready()
        channel = bot.get_channel(int(CHANNEL_ID)) # The channel id that we want the bot to send message
        print('Background task started')
        print('------')
        while not bot.is_closed():
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
            imgkit.from_url('http://www.krosmoz.com/fr/almanax', img_path, options=img_options)

            # Send image to Discord
            print('Send a new Almanax day')
            file = discord.File(img_path)
            await channel.send(file=file)

            # Delete img file
            os.remove(img_path)

@bot.tree.command(name='almanax',description="Vois l'offrande et le bonus du jour")
async def almanax(interaction: discord.Interaction):
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
        await channel.send(file=file)

        # Delete img file
        os.remove(img_path)


if __name__ == '__main__':
    print('Bot is starting')
    bot.run(TOKEN)