'''
Music Cog Module for Discord Bot

This module implements a Discord bot music system with YouTube integration.
'''
import asyncio
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands

import utils.permissions as up
from utils.utils import clear_temp_folder
from utils.yt_downloader import download_youtube_audio, cleanup


ROOT_DIR = Path(__file__).resolve().parent.parent
TEMP_SONG_PATH = ROOT_DIR / 'temp' / 'song_request'

class Music(commands.Cog):
    ''' A cog for handling music playback functionality in Discord voice channels.

    This cog allows users with permissions to request Youtube songs to played in their
    voice channel, manage music queues, and handles audio playback usin FFmpeg.
    '''
    def __init__(self, bot):
        '''
        Initialize the Music cog with bot references and empty queues.
        '''
        self.bot = bot
        self.queues = {}
        self.now_playing = {}
        self.queue_mirrors = {}
        self.skip_autoplay = {}

    # overall handle functions
    async def queue_manager(self, guild: discord.Guild, voice_client: discord.VoiceClient):
        '''
        Process the song queue and play the next available track
        '''
        self.skip_autoplay[guild.id] = False

        while not self.skip_autoplay[guild.id]:

            while not self.queues[guild.id].empty():
                filepath = await self.queues[guild.id].get()
                self.now_playing[guild.id] = filepath
                audio_source = discord.FFmpegPCMAudio(filepath)
                voice_client.play(audio_source)

                while True:
                    if not voice_client.is_playing() and not voice_client.is_paused():
                        break
                    await asyncio.sleep(1)

                cleanup(filepath)
                if len(self.queue_mirrors[guild.id]) > 0:
                    self.queue_mirrors[guild.id].pop(0)

        clear_temp_folder(TEMP_SONG_PATH)
        return

    async def music_check(self, interaction: discord.Interaction) \
        -> tuple[bool, discord.VoiceClient | None]:
        '''
        Checks if user is on a voice channel and if Manuel is there too.
        '''
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            await interaction.response.send_message('This only works on voice channels.', ephemeral = True)
            return False, None        
        
        voice_client = interaction.guild.voice_client

        if voice_client is None or not voice_client.is_connected():
            await interaction.response.send_message('Manuel is not playing anything anywhere. Call "Song Request"', ephemeral = True)
            return False, None
        
        if voice_client.channel != interaction.user.voice.channel:
            if voice_client.is_playing() or voice_client.is_paused():
                await interaction.response.send_message('Dj Manuel is playing in another chat', ephemeral = True)
                return False, None
    
        return True, voice_client
    
    async def queue_check(self, interaction: discord.Interaction):
        '''
        Check if queue is empty before pause, resume, skip, etc.
        '''
        voice_client = interaction.guild.voice_client

        if not voice_client.is_playing() and not voice_client.is_paused():
            await interaction.response.send_message('Nothing playing right now', ephemeral = True)
            return False
        
        return True
        
    # commands
    @app_commands.command(name = 'song_request', description = 'Plays a youtube audio with a link')
    @app_commands.describe(url = 'Link from Youtube Video')
    @up.is_user()
    async def song_request(self, interaction: discord.Interaction, url: str):
        '''Handles song requests from users in voice channels.'''
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            await interaction.response.send_message('This only works on voice channels.', ephemeral = True)
            return

        guild_id = interaction.guild.id
        voice_client = interaction.guild.voice_client
        voice_channel = interaction.user.voice.channel        
        
        if voice_client is None or not voice_client.is_connected():
            try:
                voice_client = await voice_channel.connect()
            except Exception as e:
                await interaction.response.send_message(f'Connection error: {e}')
                return

        elif voice_client.channel != interaction.user.voice.channel:
            if voice_client.is_connected() and not voice_client.is_paused() and not voice_client.is_playing():
                try:
                    await voice_client.disconnect()
                    voice_client = await voice_channel.connect()
                except Exception as e:
                    await interaction.response.send_message(f'Connection error: {e}')
                    return
            else:    
                await interaction.response.send_message('Dj Manuel is playing in another chat', ephemeral = True)
                return
      
        await interaction.response.send_message('Inserting song on queue', ephemeral = True)
        try:            
            filepath = download_youtube_audio(url)

            if guild_id not in self.queues:
                self.queues[guild_id] = asyncio.Queue()
                self.queue_mirrors[guild_id] = []

            queue = self.queues[guild_id]
            mirror = self.queue_mirrors[guild_id]

            await queue.put(filepath)
            mirror.append(filepath)

            if not voice_client.is_playing():
                await self.queue_manager(interaction.guild, voice_client)                                    
            
            else:
                position = len(mirror)
                await interaction.followup.send(f'Song added to the queue at position {position}', ephemeral = True)

        except Exception as e:
            await interaction.followup.send(f'Play error: {e}', ephemeral = True)
    
    @app_commands.command(name = 'skip', description = 'Skip the currently playing song')
    @up.is_admin()
    async def skip(self, interaction: discord.Interaction):
        '''
        Skips the currently playing song and plays the next one in the queue, if available.
        '''
        check, voice_client = await self.music_check(interaction)
        if not check:
            return
        
        queue_check = await self.queue_check(interaction)
        if not queue_check:
            return
              
        voice_client.stop()
        await interaction.response.send_message(f'Song skipped by {interaction.user.mention}')

        # removing temp file
        filepath = self.now_playing.get(interaction.guild.id)
        if filepath:
            cleanup(filepath)
            self.now_playing[interaction.guild.id] = None
    
    @app_commands.command(name = 'clear', description = 'Stops song request and clear the queue')
    @up.is_admin()
    async def clear(self, interaction: discord.Interaction):
        '''
        Stops the current playback and clears the queue for the server/cle  .
        '''
        check, voice_client = await self.music_check(interaction)
        if not check:
            return

        queue_check = await self.queue_check(interaction)
        if not queue_check:
            return
        
        guild_id = interaction.guild.id

        if guild_id in self.queues:
            self.queues[guild_id] = asyncio.Queue()
            self.queue_mirrors[guild_id] = []
        
        self.skip_autoplay[guild_id] = True
        voice_client.stop()       
        await interaction.response.send_message(f'Playback stopped and queue cleared by {interaction.user.mention}.')
    
    @app_commands.command(name = 'pause', description = 'Pause song request current music')
    @up.is_user()
    async def pause(self, interaction: discord.Interaction):
        '''
        Pause song request current music.
        '''        
        check, voice_client = await self.music_check(interaction)
        if not check:
            return
        
        queue_check = await self.queue_check(interaction)
        if not queue_check:
            return
        
        if voice_client.is_paused():
            return await interaction.response.send_message('Already paused')
        
        voice_client.pause()
        await interaction.response.send_message(f'Song request paused by {interaction.user.mention}')
    
    @app_commands.command(name = 'resume', description = 'Resume song request paused music')
    @up.is_user()
    async def resume(self, interaction: discord.Interaction):
        '''
        Resume song request paused music
        '''
        check, voice_client = await self.music_check(interaction)
        if not check:
            return
        
        queue_check = await self.queue_check(interaction)
        if not queue_check:
            return      

        voice_client.resume()
        await interaction.response.send_message(f'Song request resumed by {interaction.user.mention}')

async def setup(bot: commands.Bot):
    '''
    Add the music cog to the bot.
    '''
    await bot.add_cog(Music(bot))
