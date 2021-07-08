import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils.constants import channels

def validate_permissions(ctx):
    if "admins" in [y.name.lower() for y in ctx.author.roles] or "ñod" in [y.name.lower() for y in ctx.author.roles]:
        return True
    return False

def validate_channel(channel, key):
    
    # VALIDAR CANAL SEGUN LA KEY PASADA
    if channel == channels[key]:
        return True
    return False