from discord.ext import commands
from cogs.utils.checks import *
import json
import os
import random as r

def load_casino():
    if not os.path.isfile('cogs/casino.json'):
        return {}
    else:
        with open('cogs/casino.json') as f:
            return json.load(f)

def store_casino(db):
    with open('cogs/casino.json', 'w') as f:
        json.dump(db, f)

class CasinoDB:
    def __init__(self):
        self._db = load_casino()

    def reload(self):
        self._db = load_casino()

    def is_registered(self, uid):
        return uid in self._db

    def register(self, uid):
        """returns True if newly registered"""
        if not self.is_registered(uid):
            self._db[uid] = {}
            self._db[uid]['balance'] = 100
            self._db[uid]['bet'] = 5
            store_casino(self._db)
            return True
        else:
            return False

    def restore_user_integrity(self, uid):
        if self._db[uid]['balance'] < 0:
            self._db[uid]['balance'] = 0
        if self._db[uid]['bet'] < 0:
            self._db[uid]['bet'] = 0
        if self._db[uid]['balance'] == 0 and self._db[uid]['bet'] >= 1:
            self._db[uid]['bet'] = 1
        elif self._db[uid]['balance'] < self._db[uid]['bet']:
            self._db[uid]['bet'] = self._db[uid]['balance']
        store_casino(self._db)

    def set_bal(self, uid, balance):
        self.register(uid)
        self._db[uid]['balance'] = balance
        self.restore_user_integrity(uid)

    def add_bal(self, uid, balance):
        self.register(uid)
        self._db[uid]['balance'] += balance
        self.restore_user_integrity(uid)

    def sub_bal(self, uid, balance):
        self.register(uid)
        self._db[uid]['balance'] -= balance
        self.restore_user_integrity(uid)

    def get_bal(self, uid):
        self.register(uid)
        return self._db[uid]['balance']

    def set_bet(self, uid, bet):
        self.register(uid)
        self._db[uid]['bet'] = bet
        self.restore_user_integrity(uid)

    def get_bet(self, uid):
        self.register(uid)
        return self._db[uid]['bet']

    def lose_bet(self, uid):
        self.sub_bal(uid, self.get_bet(uid))

    def win_bet(self, uid):
        self.add_bal(uid, self.get_bet(uid))

class Casino:
    def __init__(self, bot):
        self.bot = bot
        self._cdb = CasinoDB()

    @commands.group(help='Can you win the jackpot?', aliases=['cas'], pass_context=True)
    async def casino(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('How can I help you?')

    @casino.command(help='So, you wanna gamble?', aliases=['reg'], pass_context=True)
    async def register(self, ctx):
        if ctx.message.mentions == []:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        if self._cdb.register(user.id):
            await self.bot.say('You have now been registered {}'.format(user.mention))
        else:
            await self.bot.say('You are already registered {}'.format(user.mention))

    @casino.command(help='Rrrreeeelllooaaaaddddd1!!!one!!eleven!', hidden=True)
    @is_owner()
    async def reload(self):
        self._cdb.reload()
        await self.bot.say('Reloaded...')

    @casino.group(help='Check your credit card :credit_card:', aliases=['bal'], pass_context=True)
    async def balance(self, ctx):
        if ctx.invoked_subcommand is None or ctx.invoked_subcommand.name == 'balance':
            if ctx.message.mentions == []:
                user = ctx.message.author
            else:
                user = ctx.message.mentions[0]
            await self.bot.say('{}\'s balance: {}:dollar:'.format(user.mention, self._cdb.get_bal(user.id)))

    @balance.command(hidden=True, aliases=['s'], pass_context=True)
    @is_owner()
    async def set(self, ctx, new_balance: int):
        if ctx.message.mentions == []:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        self._cdb.set_bal(user.id, new_balance)
        await self.bot.say('{} your balance has been set to {}:dollar:'.format(user.mention, self._cdb.get_bal(user.id)))
        
    @balance.command(hidden=True, aliases=['a'], pass_context=True)
    @is_owner()
    async def add(self, ctx, new_balance: int):
        if ctx.message.mentions == []:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        self._cdb.add_bal(user.id, new_balance)
        await self.bot.say('{}:dollar: has been added to {}\'s balance'.format(new_balance, user.mention))

    @casino.group(help='What are you willing to bet?', pass_context=True)
    async def bet(self, ctx):
        if ctx.invoked_subcommand is None or ctx.invoked_subcommand.name == 'bet':
            if ctx.message.mentions == []:
                user = ctx.message.author
            else:
                user = ctx.message.mentions[0]
            await self.bot.say('Your current bet is {}:dollar: {}'.format(self._cdb.get_bet(user.id), user.mention))

    @bet.command(name='set', help='Change your bet', aliases=['s'], pass_context=True)
    async def set_bet(self, ctx, bet:int=5):
        if is_owner()(ctx):
            if ctx.message.mentions == []:
                user = ctx.message.author
            else:
                user = ctx.message.mentions[0]
        else:
            user = ctx.message.author
        self._cdb.set_bet(user.id, bet)
        await self.bot.say('Your bet has been set to {}:dollar: {}'.format(self._cdb.get_bet(user.id), user.mention))

    rps_conditions = {#(choice1, choice2) : choice1 wins?
            ('r', 'p') : False,
            ('r', 's') : True,
            ('p', 'r') : True,
            ('p', 's') : False,
            ('s', 'r') : False,
            ('s', 'p') : True
        }
    @casino.command(help='Can you win against me?', aliases=['rps', 'rockspaperscissors', 'rockpaperandscissors', 'rockspaperandscissors'], pass_context=True)
    async def rockpaperscissors(self, ctx, your_choice):
        your_choice = your_choice.lower()[:1]
        if your_choice not in  ('r', 'p', 's'):
            await self.bot.say('This is a ***serious*** game! Choose out of R/rock P/paper S/scissors')
            return
        user = ctx.message.author
        bot_choice = r.choice([('r', 'rock'), ('p', 'paper'), ('s', 'scissors')])
        if bot_choice[0] == your_choice:
            await self.bot.say('I had {}! We\'re tied {}!'.format(bot_choice[1], user.mention))
        elif not self.rps_conditions[(bot_choice[0], your_choice)]:
            self._cdb.win_bet(user.id)
            await self.bot.say('I had {}! You won {}:dollar: {}'.format(bot_choice[1], self._cdb.get_bet(user.id), user.mention))
        else:
            self._cdb.lose_bet(user.id)
            await self.bot.say('I had {}! You lost {}:dollar: {}'.format(bot_choice[1], self._cdb.get_bet(user.id), user.mention))

def setup(bot):
    bot.add_cog(Casino(bot))
