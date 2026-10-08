import os
import discord
from discord.ext import commands
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- MINI SERVIDOR WEB PARA ENGANAR O RENDER ---
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot Online")

def run_web_server():
    server = HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), MyServer)
    server.serve_forever()

# Inicia o servidor web em segundo plano
threading.Thread(target=run_web_server, daemon=True).start()
# -----------------------------------------------

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
        color=discord.Color.red()
    )
    embed.add_field(name="🆔 ID DA SALA", value=sala_atual["id"], inline=False)
    embed.add_field(name="🔑 SENHA", value=sala_atual["senha"], inline=False)
    await ctx.send(embed=embed)

bot.run(os.environ.get('TOKEN'))
