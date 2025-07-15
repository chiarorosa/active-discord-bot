# Discord Bot

Bot do Discord desenvolvido em Python para integração e automação de comandos utilizando a biblioteca `discord.py`.

## Requisitos

- Python 3.8+
- Bibliotecas:
  - discord.py
  - aiohttp
  - python-dotenv

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto (ou use o `default.env` como base) com as seguintes variáveis:

```
DISCORD_BOT_TOKEN="ID do BOT"
TESTING_GUILD_ID="ID do SERVIDOR"
```

- `DISCORD_BOT_TOKEN`: Token do seu bot no Discord (obrigatório).
- `TESTING_GUILD_ID`: (Opcional) ID do servidor de testes para registrar comandos de barra instantaneamente.

2. No [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications), ative as intents privilegiadas "Message Content" e "Members" para o seu bot.

## Como executar

```bash
python bot.py
```

## Principais métodos e eventos

- **Classe `WordcabBot`**: Herda de `discord.Client` e gerencia eventos e comandos do bot.

  - `on_ready`: Executado quando o bot conecta e está pronto.
  - `on_guild_join`: Executado quando o bot entra em um novo servidor.
  - `on_guild_remove`: Executado quando o bot é removido de um servidor.
  - `setup_hook`: Inicialização assíncrona, cria a sessão HTTP e sincroniza comandos.
  - `close`: Fecha a sessão HTTP e encerra o bot corretamente.

- **Comando de barra `/hello`**:
  - Responde ao usuário com uma saudação personalizada.

## Observações

- O bot utiliza intents privilegiadas. Certifique-se de ativá-las no portal do Discord.
- Para adicionar novos comandos de barra, utilize o decorador `@bot.tree.command`.
- O arquivo `bot.py` está totalmente documentado em português para facilitar a manutenção e extensão.
