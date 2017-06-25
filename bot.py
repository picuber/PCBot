import discord
from discord.ext import commands
from cogs.utils.checks import is_owner
import datetime
import json
import logging
import sys
import os

logging.basicConfig(
        level=logging.INFO,
        filename='PCBot.log',
        filemode='a',
        format='%(asctime)s [%(levelname)s]-%(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger('discord').setLevel(logging.WARNING)
log = logging.getLogger('PCBot')

def load_startup():
    if not os.path.isfile('startup.json'):
        startup = {'prefix': ',', 'help_attrs': {}, 'cogs': ['cogs.core']}
        with open('startup.json', 'w') as f:
            json.dump(startup, f)
        return startup
    else:
        with open('startup.json') as f:
            return json.load(f)

startup = load_startup()
bot = commands.Bot(command_prefix=startup['prefix'], help_attrs=startup['help_attrs'])

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
        log.error('In {0.command.qualified_name}:{1.__class__.__name__}: {1}'.format(ctx, error))
    else:
        log.error('{0.__class__.__name__}: {0}'.format(error), file=sys.stderr)


@bot.event
async def on_ready():
    log.info('-------------------------------------------------')
    log.info('Logged in as ' + bot.user.name)
    log.info(bot.user.id)
    log.info('----------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_error(event, *args, **kwargs):
    log.error('{0[0]} in {1}: {0[1]}'.format(sys.exc_info(), event))

@bot.event
async def on_resumed():
    log.warning('resumed...')
    await bot.change_presence(game=discord.Game(name=',help'))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.is_private:
        if message.tts:
            log.info('Message from {0.author.name} ({0.author.id}): {0.content}'.format(message))
        else:
            log.info('Message from {0.author.name} ({0.author.id})[tts]: {0.content}'.format(message))
    else:
        if message.tts:
            log.info('Message in {0.server.name}/#{0.channel.name} from {0.author.name} ({0.author.id})[tts]: {0.content}'.format(message))
        else:
            log.info('Message in {0.server.name}/#{0.channel.name} from {0.author.name} ({0.author.id}): {0.content}'.format(message))
    await bot.process_commands(message)

def create_credentials_template(filename):
    credentials = {'client_id': '000', 'token': 'Abc123', 'owner_id': '000'}
    with open(filename, 'w') as f:
        json.dump(credentials, f)
    log.critical('Could not load {}. Template created. Exiting...'.format(filename))
    exit(-1)

def load_credentials(filename):
    if not os.path.isfile(filename):
        create_credentials_template(filename)
    else:
        with open(filename) as f:
            return json.load(f)

if __name__ == '__main__':
    creds_file_template = 'credentials{}.json'
    if len(sys.argv) >= 2:
        creds_file = creds_file_template.format('-' + sys.argv[1])
    else:
        creds_file = creds_file_template.format('')

    credentials = load_credentials(creds_file)

    bot.client_id = credentials['client_id']
    bot.owner_id = credentials['owner_id']

    for cog in startup['cogs']:
        try:
            bot.load_extension(cog)
        except Exception as e:
            log.error('Failed to load extention {}\n{}: {}'.format(cog, type(e).__name__, e))

    try:
        bot.run(credentials['token'])
    except discord.errors.LoginFailure as e:
        log.critical('Could not log in. Check your credentials in {}!'.format(creds_file))
        exit(-1)
