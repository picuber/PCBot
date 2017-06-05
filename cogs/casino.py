from discord.ext import commands
from cogs.utils.checks import is_owner
import json

def load_casino():
    with open('cogs/casino.json') as f:
            return json.load(f)

def store_casino(db):
    with open('cogs/casino.json', 'w') as f:
        json.dump(db, f)

class Casino:
    def __init__(self, bot):
        self.bot = bot
        self._db = load_casino()

    @commands.group(help='Can you win the jackpot?', aliases=['cas'], pass_context=True)
    async def casino(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('How can I help you?')

    @casino.group(help='Check your credit card :credit_card:', aliases=['bal', 'b'], pass_context=True)
    async def balance(self, ctx):
        if ctx.invoked_subcommand is None or ctx.invoked_subcommand.name == 'balance':
            user = ctx.message.author
            if not user.id in list(self._db['bank'].keys()):
                self._db['bank'][user.id] = 0
                store_casino(self._db)
            await self.bot.say(user.mention + '\'s balance: ' + str(self._db['bank'][user.id]) + ':dollar:')

    @balance.command(hidden=True, aliases=['s'], pass_context=True)
    @is_owner()
    async def set(self, ctx, new_balance: int):
        if ctx.message.mentions == []:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        self._db['bank'][user.id] = new_balance
        store_casino(self._db)
        await self.bot.say(user.mention + ' your balance has been set to ' + str(self._db['bank'][user.id]) + ':dollar:')
        
    @balance.command(hidden=True, aliases=['a'], pass_context=True)
    @is_owner()
    async def add(self, ctx, new_balance: int):
        if ctx.message.mentions == []:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        self._db['bank'][user.id] += new_balance
        store_casino(self._db)
        await self.bot.say(str(new_balance) + ':dollar: has been added to ' + user.mention + '\'s balance')

    # @casino.group(help='Let\'s play Balack Jack!', aliases=['bj', 'blackj', 'bjack'], pass_context=True)
    # async def blackjack(ctx):
    #     if ctx.invoked_subcommand.name == 'blackjack':
    #         await bot.say('Welcome to the Black Jack Table! How can I help you?')

    # @blackjack.command(pass_context=True)
    # async def test(ctx):
    #     pass
    # async def join(cxt):
    #     pass
    # async def start(ctx):
    #     pass
    # async def setpot(ctx):
    #     pass
    # @owner_only
    # async def kick(ctx):
    #     pass
    # async def hit(ctx):
    #     pass
    # async def stand(ctx):
    #     pass

def setup(bot):
    bot.add_cog(Casino(bot))
