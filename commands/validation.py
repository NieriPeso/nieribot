def validate_permissions(ctx):
    if "admins" in [y.name.lower() for y in ctx.author.roles] or "ñod" in [y.name.lower() for y in ctx.author.roles]:
        return True
    return False