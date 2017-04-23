import discord
from discord.ext import commands
import random
import json
import logging
import asyncio

def load_config():
    with open('config.json') as f:
        return json.load(f)

def store_config(config):
    with open('config.json','w') as f:
        json.dump(config, f)

config = load_config()
bot = commands.Bot(command_prefix=config['setup']['prefix'])

#-----Helper-----
def caller_is_bot_owner():
    def predicate(ctx):
        #TODO 
        print(str(bot.AppInfo.owner.id))
        print(str(ctx.message.author.id))
        return discord.AppInfo.owner == ctx.message.author
    return commands.check(predicate)
#-----Commands-----
@bot.command(hidden=True)
@caller_is_bot_owner()
async def invitelink():
    await bot.say('https://discordapp.com/api/oauth2/authorize?client_id=' + bot.user.id + '&scope=bot&permissions=0')

@bot.command(hidden=True)
@caller_is_bot_owner()
async def reloadconfig():
    config = load_config()

number_to_guess = random.randint(config['guess']['min'], config['guess']['max'])
@bot.command(help='Guess the correct number', aliases=['g'])
async def guess(number=''):
    global number_to_guess
    try:
        int(number)
    except ValueError:
        number = config['guess']['min']-1

    if number > config['guess']['max'] or number < config['guess']['min']:
        await bot.say("Choose a number between " + str(config['guess']['min']) + " and " + str(config['guess']['max']) + "!")
    elif number == number_to_guess:
        await bot.say("Correct!")
        number_to_guess = random.randint(config['guess']['min'], config['guess']['max'])
    elif number < number_to_guess:
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
    print('Message from ' + message.author.name + ' (' + message.author.id + '): ' + message.content)
    try:
        await bot.process_commands(message)
    except MissingRequiredArgument:
        await bot.say("You forgot an argument!")

bot.run(config['bot']['token'])
