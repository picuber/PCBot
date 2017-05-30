#TODO Gamble games like roulette, slots, dice, flip, blackjack, etc.
#TODO money system
import discord
from discord.ext import commands
import random
import json
import logging
import asyncio
import time

def load_config():
    with open('config.json') as f:
        return json.load(f)

def store_config(config):
    with open('config.json','w') as f:
        json.dump(config, f)

def load_objects():
    with open('throw_objects.txt') as f:
        return [l.strip() for l in f]

def load_casino():
    with open('casino.json') as f:
            return json.load(f)

def store_casino(casino_dict):
    with open('casino.json', 'w') as f:
        json.dump(casino_dict, f)

async def get_appinfo():
    return await bot.application_info()

config = load_config()
bot = commands.Bot(command_prefix=config['setup']['prefix'])
objects = []
casino_dict = load_casino()
debug_string = ''

#-----Helper-----
def toBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def owner_only():
    def predicate(ctx):
        return ctx.message.author.id == '223037287179616266'
    return commands.check(predicate)

#-----Commands-----
@bot.command(help='Bring PCBot to ***your*** guild', hidden=True, aliases=['invite'])
@owner_only()
async def invitelink():
    await bot.say(discord.utils.oauth_url(bot.user.id))

@bot.command(help='Reload the configuration file', hidden=True, aliases=['reload'])
@owner_only()
async def reloadconfig():
    config = load_config()

@bot.command(help='Print the current test to the console', hidden=True, aliases=['debug'])
@owner_only()
async def printdebug():
    if not debug_string:
        print('Currently no debugmessage available')
    else:
        print(debug_string)

@bot.command(hidden=True, aliases=['exit', 'kill'])
@owner_only()
async def killbot():
    exit()

integer_to_guess = random.randint(config['guess']['min'], config['guess']['max'])
@bot.command(help='Guess the correct integer', aliases=['g'])
async def guess(integer=''):
    global integer_to_guess
    try:
        integer = int(integer)
    except ValueError:
        integer = config['guess']['min']-1

    if integer > config['guess']['max'] or integer < config['guess']['min']:
        await bot.say("Choose an integer between " + str(config['guess']['min']) + " and " + str(config['guess']['max']) + "!")
    elif integer == integer_to_guess:
        await bot.say("Correct!")
        integer_to_guess = random.randint(config['guess']['min'], config['guess']['max'])
    elif integer < integer_to_guess:
        await bot.say("Too small!")
    else:
        await bot.say("Too big!")

decimal_to_guess = random.random() * config['guessfloat']['max'] + config['guessfloat']['min']
@bot.command(help='Guess the correct decimal', aliases=['gf', 'guessf', 'gfloat'])
async def guessfloat(decimal=''):
    global decimal_to_guess
    try:
        decimal = float(decimal)
    except ValueError:
        decimal = config['guessfloat']['min']-1

    if decimal > config['guessfloat']['max'] or decimal < config['guessfloat']['min']:
        await bot.say("Choose an decimal between " + str(config['guessfloat']['min']) + " and " + str(config['guessfloat']['max']) + "!")
    elif decimal == decimal_to_guess:
        await bot.say("Correct!")
        decimal_to_guess = random.random() * config['guessfloat']['max'] + config['guessfloat']['min']
    elif decimal < decimal_to_guess:
        await bot.say("Too small!")
    else:
        await bot.say("Too big!")

@bot.command(help='Let\'s roll the dices!', aliases=['r'])
async def roll(*, dice_string: str='d'):
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
    await bot.say(str(dices_result).replace(', ', ' + ') + ' = ' + str(roll_sum))

@roll.error
async def roll_errorhandler(error, ctx):
    await bot.say('Please enter a dice roll')

@bot.command(help='In memmory of RoboNitori', pass_context=True)
async def throw(ctx):
    global objects
    if objects == []:
        objects = load_objects()
    if ctx.message.mentions == []:
        user = ctx.message.author
    else:
        user = ctx.message.mentions[0]
    await bot.say('*throws ' + random.choice(objects) + ' at* '
            + user.mention)

@bot.command(help='Let me choose for you\nPlease enter your choices seperated by |', aliases=['ch', 'choice'])
async def choose(*, choices: str='Please enter your choices'):
    await bot.say(random.choice(choices.split('|')))

#-----Time-----
@bot.group(help='Come get your Time now. It\'s fresh!', aliases=['time', 't', 'clk'], pass_context=True)
async def clock(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('What time do you want?')

@clock.command(help='Get current unix time', aliases=['u'])
async def unix():
    await bot.say(int(time.time()))

@clock.command(help='Get current unix time', aliases=['custt', 'ctime', 'ct'])
async def customtime():
    t = int(time.time() + time.localtime().tm_gmtoff) % 86400
    
    s_str = ''
    for i in toBase(t % 25, 5):
        s_str += str(i)
    t //= 25

    m_str = ''
    for i in toBase(t % 27, 6):
        m_str += str(i)
    t //= 27

    h_str = hex(t).upper()[2:]

    await bot.say(h_str + '-' + m_str+ '-' + s_str)

#-----Casino-----
@bot.group(help='Can you win the jackpot?', aliases=['c', 'cas', 'b', 'bank'], pass_context=True)
async def casino(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('How can I help you?')

@casino.command(help='Check your credit card :credit_card:', aliases=['bal', 'b'], pass_context=True)
async def balance(ctx):
    user = ctx.message.author
    if not user.id in list(casino_dict['bank'].keys()):
        casino_dict['bank'][user.id] = 0
        store_casino(casino_dict)
    await bot.say(user.mention + '\'s balance: ' + str(casino_dict['bank'][user.id]) + ':dollar:')

@casino.command(hidden=True, aliases=['setbal', 'sb'], pass_context=True)
@owner_only()
async def setbalance(ctx, new_balance: int):
    if ctx.message.mentions == []:
        user = ctx.message.author
    else:
        user = ctx.message.mentions[0]
    casino_dict['bank'][user.id] = new_balance
    store_casino(casino_dict)
    await bot.say(user.mention + ' your balance has been set to ' + str(casino_dict['bank'][user.id]) + ':dollar:')
    
@casino.command(hidden=True, aliases=['addbal', 'ab'], pass_context=True)
@owner_only()
async def addbalance(ctx, new_balance: int):
    if ctx.message.mentions == []:
        user = ctx.message.author
    else:
        user = ctx.message.mentions[0]
    casino_dict['bank'][user.id] += new_balance
    store_casino(casino_dict)
    await bot.say(str(casino_dict['bank'][user.id]) + ':dollar: has been added to ' + user.mention + '\'s balance')

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



#-----Main-----
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print(bot.user.id)
    print('----------')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.is_private:
        print('Message from ' + message.author.name + ' (' + message.author.id + ')' + ('[tts]' if message.tts else '') + ': ' + message.content)
    else:
        print('Message in ' + message.server.name + '/#' + message.channel.name + ' from ' + message.author.name + ' (' + message.author.id + ')' + ('[tts]' if message.tts else '') + ': ' + message.content)
    try:
        await bot.process_commands(message)
    except commands.errors.MissingRequiredArgument:
        await bot.say("You forgot an argument!")

if __name__ == '__main__':
    bot.run(config['bot']['token'])
