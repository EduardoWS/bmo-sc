import discord
from discord.ext import commands
import psycopg2 as db
import os
import requests
from discord.ext import tasks


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '??', case_insensitive = True, intents = intents)
client.remove_command('help')

db_host = ""
db_user = ""
db_name = ""
db_pass = ""



@client.event
async def on_ready():
    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
    cur = conn.cursor()
    cur.execute("UPDATE idforca SET id = 0")
    conn.commit()
    cur.close()
    conn.close()
    my_background.start()
    print('O BMO FOI LIGADO!')

@client.listen('on_message')
async def on_message(message):

    if type(message.channel) == discord.DMChannel and not message.author.bot:
        canal = client.get_channel(924789989559115846)
        img = message.attachments
        
        if img:
            

            await canal.send(f'━━━━━━━━━━━━━━━━━━━━━━━━━━ \n<@{message.author.id}> enviou: \n> {message.content}')
            for n in range(0, len(img)):
                await canal.send(img[n])


        else:
            await canal.send(f'━━━━━━━━━━━━━━━━━━━━━━━━━━ \n<@{message.author.id}> enviou: \n> {message.content}')



initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])


if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)





@tasks.loop(hours=8)
async def my_background():
    channel = client.get_channel(920736410183557142)
    result = requests.get("https://discloud.app/status/user", headers={"api-token": ""}).json()
    r = result["lastDataLeft"]["days"]
    if r == 1 or r == 0:
        edu = client.get_user(611235322411352107)
        await channel.send(f'{edu.mention} **EDUUUU, SOCORRO!!! VÃO ME DESLIGAR DA TOMADA, FAÇA O BACKUP AGORA!!**')
        await edu.send('**EDUUUU, SOCORRO!!! VÃO ME DESLIGAR DA TOMADA, FAÇA O BACKUP AGORA!!**')


@my_background.before_loop
async def before_my_task():
    await client.wait_until_ready()
        
@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000, 1)
    await ctx.send(f'Pong! {latency} ms')



client.run("token")