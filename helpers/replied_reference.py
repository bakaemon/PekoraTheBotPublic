import discord


def replied_reference(ctx):
    ref = ctx.message.reference
    if ref and isinstance(ref.resolved, discord.Message):
        return ref.resolved.to_reference()
    return None
