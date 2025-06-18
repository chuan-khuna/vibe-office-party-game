import discord
import logging
from dotenv import load_dotenv

load_dotenv()

import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscordClient(discord.Client):
    async def on_ready(self):
        logger.info(f'Logged on as {self.user}!')

    # get last image from the channel
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image/'):
                    logger.info(f'Image found: {attachment.url}')
                    # Here you can download the image or process it as needed
                    break
        else:
            logger.info('No images found in the message.')


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    client = DiscordClient(intents=intents)
    client.run(os.environ.get('DISCORD_TOKEN', 'discord-token'))
