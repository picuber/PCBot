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

prefix = ','
bot = commands.Bot(command_prefix=prefix)
config = load_config()

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print(bot.user.id)
    print('----------')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print('Message from ' + message.autor.name + ' (' + message.author.id + ')')
    try:
        await bot.process_commands(message)
    except MissingRequiredArgument:
        await bot.say("You forgot an argument!")

@bot.event
async def on_error(event, *args, **kwargs):
    #TODO
	try:
		pass
	except MissingRequiredArgumend:
		print('ERROR caught')
	return

#-----Commands-----
number_to_guess = random.randint(config['guess']['min'], config['guess']['max'])
@bot.command()
async def guess(number: int):
    global number_to_guess

    if number > config['guess']['max'] or number < config['guess']['min']:
        await bot.say("Choose a number between " + str(config['guess']['min']) + " and " + str(config['guess']['max']) + "!")
    elif number == number_to_guess:
        await bot.say("Correct!")
        number_to_guess = random.randint(config['guess']['min'], config['guess']['max'])
    elif number < number_to_guess:
        await bot.say("Too small!")
    else:
        await bot.say("Too big!")

@bot.command()
async def roll(*, dice_string: str):
    dice_string = dice_string.lower().replace(' ', '').replace('-', '+-').split('+')
    dices_list = []
    dices_result = []
    for d in dice_string:
        if not d == '':
            dices_list.append(d.lower().split('d'))
    for d in dices_list:
        if len(d) > 1:
            if d[0] == '':
                d[0] = '1'
            for i in range(0, int(d[0])):
                dices_result.append(random.randint(1, int(d[1])))
        else:
            dices_result.append(int(d[0]))
    roll_sum = 0
    for d in dices_result:
        roll_sum += d
    await bot.say(str(dices_result).replace(', ', ' + ') + ' = ' + str(roll_sum))

#-----Main-----
bot.run(config['bot']['token'])
