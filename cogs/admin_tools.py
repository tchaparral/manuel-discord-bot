import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class AdminTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick member command
    @app_commands.command(name = 'kick', description = 'Kick a member from server')
    @app_commands.describe(membro = 'Member to kick', motivo = 'Why to kick him/her?')
    async def kick(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = 'Not informed'):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message('You are not allowed to kick members', ephemeral = True)
            return
        
        await membro.kick(reason = motivo)
        await interaction.response.send_message(f'{membro.mention} was kicked by {interaction.user.mention}. Reason: {motivo}')

    # Mute (timeout) member
    @app_commands.command(name = 'mute', description = 'Timeout a member for determined time')
    @app_commands.describe(membro = 'Member to mute', motivo = 'Why to kick him/her/they?', minutos = 'Mute time in minutes')
    async def mute(self, interaction: discord.Interaction, membro: discord.Member, minutos: int, motivo: str = 'Not informed'):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message('You are not allowed to mute members', ephemeral = True)
            return
        
        duration = timedelta(minutes = minutos)
        await membro.timeout(duration, reason = motivo)
        await interaction.response.send_message(f'{membro.mention} was muted for {minutos} minutes by {interaction.user.mention}. Reason: {motivo}')

    # Unmute (remove timout) member
    @app_commands.command(name = 'unmute', description = 'Unmute (remove timout) user')
    @app_commands.describe(membro = 'Member to unmute')
    async def unmute(self, interaction: discord.Interaction, membro: discord.Member):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response('You are not allowed to unmute anyone.')
            return
        
        duration = None
        await membro.timeout(duration)
        await interaction.response.send_message(f'{membro.mention} was unmuted.')

    # Purge chat messages
    @app_commands.command(name = 'limpar', description = 'Purge chat messages (100 max)')
    @app_commands.describe(quantidade = 'How many messages to purge?')
    async def limpar(self, interaction: discord.Interaction, quantidade: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message('You are not allowed to purge chat messages', ephemeral = True)
            return
        
        elif quantidade > 100:
            await interaction.response.send_message('Only 100 messages per time', ephemeral = True)
            return
        
        await interaction.channel.purge(limit = quantidade)
        await interaction.response.send_message(f'{quantidade} deleted', ephemeral = True)

    # ban member from the server
    @app_commands.command(name = 'manuel_ban', description = 'Ban a membre from the server')
    @app_commands.describe(membro = 'Member to ban', motivo = 'Reason why to ban him/her/they')
    async def manuel_ban(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = 'Motivo não informado'):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message('You are not allowed to ban anyone.')
            return
        
        await membro.ban(reason = motivo)
        await interaction.response.send_message(f'{membro} was banned banned by {interaction.user.mention}. Reason: {motivo}.')

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminTools(bot))
