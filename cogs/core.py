from discord.ext import commands
import discord
from cogs.utils.checks import is_owner
import logging
import os

class Core:
    def __init__(self, bot):
        global log
        self.bot = bot
        log = bot.logger.getChild('core')

    @commands.command(help='Bring PCBot to ***your*** guild', hidden=True, aliases=['invite'])
    @is_owner()
    async def invitelink(self):
        await self.bot.say(discord.utils.oauth_url(self.bot.user.id))

    @commands.command(hidden=True, aliases=['exit', 'kill'])
    @is_owner()
    async def killbot(self):
        log.info('Killing PCBot...')
        await self.bot.say('Good bye cruel world!')
        os._exit(0)

    @commands.command(help='Load a module', hidden=True)
    @is_owner()
    async def load(self, *, module : str):
        module = module.lower()
        if module in self.bot.extensions:
            await self.bot.say(module + ' already loaded')
            return
        try:
            self.bot.load_extension(module)
        except discord.ClientException as e:
            await self.bot.say('Thats not a module!')
        except ImportError as e:
            await self.bot.say('Ew! What\'s that?? I don\'t know that! Get that away from me!')
        except Exception as e:
            await self.bot.say(module + ' could not be loaded')
            log.error('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say(module + ' successfully loaded')

    @commands.command(help='Unload a module', hidden=True)
    @is_owner()
    async def unload(self, *, module : str):
        module = module.lower()
        if module == 'cogs.core':
            await self.bot.say('You can\'t take my heart! I only have two!!')
            return
        if self.bot.extensions.get(module) is None:
            await self.bot.say('I don\'t have that. You can\'t take things from me I don\'t have')
            return
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say(module + ' could not be unloaded')
            log.error('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say(module + ' successfully unloaded')

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def do(self, ctx, times : int, *, command):
        """Repeats a command a specified number of times."""
        msg = ctx.message
        msg.content = command
        for i in range(times):
            await self.bot.process_commands(msg)

    @commands.command(help='Pong')
    async def ping(self):
        await self.bot.say('Pong')

def setup(bot):
    bot.add_cog(Core(bot))
