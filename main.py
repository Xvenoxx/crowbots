import os
from datetime import timedelta

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="+",
    intents=intents,
    help_command=None,
)


@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user} ({bot.user.id})")


@bot.command(name="help")
async def aide(ctx):
    embed = discord.Embed(
        title="🛡️ Commandes de modération",
        description="Voici les commandes disponibles :",
        color=discord.Color.blurple(),
    )
    embed.add_field(
        name="+ban @membre [raison]",
        value="Bannir un membre.",
        inline=False,
    )
    embed.add_field(
        name="+kick @membre [raison]",
        value="Expulser un membre.",
        inline=False,
    )
    embed.add_field(
        name="+clear nombre",
        value="Supprimer des messages.",
        inline=False,
    )
    embed.add_field(
        name="+mute @membre [minutes] [raison]",
        value="Rendre un membre muet temporairement.",
        inline=False,
    )
    embed.add_field(
        name="+unmute @membre",
        value="Retirer le mute temporaire.",
        inline=False,
    )
    await ctx.send(embed=embed)


@bot.command()
@commands.guild_only()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, membre: discord.Member, *, raison="Aucune raison indiquée"):
    await membre.ban(reason=raison)
    await ctx.send(f"🔨 {membre.mention} a été banni. Raison : {raison}")


@bot.command()
@commands.guild_only()
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx, membre: discord.Member, *, raison="Aucune raison indiquée"):
    await membre.kick(reason=raison)
    await ctx.send(f"👢 {membre.mention} a été expulsé. Raison : {raison}")


@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True, read_message_history=True)
async def clear(ctx, nombre: int):
    if nombre < 1 or nombre > 100:
        await ctx.send("Choisis un nombre entre 1 et 100.")
        return

    messages = await ctx.channel.purge(limit=nombre)
    confirmation = await ctx.send(f"🧹 {len(messages)} message(s) supprimé(s).")
    await confirmation.delete(delay=4)


@bot.command()
@commands.guild_only()
@commands.has_permissions(moderate_members=True)
@commands.bot_has_permissions(moderate_members=True)
async def mute(
    ctx,
    membre: discord.Member,
    minutes: int = 10,
    *, raison="Aucune raison indiquée",
):
    if minutes < 1 or minutes > 40320:
        await ctx.send("La durée doit être entre 1 minute et 28 jours.")
        return

    await membre.timeout(timedelta(minutes=minutes), reason=raison)
    await ctx.send(
        f"🔇 {membre.mention} est mute pendant {minutes} minute(s). "
        f"Raison : {raison}"
    )


@bot.command()
@commands.guild_only()
@commands.has_permissions(moderate_members=True)
@commands.bot_has_permissions(moderate_members=True)
async def unmute(ctx, membre: discord.Member):
    await membre.timeout(None, reason=f"Unmute par {ctx.author}")
    await ctx.send(f"🔊 Le mute de {membre.mention} a été retiré.")


@bot.event
async def on_command_error(ctx, erreur):
    if isinstance(erreur, commands.MissingPermissions):
        await ctx.send("❌ Tu n'as pas la permission nécessaire.")
    elif isinstance(erreur, commands.BotMissingPermissions):
        await ctx.send("❌ Il manque une permission au bot.")
    elif isinstance(erreur, commands.MissingRequiredArgument):
        await ctx.send("❌ Il manque un argument. Utilise +help.")
    elif isinstance(erreur, commands.MemberNotFound):
        await ctx.send("❌ Membre introuvable. Mentionne-le correctement.")
    elif isinstance(erreur, commands.BadArgument):
        await ctx.send("❌ Argument invalide. Vérifie la commande.")
    elif isinstance(erreur, commands.CommandNotFound):
        return
    else:
        print(f"Erreur : {erreur}")
        await ctx.send("❌ Une erreur est survenue pendant la commande.")


token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("Définis la variable d'environnement DISCORD_TOKEN.")

bot.run(token)
