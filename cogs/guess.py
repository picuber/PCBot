from discord.ext import commands
import random
import json
import os

def load():
    if not os.path.isfile('cogs/guess.json'):
        guess = {'integer': {'min': 0, 'max': 99}, 'float': {'min': 0, 'max': 10}}
        store(guess)
    with open('cogs/guess.json') as f:
        return json.load(f)

def store(config):
    with open('cogs/guess.json','w') as f:
        json.dump(config, f)

class Guess(commands.Cog):
    def reload_numbers(self):
        config = load()
        self.int_min = config['integer']['min']
        self.int_max = config['integer']['max']
        self.f_min = config['float']['min']
        self.f_max = config['float']['max']

    def __init__(self, bot):
        self.bot = bot
        self.reload_numbers()
        self.integer_to_guess = self.new_int()
        self.decimal_to_guess = self.new_decimal()

    def new_int(self):
        return random.randint(self.int_min, self.int_max)

    def new_decimal(self):
        return random.random() * self.f_max + self.f_min
    
    @commands.group(help='Do you know what I want?', aliases=['g'], pass_context=True)
    async def guess(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Welcome to the unknown. Guess your way!')

    @guess.command(hidden=True, help='reload the numbers', aliases=['r', 'rld'])
    async def reload(self):
        self.reload_numbers()
        await self.bot.say('Fresh numbers coming right in!')

    @guess.command(help='Guess the correct integer', aliases=['i', 'int'])
    async def integer(self, *, guess:int=-1):
        if guess > self.int_max or guess < self.int_min:
            await self.bot.say("Choose an integer between " + str(self.int_min) + " and " + str(self.int_max) + "!")
        elif guess == self.integer_to_guess:
            await self.bot.say("Correct!")
            integer_to_guess = random.randint(self.int_min, self.int_max)
        elif guess < self.integer_to_guess:
            await self.bot.say("Too small!")
        else:
            await self.bot.say("Too big!")

    @integer.error
    async def integer_error(self, error, ctx):
        await self.bot.say("Choose an integer between " + str(self.int_min) + " and " + str(self.int_max) + "!")


    @guess.command(help='Guess the correct decimal', aliases=['f'])
    async def float(self, decimal:float=-1):
        if decimal > self.f_max or decimal < self.f_min:
            await self.bot.say("Choose an decimal between " + str(self.f_min) + " and " + str(self.f_max) + "!")
        elif decimal == self.decimal_to_guess:
            await self.bot.say("Correct!")
            self.decimal_to_guess = random.random() * self.f_max + self.f_min
        elif decimal < self.decimal_to_guess:
            await self.bot.say("Too small!")
        else:
            await self.bot.say("Too big!")

    @float.error
    async def float_error(self, error, ctx):
        await self.bot.say("Choose an decimal between " + str(self.f_min) + " and " + str(self.f_max) + "!")
        
def setup(bot):
    bot.add_cog(Guess(bot))
