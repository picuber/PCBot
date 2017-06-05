from discord.ext import commands
from cogs.utils.checks import is_owner

class Core:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Bring PCBot to ***your*** guild', hidden=True, aliases=['invite'])
    @is_owner()
    async def invitelink(self):
        await self.bot.say(discord.utils.oauth_url(self.bot.user.id))

    @commands.command(hidden=True, aliases=['exit', 'kill'])
    @is_owner()
    async def killbot(self):
        print('Killing PCBot...')
        await self.bot.say('Good bye cruel world!')
        exit()

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def do(self, ctx, times : int, *, command):
        """Repeats a command a specified number of times."""
        msg = ctx.message
        msg.content = command
        for i in range(times):
            await self.bot.process_commands(msg)

    @commands.command(help='Pong')
    async def ping(self):
        await self.bot.say('Pong')

def setup(bot):
    bot.add_cog(Core(bot))
