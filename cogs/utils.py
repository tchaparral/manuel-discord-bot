'''
Utility Commands Module

This module provides various utility commands for the Discord bot
'''
from datetime import timezone

import discord
from discord import app_commands
from discord.ext import commands

from logs import get_logger
import utils.permissions as up

logger = get_logger(__name__)

class Utils(commands.Cog):
    '''
    Utility Cog - Provides informational and utility commands
    '''
    def __init__(self, bot):
        '''
        Initialize the Utils cog with bot reference
        '''
        self.bot = bot

    @app_commands.command(name = 'userinfo', description = "Show user's info")
    @up.is_user()
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        '''
         Display comprehensive information about a server member.
        '''
        member = member or interaction.user

        roles = [role.mention for role in member.roles if role.name != '@everyone']
        joined_at = member.joined_at.astimezone(timezone.utc).strftime('%d %b %Y, %H:%M UTC') if member.joined_at else 'Unknown'
        created_at = member.created_at.astimezone(timezone.utc).strftime('%d %b %Y, %H:%M UTC')

        embed = discord.Embed(title = f"{member.display_name}'s Info", color = discord.Color.blue())
        embed.set_thumbnail(url = member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name = 'User', value = f'{member} (`{member.id}`)', inline = False)
        embed.add_field(name = 'Account created at', value = created_at, inline = True)
        embed.add_field(name = 'Joined server at', value = joined_at, inline = True)
        embed.add_field(name = 'Roles', value = ', '.join(roles) if roles else 'None', inline = False)
        
        await interaction.response.send_message(embed = embed, ephemeral = True)
    
    @app_commands.command(name = 'serverinfo', description = "Show server's info")
    @up.is_user()
    async def serverinfo(self, interaction: discord.Interaction):
        '''
        Display detailed information about the current server.
        '''
        guild = interaction.guild
        created_at = guild.created_at.astimezone(timezone.utc).strftime('%d %b %Y, %H:%M UTC')
        text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
        voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])

        embed = discord.Embed(title = f"{guild.name}'s Info", color = discord.Color.blue())
        embed.set_thumbnail(url = guild.icon.url if guild.icon else discord.Embed.Empty)
        embed.add_field(name = 'Name', value = guild.name, inline = True)
        embed.add_field(name = 'ID', value = guild.id, inline = True)
        embed.add_field(name = 'Owner', value = guild.owner.mention, inline = True)
        embed.add_field(name = 'Created at', value = created_at, inline = True)
        embed.add_field(name = 'Members', value = guild.member_count, inline = True)
        embed.add_field(name = 'Text Channels', value = text_channels, inline = True)
        embed.add_field(name = 'Voice Channels', value = voice_channels, inline = True)
        embed.add_field(name = 'Total Roles', value = len(guild.roles) - 1, inline = True)

        await interaction.response.send_message(embed = embed, ephemeral = True)

    @app_commands.command(name = 'say', description = 'Send a message as Manuel')
    @app_commands.describe(message = 'Message you want to Manuel send for you')
    @up.is_admin()
    async def say(self, interaction: discord.Interaction, message: str):
        '''
        Send a message through the bot (Admin only)
        '''
        await interaction.response.send_message(f'> {message}')

async def setup(bot: commands.Bot):
    '''
    Add the Utils cog to the bot
    '''
    await bot.add_cog(Utils(bot))

