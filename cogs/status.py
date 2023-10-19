import sqlite3
from discord.ext import commands

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx):

        '''Connect to database and create table if needed'''
        connection = sqlite3.connect("data/log.db")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY, username TEXT, day INTEGER)''')

        '''Pull username from discord command caller'''
        user = ctx.author

        '''Check if there is a exsisting user in db table log'''
        cursor.execute("SELECT id FROM log WHERE username = ?", (user.mention,))
        exsisting_user = cursor.fetchone()

        '''If exsisting user is present fetch day from db and return to user'''
        if exsisting_user:
            cursor.execute("SELECT day FROM log WHERE username = ?", (user.mention,))
            logged_day = cursor.fetchone()
            day = logged_day[0] + 1
            await ctx.send(f"{user.mention} is on day {day}") 
        else:
            '''Tells the user that they dont have a log'''
            await ctx.send(f"{user.mention} you haven't started a log")

        '''Process data into db and close connection to db'''
        connection.commit()
        connection.close()   
        
def setup(bot):
    bot.add_cog(StatusCog(bot))