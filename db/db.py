from .init import get_connection

class RoleDB:
    @staticmethod
    def db_set_role(guild_id: int, role_type: str, role_id: int, discord_name: str):
        '''
        Assign or update a role permission for a guild.
        '''
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                DELETE FROM role_permissions
                WHERE guild_id = ? AND role_id = ?
                ''',
                (guild_id, role_id)
            )
            cursor.execute(
                '''
                INSERT INTO role_permissions (guild_id, role_type, role_id, discord_name)
                VALUES (?, ?, ?, ?)
                ''',
                (guild_id, role_type, role_id, discord_name)
            )
            conn.commit()

    @staticmethod
    def db_get_role(guild_id: int, role_type: str):
        '''
        Retrieve a role ID for specific permission level in a guild.
        '''
        with get_connection() as coon:
            cursor = coon.cursor()
            cursor.execute(
                '''
                SELECT role_id FROM role_permissions
                WHERE guild_id = ? AND role_type = ?
                ''',
                (guild_id, role_type)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        
    @staticmethod
    def db_list_roles(guild_id: int):
        '''
        "List all registered roles for a specific guild.
        '''
        with get_connection() as coon:
            cursor = coon.cursor()
            cursor.execute(
                '''
                SELECT role_type, role_id FROM role_permissions
                WHERE guild_id = ?
                ''',
                (guild_id)
            )
            return cursor.fetchall()
        
class ServerConfigDB:
    @staticmethod
    def set_welcome_channel(guild_id: int, channel_id: int, is_welcome: int, channel_name: str):
        '''
        Set or update the welcome channel for a guild.
        '''
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO server_config (guild_id, welcome_channel_id, is_welcome, channel_name)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET
                    welcome_channel_id = excluded.welcome_channel_id,
                    is_welcome = excluded.is_welcome,
                    channel_name = excluded.channel_name,
                    updated_at = CURRENT_TIMESTAMP
                ''',
                (guild_id, channel_id, 1, channel_name)
            )
            conn.commit()
        
    @staticmethod
    def set_welcome_message(guild_id: int, message: str):
        '''
        Set or update welcome message for a guild.
        '''
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO server_config (guild_id, welcome_message)
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET welcome_message=excluded.welcome_message, updated_at=CURRENT_TIMESTAMP
                ''',
                (guild_id, message)
            )
            conn.commit()

    @staticmethod
    def welcome_config(guild_id: int):
        '''
        Retrieve the welcome channel and message for a guild.
        '''
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT welcome_channel_id, welcome_message
                FROM server_config
                WHERE guild_id = ?
                ''',
                (guild_id,)
            )
            return cursor.fetchall()
    
    @staticmethod
    def get_server_config(guild_id: int) -> dict | None:
        '''
        Search welcome configs for the server
        '''
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT welcome_channel_id, welcome_message, is_welcome
                FROM server_config WHERE guild_id = ?
                ''',
                (guild_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    'welcome_channel_id': row[0],
                    'welcome_message': row[1],
                    'is_welcome': bool(row[2])
                }
            return None
        
    @staticmethod
    def set_welcome_enable(guild_id: int, is_enable: bool):
        '''
        Enable or disable the welcome message feature for a specific guild.
        '''
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO server_config (guild_id, is_welcome)
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET is_welcome = excluded.is_welcome, updated_at = CURRENT_TIMESTAMP
                ''',
                (guild_id, int(is_enable))
            )
            conn.commit()