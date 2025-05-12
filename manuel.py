import asyncio
import discord
from discord.ext import commands
from config import TOKEN, PREFIX

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = PREFIX, intents = intents)

async def main():
    '''
    Main asynchronous function to start the bot and load extensions.
    '''
    await bot.load_extension('cogs.admin_tools')
    await bot.load_extension('cogs.music')
    await bot.start(TOKEN)

@bot.event
async def on_ready():
    '''
    Event handler that triggers when te bot is ready and connected to Discord.
    '''
    print(f'{bot.user} online!')
    try:
        synced = await bot.tree.sync()
        print(f'Syncing {len(synced)} (/) commands')
    except Exception as e:
        print(f'Error on syncing slash commands: {e}')


if __name__ == '__main__':
    '''
    Entry point
    '''
    asyncio.run(main())