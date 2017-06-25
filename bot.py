import discord
from discord.ext import commands
from cogs.utils.checks import is_owner
import datetime
import json
import logging
import sys
import os

if len(sys.argv) >= 2:
    config_name = sys.argv[1]
else:
    config_name = 'bot'

logging.basicConfig(
        level=logging.INFO,
        filename= config_name + '.log',
        filemode='a',
        format='%(asctime)s [%(levelname)s]-%(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger('discord').setLevel(logging.WARNING)
log = logging.getLogger(config_name)

def create_config_template(filename):
    config = {'prefix': ',',
            'help_attrs': {},
            'cogs': ['cogs.core'],
            'client_id': '000',
            'token': 'Abc123',
            'owner_id': '000'}
    with open(filename, 'w') as f:
        json.dump(config, f)
    log.critical('Could not load {}. Template created. Exiting...'.format(filename))
    exit(-1)

def load_config(filename):
    if not os.path.isfile(filename):
        create_config_template(filename)
    else:
        with open(filename) as f:
            return json.load(f)

config = load_config(config_name + '-config.json')
bot = commands.Bot(command_prefix=config['prefix'], help_attrs=config['help_attrs'])

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

if __name__ == '__main__':
    bot.config_name = config_name
    bot.logger = log
    bot.client_id = config['client_id']
    bot.owner_id = config['owner_id']

    for cog in config['cogs']:
        try:
            bot.load_extension(cog)
        except Exception as e:
            log.error('Failed to load extention {}\n{}: {}'.format(cog, type(e).__name__, e))

    try:
        bot.run(config['token'])
    except discord.errors.LoginFailure as e:
        log.critical('Could not log in. Check your config in {}!'.format(config_name + '-config.json'))
        exit(-1)
