'''
Discord Command Permission Decorators

This module provides permission checking decorators for Manuel commands. 
'''
import functools

from discord import Interaction
from discord.app_commands import CheckFailure, check

from config import OWNER_ID
from db import role_db

# Exceptions
class NotOWner(CheckFailure):
    '''
    Raised when a non-owner attempts an owner-only command.
    '''
    pass

class NotAdmin(CheckFailure):
    '''
    Raised when a non-owner attempts an owner-only command.
    '''
    pass

class NotUser(CheckFailure):
    '''
    Reserved for future user verification checks.
    '''
    pass


# Owner check -> Local ID
def is_owner():
    '''
    Decorator to verify command invoker is the bot owner.
    
    Checks against the configured OWNER_ID from config
    '''
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            if interaction.user.id == OWNER_ID:
                return await func(self, interaction, *args, **kwargs)
            raise NotOWner('Only the owner can use this command')
        return wrapper
    return decorator

# Admin check


# Admin check
def is_admin():
    '''
    Decorator to verify command invoker is an admin.
    '''
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            if interaction.user.id == OWNER_ID: # Local ID check
                return await func(self, interaction, *args, **kwargs)
            
            role_id = role_db.db_get_role(interaction.guild.id, 'admin')
            if role_id and any(role.id == role_id for role in interaction.user.roles):
                return await func(self, interaction, *args, **kwargs)
            
            raise NotAdmin('Only adm can use this command')
        return wrapper
    return decorator


# User check -> everyone pass - maybe in the future registration or rule acceptance
def is_user():
    '''
    Decorator placeholder for future user verification.
    
    Currently allows all users.
    '''
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            if interaction.user.id == OWNER_ID: # Local ID check
                return await func(self, interaction, *args, **kwargs)
            
            role_id = role_db.db_get_role(interaction.guild.id, 'admin')
            if role_id and any(role.id == role_id for role in interaction.user.roles):
                return await func(self, interaction, *args, **kwargs)            

            return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator
