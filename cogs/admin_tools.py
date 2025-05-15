'''
Admin Tools Cog - Server Management Commands

This module provides administrative commands for Discord server moderation.
'''
from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from config import OWNER_ID
import utils.permissions as up


class AdminTools(commands.Cog):
    '''
    Server administration and moderation commands cog
    '''
    def __init__(self, bot):
        '''
        Initialize the AdminTools cog with bot reference
        '''
        self.bot = bot

    
    @app_commands.command(name = 'shutdown', description = 'Shutdowns Manuel (Owner only)')
    @up.is_owner()
    async def shutdown(self, interaction: discord.Interaction):
        '''
        Shut down the bot (Owner only)
        '''
        await interaction.response.send_message('Shutting Manuel down =/')
        await self.bot.close()

    # Kick member command
    @app_commands.command(name = 'kick', description = 'Kick a member from server')
    @app_commands.describe(member = 'Member to kick', motivo = 'Why to kick him/her?')
    @up.is_admin()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, motivo: str = 'Not informed'):
        '''
        Kick a member from the server
        '''        
        await member.kick(reason = motivo)
        await interaction.response.send_message(f'{member.mention} was kicked by {interaction.user.mention}. Reason: {motivo}')

    # Mute (timeout) member    
    @app_commands.command(name = 'mute', description = 'Timeout a member for determined time')
    @app_commands.describe(member = 'Member to mute', motivo = 'Why to kick him/her/they?', minutos = 'Mute time in minutes')
    @up.is_admin()
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutos: int, motivo: str = 'Not informed'):
        '''
        Timeout (mute) a member for specified duration
        '''
        duration = timedelta(minutes = minutos)
        await member.timeout(duration, reason = motivo)
        await interaction.response.send_message(f'{member.mention} was muted for {minutos} minutes by {interaction.user.mention}. Reason: {motivo}')

    # Unmute (remove timout) member
    @app_commands.command(name = 'unmute', description = 'Unmute (remove timout) user')
    @app_commands.describe(member = 'Member to unmute')
    @up.is_admin()
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        '''
        Remove timeout from muted member
        '''
        duration = None
        await member.timeout(duration)
        await interaction.response.send_message(f'{member.mention} was unmuted.')

    # Purge chat messages
    @app_commands.command(name = 'limpar', description = 'Purge chat messages (100 max)')
    @app_commands.describe(quantidade = 'How many messages to purge?')
    @up.is_admin()
    async def limpar(self, interaction: discord.Interaction, quantidade: int):
        '''
        Bulk delete messages from current channel
        '''        
        if quantidade > 100:
            await interaction.response.send_message('Only 100 messages per time', ephemeral = True)
            return
        
        await interaction.response.defer(ephemeral = True)        
        await interaction.channel.purge(limit = quantidade)
        await interaction.followup.send(f'{quantidade} deleted', ephemeral = True)

    # ban member from the server
    @app_commands.command(name = 'manuel_ban', description = 'Ban a membre from the server')
    @app_commands.describe(member = 'Member to ban', motivo = 'Reason why to ban him/her/they')
    @up.is_admin()
    async def manuel_ban(self, interaction: discord.Interaction, member: discord.Member, motivo: str = 'Not informed.'):
        '''
        Ban a member from the server
        '''
        await member.ban(reason = motivo)
        await interaction.response.send_message(f'{member} was banned banned by {interaction.user.mention}. Reason: {motivo}.')

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminTools(bot))
