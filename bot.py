import discord
from discord.ext import commands
from cogs.utils.checks import is_owner
import datetime
import json
import logging
import sys

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='PCBot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

def load_startup():
    with open('startup.json') as f:
        return json.load(f)

startup = load_startup()
bot = commands.Bot(command_prefix=startup['prefix'], help_attr=startup['help_attrs'])

@bot.event
async def on_command_error(error, ctx):
    chan = ctx.message.channel
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(chan, 'You forgot at least one argument!')
    elif isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(chan, error)
    elif isinstance(error, commands.CheckFailure):
        await bot.send_message(chan, 'YOU SHALL NOT PASS!')
    elif isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(chan, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(chan, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr, end='')
        print('{0.__class__.__name__}: {0}'.format(error), file=sys.stderr)
    else:
        print('{0.__class__.__name__}: {0}'.format(error), file=sys.stderr)


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print(bot.user.id)
    print('----------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_error(event, *args, **kwargs):
    print('{0[0]} in {1}: {0[1]}'.format(sys.exc_info(), event))

@bot.event
async def on_resumed():
    print('resumed...')
    await bot.change_presence(game=discord.Game(name=',help'))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.is_private:
        print('Message from ' + message.author.name + ' (' + message.author.id + ')' + ('[tts]' if message.tts else '') + ': ' + message.content)
    else:
        print('Message in ' + message.server.name + '/#' + message.channel.name + ' from ' + message.author.name + ' (' + message.author.id + ')' + ('[tts]' if message.tts else '') + ': ' + message.content)
    await bot.process_commands(message)

def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)

if __name__ == '__main__':
    credentials = load_credentials()

    bot.client_id = credentials['client_id']
    bot.owner_id = credentials['owner_id']

    for cog in startup['cogs']:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print('Failed to load extention {}\n{}: {}'.format(cog, type(e).__name__, e))

    bot.run(credentials['token'])
