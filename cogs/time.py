from discord.ext import commands
import time as sys_time
from .utils.helper import toBase

class Time():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help='Come get your Time now. It\'s fresh!', aliases=['t', 'clk', 'clock'], pass_context=True)
    async def time(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('What time do you want?')

    @time.command(help='Get current unix time', aliases=['u'])
    async def unix(self):
        await self.bot.say(int(sys_time.time()))

    @time.command(help='Leo\'s custom time system', aliases=['t', 'time', 'lt'])
    async def lcts(self):
        t = int(sys_time.time() + sys_time.localtime().tm_gmtoff) % 86400
        
        s_str = ''
        for i in toBase(t % 25, 5):
            s_str += str(i)
        t //= 25

        m_str = ''
        for i in toBase(t % 27, 6):
            m_str += str(i)
        t //= 27

        h_str = hex(t).upper()[2:]

        await self.bot.say(h_str + '-' + m_str+ '-' + s_str)

    @time.command(help='Standard boring time system', aliases=['st', 'standardtime'])
    async def sbts(self):
        await self.bot.say(sys_time.strftime('%H:%M:%S'))

def setup(bot):
    bot.add_cog(Time(bot))
