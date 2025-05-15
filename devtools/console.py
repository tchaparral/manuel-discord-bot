import asyncio
import nest_asyncio
from IPython import embed

def start_terminal(bot_instance, music_instance):
    loop = asyncio.new_event_loop()
    asyncio.get_event_loop()
    nest_asyncio.apply(loop)

    namespace = {
        'bot': bot_instance,
        'music': music_instance,
        'loop': loop,
     }

    banner = 'Terminal!'

    embed(user_ns = namespace, banner1 = banner)


    ####### DEVELOPING ###########