import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

sala_atual = {"id": "Não definida", "senha": "Não definida"}


@bot.event
async def on_ready():
  print(f"Bot online com sucesso como {bot.user}!")


@bot.command()
async def definir(ctx, id_sala: str, senha: str):
  sala_atual["id"] = id_sala
  sala_atual["senha"] = senha
  await ctx.send("✅ Sala de FF atualizada com sucesso!")


@bot.command()
async def sala(ctx):
  embed = discord.Embed(
      title="🔥 SALA PERSONALIZADA - FREE FIRE 🔥",
      color=discord.Color.red(),
  )
  embed.add_field(name="🆔 ID DA SALA", value=sala_atual["id"], inline=False)
  embed.add_field(name="🔑 SENHA", value=sala_atual["senha"], inline=False)
  await ctx.send(embed=embed)

bot.run(MTU1Nzc3NjI0MTg3NTA5OTY4OA.GJfLka.m6Y6kTk533OosOt9Hl1wsVXoD8GE-trRZs8O3U)

