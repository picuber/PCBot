from discord.ext import commands

def is_owner():
    def predicate(ctx):
        return ctx.message.author.id == '223037287179616266'
    return commands.check(predicate)
