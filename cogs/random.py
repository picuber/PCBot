from discord.ext import commands
import random

def load_objects():
    with open('cogs/throw_objects.txt') as f:
        return [l.strip() for l in f]

class Random:
    def __init__(self, bot):
        self.bot = bot
        self.objects = load_objects()

    @commands.command(help='Let\'s roll the dices!', aliases=['r'])
    async def roll(self, *, dice_string: str='d'):
        dice_string_clean = ''
        dice_strings_list = []
        dices_list = []
        dices_result = []
        for c in dice_string: #clean string, only leave relevant characters
            if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'd', 'D', '+', '-']:
                if c == 'D':
                    dice_string_clean += 'd'
                elif c == '-':
                    dice_string_clean += '+-'
                else:
                    dice_string_clean += c
        dice_strings_list = dice_string_clean.split('+')
        for d in dice_strings_list:
            if not d == '':
                dices_list.append(d.lower().split('d'))
        for d in dices_list:
            if len(d) > 1:
                if d[0] == '':
                    d[0] = '1'
                if d[1] == '':
                    d[1] = '6'
                for i in range(0, int(d[0])):
                    dices_result.append(random.randint(1, int(d[1])))
            else:
                dices_result.append(int(d[0]))
        roll_sum = 0
        for d in dices_result:
            roll_sum += d
        await self.bot.say(str(dices_result).replace(', ', ' + ') + ' = ' + str(roll_sum))
    
    @roll.error
    async def roll_error(error, ctx):
        await bot.say('Please enter a dice roll')
    
    @commands.command(help='In memmory of RoboNitori', pass_context=True)
    async def throw(self, ctx):
        if ctx.message.mentions == []:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        await self.bot.say('*throws ' + random.choice(self.objects) + ' at* ' + user.mention)

    @commands.command(help='Let me choose for you\nPlease enter your choices seperated by |', aliases=['ch', 'choice'])
    async def choose(self, *, choices: str='Please enter your choices'):
        await self.bot.say(random.choice(choices.split('|')))


def setup(bot):
    bot.add_cog(Random(bot))
