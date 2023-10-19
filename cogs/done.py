import sqlite3
from discord.ext import commands

class DoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def done(self, ctx, day: int):
        '''Connect to database and create table if needed'''
        connection = sqlite3.connect("data/log.db")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY, username TEXT, day INTEGER)''')

        '''Pull username from discord command caller'''
        user = ctx.author

        '''Check if day input is between 1 and 100 and is integer'''
        if 1 <= day <= 100:

            '''Check if there is a exsisting user in db table log'''
            cursor.execute("SELECT id FROM log WHERE username = ?", (user.mention,))
            exsisting_user = cursor.fetchone()

            '''If exsisting user is present in log update the day record for user'''
            if exsisting_user:
                cursor.execute("UPDATE log SET day = ? WHERE username = ?", (day, user.mention))
            else:
                '''Otherwise insert new user into log'''
                cursor.execute("INSERT INTO log (username, day) VALUES (?, ?)", (user.mention, day))

            '''Process data into db and close connection to db'''
            connection.commit()
            connection.close()

            '''Return message to server'''
            await ctx.send(f"{user.mention} Completed day {day} milestone recorded")
        else:
            await ctx.send("Please enter a day between 1 and 100")

def setup(bot):
    bot.add_cog(DoneCog(bot))