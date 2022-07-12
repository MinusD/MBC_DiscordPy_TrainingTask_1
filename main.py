import time
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


class User:
    def __init__(self, user_id: int):
        self.id: int = user_id
        self.win: int = 0
        self.lose: int = 0


users: [User] = []


@bot.command()
async def profile(ctx):
    """
    Выводит краткую информацию о пользователе
    - Имя в discord
    - Отображаемое имя на сервере
    - Дата и время присоединения к серверу
    """
    text = f'**Никнейм:** {ctx.author.name}\n**Отображаемое имя:** {ctx.author.display_name}' \
           f'\n**Присоединился:** {ctx.author.joined_at.strftime("%d.%m.%Y, %H:%M:%S")}'
    users.append(User(ctx.author.id))
    await ctx.send(text)


@bot.command()
async def game(ctx):
    """
    Пользователь играет в рулетку с шансом 1к3
    Выводится результат и результат записывается в статистику
    """
    a = [i for i in range(len(users)) if users[i].id == ctx.author.id]
    if a:
        # Пользователь уже добавлен
        user = a[0]
    else:
        # Создаём пользователя
        users.append(User(ctx.author.id))
        user = len(users) - 1

    rand_tmp = random.randint(0, 2)
    if not rand_tmp:
        # Победа
        users[user].win += 1
        text = 'Вы **победили**!'
    else:
        # Поражение
        users[user].lose += 1
        text = 'Вы **проиграли** :('
    await ctx.send(text)


@bot.command()
async def stats(ctx):
    """
    Выводит статистику игр пользователя
    """
    a = [i for i in range(len(users)) if users[i].id == ctx.author.id]
    if a:
        text = f'Статистика - **{ctx.author.name}**\nПобед - **{users[a[0]].win}**\nПоражений - **{users[a[0]].lose}**'
    else:
        text = 'Вы не сыграли ни одной игры'
    await ctx.send(text)


bot.run('token')
