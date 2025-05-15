'''
Discord Role Managemente Cog.

This module provides role management funcionalities.
'''
import discord
from discord.app_commands import Transformer, Choice
from discord import app_commands, Interaction, Role, Guild
from discord.ext import commands

from db import role_db
from logging_config import get_logger
import utils.permissions as up

logger = get_logger(__name__)

class RoleAutocomplete(Transformer):
    '''
    Transformer for Discord role autocomplete functionality.
    
    Provides both transformation and autocomplete capabilities for role selection
    in slash commands.
    '''
    async def transform(self, interaction: Interaction, value: str) -> Role:
        '''
        Convert role name string to actual Role object.
        '''
        return discord.utils.get(interaction.guild.roles, name = value)
    
    async def autocomplete(self, interaction: Interaction, current: str):
        '''
        Generate autocomplete choices for discord role selection.
        '''
        roles = interaction.guild.roles
        choices = [
            Choice(name = role.name, value = role.name)
            for role in roles if current.lower() in role.name.lower()
        ]
        return choices[:25]

class RoleManager(commands.Cog):
    '''
    Cog for managing Discord role versus Manuel roles permissions and assignments.
    '''
    def __init__(self, bot: commands.Bot):
        '''
        Initialize the RoleManager with bot reference and database setup.
        '''
        self.bot = bot
        role_db.init_db()
    
    # commands    
    @app_commands.command(name = 'role_list', description = 'List roles from server')
    @up.is_user()
    async def role_list(self, interaction: Interaction):
        '''
        List all available roles in the server (except @everyone).
        '''
        roles = interaction.guild.roles[::-1]
        content = '\n'.join([f'- {role.name}' for role in roles if role.name != '@everyone'])
        await interaction.response.send_message(f'Available roles on {interaction.guild.name}:\n{content}', ephemeral = True)

    @app_commands.command(name = 'set_admin', description = 'Set a discord role into admin on Manuel')
    @app_commands.describe(role = 'Choose server role to admin role at Manuel')
    @up.is_owner()
    async def set_admin(
        self,
        interaction: Interaction,
        role: app_commands.Transform[Role, RoleAutocomplete]
    ):
        '''
        Set a role as admin role in the Manuel's permission system.
        '''
        role_db.db_set_role(interaction.guild.id, 'admin', role.id)
        logger.info(f'{role.name}[Discord role] is now admin on Manuel. By: {interaction.user.name}')
        await interaction.response.send_message(f'{role.name} is now admin on Manuel')

    @app_commands.command(name = 'set_user', description = 'Set a discord role into admin on Manuel')
    @app_commands.describe(role = 'Choose server role to admin role at Manuel')
    @up.is_owner()
    async def set_user(
        self,
        interaction: Interaction,
        role: app_commands.Transform[Role, RoleAutocomplete]
    ):
        '''
        Set a role as user role in the Manuel's permission system.
        '''
        role_db.db_set_role(interaction.guild.id, 'user', role.id)
        logger.info(f'{role.name}[Discord role] is now user on Manuel. By: {interaction.user.name}')
        await interaction.response.send_message(f'{role.name} is now user on Manuel')

async def setup(bot: commands.Bot):
    '''
    "Add the RoleManager cog to the bot.
    '''
    await bot.add_cog(RoleManager(bot))

