import os
import openai
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('DISCORD_CHANNEL')
openai.api_key = os.getenv("OPENAI_API_KEY")

class MyClient(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_sent = False
        self.last_sent_at = None

    async def on_ready(self):
        channel = self.get_channel(CHANNEL)
        await self.timer.start(channel)

    @tasks.loop(seconds=5)
    async def timer(self, channel):
        
        date = datetime.now()
        weekday = date.weekday()

        if weekday == 4 and date.hour == 15 and date.minute == 0:
            delta = None
            if self.last_sent_at is not None:
                delta = date - self.last_sent_at
            if delta is None or delta.seconds > 60 :
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt="Write a fun easy creative personal opinion question about A.I., generative art, or synthetic media that realted to the current date",
                    max_tokens=256,
                    temperature=0.5,
                    n = 10,
                    presence_penalty = 2.0)
                    
                qotw = response["choices"][0]["text"].strip()

                self.last_sent_at = datetime.now()
                await channel.send(qotw)

intents = discord.Intents.all()
intents.message_content = True
client = MyClient(intents=intents, command_prefix='!')

client.run(TOKEN)
