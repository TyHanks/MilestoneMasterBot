import sqlite3
from discord.ext import commands

class ListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def list(self, ctx):
        
        '''Connect to database and create table if needed'''
        connection = sqlite3.connect("data/log.db")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY, username TEXT, day INTEGER)''')

        '''Pull usernames from database'''
        cursor.execute("SELECT username FROM log")
        usernames = cursor.fetchall()

        '''Pull day from database'''
        cursor.execute("SELECT day FROM log")
        days = cursor.fetchall()

        for username_tuple, day_tuple in zip(usernames, days):
            i = len(username_tuple) - 1
            j = len(day_tuple) - 1
            while i >= 0 and j >= 0:
                username = username_tuple[i]
                day = day_tuple[j]
                await ctx.send(f"{username} Completed - {day} days    Left to complete - {100 - day} days     Percentage complete - {day}%")
                i -= 1
                j -= 1

        '''Process data into db and close connection to db'''
        connection.commit()
        connection.close()

def setup(bot):
    bot.add_cog(ListCog(bot))