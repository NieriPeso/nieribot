from . import channels

def validate_permissions(ctx):
    if "admins" in [y.name.lower() for y in ctx.author.roles] or "ñod" in [y.name.lower() for y in ctx.author.roles]:
        return True
    return False

def validate_channel(channel, key):
    
    # VALIDAR CANAL SEGUN LA KEY PASADA
    if channel == channels.channels[key]:
        return True
    return False