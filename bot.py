import asyncio  # Importa asyncio para gerenciamento do event loop, se necessário fora do contexto do bot
import os
from typing import Optional

import discord
from aiohttp import ClientSession
from discord import app_commands
from dotenv import load_dotenv  # Para carregar variáveis de ambiente do arquivo .env

# --- Configuração ---
# Carrega variáveis de ambiente de um arquivo .env, se existir
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
# Opcional: Coloque o ID do seu servidor de testes no .env ou substitua por None
# Útil para registrar comandos de barra instantaneamente para testes
TESTING_GUILD_ID_STR = os.getenv("TESTING_GUILD_ID")
TESTING_GUILD_ID = int(TESTING_GUILD_ID_STR) if TESTING_GUILD_ID_STR else None

# Verificação básica do token
if not DISCORD_BOT_TOKEN:
    raise ValueError("A variável de ambiente DISCORD_BOT_TOKEN não está definida!")


# --- Classe do Bot ---
class MCPBot(discord.Client):
    """
    Bot do Discord para integração com MCP.

    Esta classe herda de discord.Client e gerencia eventos, comandos e recursos do bot.
    """

    def __init__(
        self,
        *args,
        intents: discord.Intents,  # Intents agora são obrigatórios
        testing_guild_id: Optional[int] = None,
        **kwargs,  # Permite passar outras opções para discord.Client
    ):
        """
        Inicialização do cliente do bot.

        Args:
            intents (discord.Intents): Intents necessários para o bot.
            testing_guild_id (Optional[int]): ID do servidor de testes para registrar comandos instantaneamente.
        """
        super().__init__(*args, intents=intents, **kwargs)
        self.testing_guild_id = testing_guild_id
        self.tree = app_commands.CommandTree(self)  # Gerenciador de comandos de barra
        # Inicializa web_client como None, será criado em setup_hook
        self.web_client: Optional[ClientSession] = None

    async def on_ready(self):
        """
        Chamado quando o bot está pronto e conectado ao Discord.
        """
        await self.wait_until_ready()  # Boa prática, embora geralmente já aguardado
        print(f"Logado como {self.user} (ID: {self.user.id})")
        print("------")

    async def on_guild_join(self, guild: discord.Guild):
        """
        Chamado quando o bot entra em um novo servidor (guild).

        Args:
            guild (discord.Guild): O servidor que o bot acabou de entrar.
        """
        print(f"Entrou no servidor: {guild.name} (ID: {guild.id})")
        # Você pode sincronizar comandos específicos para este servidor aqui, se necessário
        # await self.tree.sync(guild=guild) # Sincroniza comandos específicos para este servidor

    async def on_guild_remove(self, guild: discord.Guild):
        """
        Chamado quando o bot sai ou é removido de um servidor.

        Args:
            guild (discord.Guild): O servidor que o bot saiu.
        """
        print(f"Saiu do servidor: {guild.name} (ID: {guild.id})")

    async def setup_hook(self) -> None:
        """
        Fase de configuração assíncrona. Chamado antes de on_ready.
        Local ideal para criar sessões HTTP e sincronizar comandos.
        """
        print("Executando setup_hook...")

        # Cria a sessão aiohttp ClientSession aqui
        self.web_client = ClientSession()
        print("aiohttp.ClientSession criada.")

        # Sincroniza comandos específicos para o servidor de testes (atualização instantânea)
        if self.testing_guild_id:
            guild = discord.Object(id=self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            try:
                await self.tree.sync(guild=guild)
                print(f"Comandos sincronizados com o servidor de testes (ID: {self.testing_guild_id})")
            except discord.errors.Forbidden:
                print(
                    f"Erro: O bot não possui escopo APPLICATION_COMMANDS ou permissões no servidor de testes (ID: {self.testing_guild_id})."
                )
            except Exception as e:
                print(f"Erro ao sincronizar comandos com o servidor de testes: {e}")

        print("setup_hook finalizado.")

    async def close(self) -> None:
        """
        Fecha o bot corretamente e libera recursos.
        """
        print("Fechando o bot...")
        if self.web_client:
            await self.web_client.close()
            print("aiohttp.ClientSession fechada.")
        await super().close()
        print("Bot fechado.")


# --- Definição de Intents ---
# Começa com intents padrão
definir_intents = discord.Intents.default()
# Adiciona intents privilegiadas se necessário E habilitadas no Portal de Desenvolvedores
intents.message_content = (
    True  # Necessário para ler o conteúdo das mensagens (comandos por prefixo, análise de mensagens)
)
intents.members = True  # Necessário para eventos de entrada/saída de membros, listas de membros precisas
# LEMBRETE: Habilite essas intents no Portal de Desenvolvedores do Discord!

# --- Instanciação do Bot ---
bot = MCPBot(intents=intents, testing_guild_id=TESTING_GUILD_ID)


# --- Definição de um Comando de Barra Simples (Exemplo) ---
@bot.tree.command(name="hello", description="Responde com uma saudação!")
async def hello_command(interaction: discord.Interaction):
    """
    Comando de barra /hello.
    Responde ao usuário com uma saudação personalizada.

    Args:
        interaction (discord.Interaction): A interação do usuário com o comando.
    """
    user_name = interaction.user.display_name
    await interaction.response.send_message(f"Olá {user_name}!")


# --- Execução Principal ---
if __name__ == "__main__":
    try:
        print("Iniciando o bot...")
        # Executa o bot usando o token da variável de ambiente
        bot.run(DISCORD_BOT_TOKEN)
    except discord.LoginFailure:
        print("Erro: Token do Discord inválido. Verifique a variável de ambiente DISCORD_BOT_TOKEN.")
    except discord.PrivilegedIntentsRequired:
        print(
            "Erro: Intents privilegiadas (Members ou Message Content) não estão habilitadas no Portal de Desenvolvedores do Discord."
        )
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
