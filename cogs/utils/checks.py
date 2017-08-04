from discord.ext import commands

_owner_id = None

def set_owner_id(id):
    global _owner_id
    _owner_id = id

def is_owner():
    def predicate(ctx):
        return _owner_id != None and ctx.message.author.id == _owner_id
    return commands.check(predicate)
