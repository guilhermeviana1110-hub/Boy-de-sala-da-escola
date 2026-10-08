import os
import discord
from discord import app_commands
from discord.ext import commands
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- MINI SERVIDOR WEB PARA O RENDER ---
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot Online")

def run_web_server():
    server = HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), MyServer)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()
# ---------------------------------------

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        
    async def setup_hook(self):
        # Sincroniza os comandos de barra globalmente com o Discord
        await self.tree.sync()
        print("Comandos de barra sincronizados com sucesso!")

bot = Bot()
sala_atual = {"id": "Não definida", "senha": "Não definida"}

@bot.event
async def on_ready():
    print(f"Bot online com sucesso como {bot.user}!")

# --- COMANDO DE BARRA /definir ---
@bot.tree.command(name="definir", description="Define o ID e a Senha da sala personalizada de FF")
@app_commands.describe(id_sala="Digite o ID da sala", senha="Digite a senha da sala")
async def definir(interaction: discord.Interaction, id_sala: str, senha: str):
    # Trava de segurança opcional: Apenas quem tem permissão de gerenciar mensagens ou administrador
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ Você não tem permissão para alterar as informações da sala!", ephemeral=True)
        return

    sala_atual["id"] = id_sala
    sala_atual["senha"] = senha
    await interaction.response.send_message(f"✅ Sala de FF atualizada com sucesso!\n**ID:** {id_sala} | **Senha:** {senha}")

# --- COMANDO DE BARRA /sala ---
@bot.tree.command(name="sala", description="Mostra as informações da sala atual")
async def sala(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 SALA PERSONALIZADA - FREE FIRE 🔥",
        color=discord.Color.red()
    )
    embed.add_field(name="🆔 ID DA SALA", value=sala_atual["id"], inline=False)
    embed.add_field(name="🔑 SENHA", value=sala_atual["senha"], inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(os.environ.get('TOKEN'))
