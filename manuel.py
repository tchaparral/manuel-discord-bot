import asyncio

import discord
from discord.ext import commands

from config import TOKEN, PREFIX
from logging_config import get_logger
import utils.permissions as up

logger = get_logger(__name__)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = PREFIX, intents = intents)

async def main():
    '''
    Main asynchronous function to start the bot and load extensions.
    '''
    await bot.load_extension('cogs.admin_tools')
    await bot.load_extension('cogs.music')
    await bot.load_extension('cogs.role_manager')
    await bot.start(TOKEN)

@bot.event
async def on_ready():
    '''
    Event handler that triggers when te bot is ready and connected to Discord.
    '''
    logger.info(f'Manuel started as {bot}')
    print('Manuel is online. Check log file to interactions.')

    try:
        synced = await bot.tree.sync()
        logger.info(f'Syncing {len(synced)} (/) commands')
    except Exception as e:
        logger.error(f'Error on syncing slash commands: {e}')

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    '''
    Handle slash command errors including permission violations and unexpected exceptions.
    '''
    if isinstance(error, up.NotOWner):
        logger.warning(f'[PERMISSION] {interaction.user} tried to use OWNER command: {interaction.command.name}')
        await interaction.response.send_message('Forbidden', ephemeral = True)

    elif isinstance(error, up.NotAdmin):
        logger.warning(f'[PERMISSION] {interaction.user} tried to use ADMIN command: {interaction.command.name}')
        await interaction.response.send_message('Forbidden', ephemeral = True)

    elif isinstance(error, discord.app_commands.MissingPermissions):
        logger.warning(f'[DISCORD] {interaction.user} Does not have Discord : {interaction.command.name}')
        await interaction.response.send_message('Forbidden', ephemeral = True)

    else:
        logger.error(f'Unexpected error at {interaction.command.name} by {interaction.user}: {error}')
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message('Unexpected error. Check logs.', ephemeral = True)
            else:
                await interaction.response.send_message('Unexpected error. Check logs.', ephemeral = True)
        except discord.InteractionResponded:
            pass
        
if __name__ == '__main__':
    '''
    Entry point
    '''
    asyncio.run(main())