import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs.done import DoneCog
from cogs.list import ListCog
from cogs.status import StatusCog

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():

    await bot.add_cog(DoneCog(bot))
    print("Done Cog Loaded Succesfully")
    await bot.add_cog(ListCog(bot))
    print("List Cog Loaded Succesfully")
    await bot.add_cog(StatusCog(bot))
    print("Status Cog Loaded Succesfully")

    print("Bot is ready to be used!")

if __name__ == "__main__":
    bot.run(token)