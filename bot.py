import discord
from discord.ext import commands

# Configurações
TOKEN = 'Safadinho' # Substitua pelo seu token de bot
# Substitua pelo seu token de bot
CHANNEL_ID = 1362461608890077488  
MESSAGE_ID = 1362466517836497079  

# Mapeamento de emojis para cores
emoji_to_role = {
    '🟡': 'Amarelo',
    '🔵': 'Azul',
    '⚪': 'Branco',
    '🔷': 'Ciano',
    '💚': 'Ciano Verde Limão',
    '🔘': 'Cinza',
    '💎': 'Esmeralda',
    '🟠': 'Laranja',
    '🌸': 'Rosa',
    '💖': 'Rosa choque',
    '🟣': 'Roxo',
    '🍏': 'Verde Claro',
    '🌲': 'Verde Musgo',
    '🟢': 'Verde puro',
    '🔴': 'Vermelho'
}

# Lista de todos os cargos de cores (para remoção)
all_color_roles = list(emoji_to_role.values())

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    
    if MESSAGE_ID is None:
        channel = bot.get_channel(CHANNEL_ID)
        if channel is None:
            print(f'Canal com ID {CHANNEL_ID} não encontrado!')
            return
        
        message_text = "**Escolha sua cor favorita!**\n\nReaja com os emojis abaixo para receber o cargo correspondente:\n"
        message_text += "Você só pode ter uma cor ativa por vez.\n\n"
        
        for emoji, role in emoji_to_role.items():
            message_text += f"{emoji} - {role}\n"
        
        message = await channel.send(message_text)
        
        # Adiciona reações
        for emoji in emoji_to_role.keys():
            await message.add_reaction(emoji)
        
        print(f'Mensagem de reações enviada com ID: {message.id}')
        print('ATENÇÃO: Copie este ID e substitua no código na variável MESSAGE_ID')

async def remove_all_color_roles(member):
    for role_name in all_color_roles:
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role and role in member.roles:
            await member.remove_roles(role)
            print(f'Removido cargo {role_name} de {member.display_name}')

@bot.event
async def on_raw_reaction_add(payload):
    # Ignora bots
    if payload.member.bot:
        return
    
    if MESSAGE_ID is not None and payload.message_id != MESSAGE_ID:
        return
    
    emoji = str(payload.emoji)
    role_name = emoji_to_role.get(emoji)
    
    if role_name is None:
        return
    
    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return
    
    member = guild.get_member(payload.user_id)
    if member is None:
        return
    
    # Remove todos os cargos de cores primeiro
    await remove_all_color_roles(member)
    
    # Adiciona o novo cargo
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        print(f'Cargo {role_name} não encontrado!')
        return
    
    try:
        await member.add_roles(role)
        print(f'Cargo {role_name} adicionado para {member.display_name}')
        
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, member)
        
    except Exception as e:
        print(f'Erro ao adicionar cargo: {e}')

@bot.event
async def on_raw_reaction_remove(payload):
    pass

bot.run(TOKEN)