def validate_permissions(ctx):
    if "admins" in [y.name.lower() for y in ctx.author.roles] or "ñod" in [y.name.lower() for y in ctx.author.roles]:
        return True
    return False

def validate_channel(channel, key):
    channels = {
        'remate-valorate':849410645513207828,
        'cartelera-remate':854807245509492808
    }
    # VALIDAR CANAL REMATE-VALORATE
    if channel == channels.get(key=key):
        return True
    return False