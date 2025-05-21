'''

'''
import discord
from discord import app_commands, Interaction, TextChannel
from discord.app_commands import Transformer, Choice
from discord.ext import commands
from discord.ui import View, Select

from db import ServerConfigDB
from logs import get_logger
import utils.permissions as up


logger = get_logger(__name__)

class ChannelAutocomplete(Transformer):
    '''
    
    '''
    async def transform(self, interaction: Interaction, value: str) -> TextChannel:
        '''
        Convert channel name string to actual Channel object
        '''
        return discord.utils.get(interaction.guild.text_channels, name = value)
    
    async def autocomplete(self, interaction: Interaction, current: str):
        '''
        Generate autocomplete choices for discord welcome channel.
        '''
        channels = interaction.guild.text_channels
        choices = [
            Choice(name = channel.name, value = channel.name)
            for channel in channels if current.lower() in channel.name.lower()
        ]
        return choices
    
class ToogleSelect(Select):
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        options = [
            discord.SelectOption(label = 'Enable', description = 'Enable welcome message on server'),
            discord.SelectOption(label = 'Disable', description = 'Disable welcome message on server'),
        ]
        super().__init__(placeholder = "Choose...", options = options)

    async def callback(self, interaction: Interaction):
        choice = self.values[0]
        new_value = True if choice == 'Enable' else False

        ServerConfigDB.set_welcome_enable(self.guild_id, new_value)
        logger.info(f'Welcome message from {interaction.guild.name} is now {"enableb" if new_value else "disableb"}')
        await interaction.response.send_message(f'Welcome messages is now {"enableb" if new_value else "disableb"}', ephemeral = True)

class ToogleWelcomeView(View):
    '''
    A Discord UI View for toggling welcome message settings via dropdown menu.
    '''
    def __init__(self, guild_id: int):
        '''
        Initialize the welcome message toggle view.
        '''
        super().__init__(timeout = 60)
        self.guild_id = guild_id

        self.add_item(ToogleSelect(guild_id))

class ServerConfig(commands.Cog):
    '''
    Server Configuration Cog - manages guild-specific bot settings.
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = 'set_welcome_channel', description = 'Sets text channel to sendo welcome message')
    @app_commands.describe(channel = 'Select a text channel')
    @up.is_admin()
    async def set_welcome_channel(
        self, 
        interaction: Interaction,
        channel: app_commands.Transform[TextChannel, ChannelAutocomplete]
    ):
        '''
        Set welcome channel from server text channels.
        '''
        ServerConfigDB.set_welcome_channel(interaction.guild.id, channel.id, 1, channel.name)
        logger.info(f'{channel.name} setted to welcome channel by {interaction.user.name}')
        await interaction.response.send_message(f'{channel.name} is now the welcome channel from {interaction.guild.name}', ephemeral = True)

    @app_commands.command(name = 'set_welcome_message', description = 'Set the welcome message on welcome channel')
    @app_commands.describe(message = 'Write the welcome message')
    @up.is_admin()
    async def set_welcome_message(
        self,
        interaction: Interaction,
        message: str
    ):
        '''
        Set welcome message on welcome channel.
        '''
        try:
            ServerConfigDB.set_welcome_message(interaction.guild.id, message)
            logger.info(f'{message} is now the welcome message. Setted by: {interaction.user.name}')
            await interaction.response.send_message(f'"{message}" is the new welcome message', ephemeral = True)
        
        except Exception as e:
            logger.error(f'{e}')
    
    @app_commands.command(name = 'toogle_welcome', description = 'Enable or disable welcome message')
    @up.is_admin()
    async def toogle_welcome(self, interaction: Interaction):
        '''
         Toggle welcome messages for the server (admin-only command).
        '''
        view = ToogleWelcomeView(guild_id = interaction.guild.id)
        await interaction.response.send_message(
            'Choose enable or disable welcome message:',
            view = view,
            ephemeral = True
        )

    @app_commands.command(name = 'preview_welcome', description = 'Preview currently welcome message.')
    @up.is_admin()
    async def preview_welcome(self, interaction: Interaction):
        '''
        Preview welcome message if it exists.
        '''
        guild = interaction.guild
        member = interaction.user
        config = ServerConfigDB.get_server_config(guild.id)

        if not config or not config.get('welcome_channel_id'):
            await interaction.response.send_message('No welcome messages')
            return
        
        welcome_message = config.get('welcome_message') or 'Welcome, {user} to {server}!'
        rendered_message = welcome_message.replace("{user}", member.mention).replace("{server}", guild.name)

        await interaction.response.send_message(f'Welcome preview message:\n{rendered_message}', ephemeral = True)

    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        '''
        Listener to log and send welcome message when a member joins the guild.
        '''
        logger.info(
            f'[JOIN] {"bot" if member.bot else "user"}: {member.name}#{member.discriminator}'
            f'ID: {member.id} joined "{member.guild.name}" (ID: {member.guild.id})'
        )

        guild_id = member.guild.id
        config = ServerConfigDB.get_server_config(guild_id)

        if not config:
            return # Server config return None
        
        if not config['is_welcome']:
            return # Welcome messages disabled
        
        channel_id = config.get('welcome_channel_id')
        welcome_message = config.get('welcome_message') or "Welcome, {user}"

        if not channel_id:
            return # No channel for welcome message
        
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return # If welcome channel was deleted
        
        message = welcome_message.format(
            user = member.mention,
            server = member.guild.name
        )
        
        try:
            await channel.send(message)
            logger.info(f'Welcome message sent at {channel.name}')

        except discord.Forbidden:
            logger.warning(f'No discord permission to send messages at {channel.name}')
        
        except Exception as e:
            logger.warning(f'Error sending welcome message at {channel.name}')

async def setup(bot: commands.Bot):
    '''
    Add the ServerConfig cog to the bot
    '''
    await bot.add_cog(ServerConfig(bot))
