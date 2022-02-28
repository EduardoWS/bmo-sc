import discord
from discord.ext import commands
import psycopg2 as db
import infos
import sqlite3
import os
import datetime

canais_permitidos = infos.canais_perm()

db_host = ""
db_user = ""
db_name = ""
db_pass = ""


class frases(commands.Cog):

    def __init__(self, client):
        self.client = client

    """ @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = '**Vai com Calma!!** \nVocê só poderá usar esse comando de novo amanhã'    #`{:.2f}s`' .format(error.retry_after)
            await ctx.reply(msg) """

    @commands.command()
    async def addfrase(self, ctx, *, frase):
        if ctx.channel.id in canais_permitidos:
            canal = self.client.get_channel(931677809527648297)
            await canal.send(f'━━━━━━━━━━━━━━━━━━━━━━━━━━ \n<@{ctx.author.id}> mandou esta frase: \n> {frase}')
            await ctx.reply('Frase enviada para análise. Se for aceita, adicionaremos no banco de dados.')
        else:
            await ctx.reply('Canal errado, bobinho(a).')

    @commands.command()
    async def inserirfrase(self, ctx, *, frase):
        
        if ctx.channel.id == 931677809527648297:
            conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
            cur = conn.cursor()
            cur.execute('INSERT INTO frases (msg) VALUES (%s)', (frase, ))
            conn.commit()
            await ctx.reply('Frase adicionada com sucesso!!')

            cur.close()
            conn.close()
        else:
            await ctx.reply("Você não tem permissão para usar este comando.")

    
    """ @commands.cooldown(1, 86400, commands.BucketType.user) """
    @commands.command()
    async def frase(self, ctx):
        if ctx.channel.id in canais_permitidos:
            conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
            cur = conn.cursor()
            cur.execute("SELECT msg FROM frases ORDER BY random() LIMIT 1")
            resultado = cur.fetchone()
            dm_user = self.client.get_user(ctx.author.id)

            caminho = f'{os.getcwd()}/bmoBD.db'
            conn2 = sqlite3.connect(caminho)
            cur2 = conn2.cursor()
            cur2.execute("SELECT iduser FROM user_frases WHERE iduser = ?", (str(ctx.author.id),))
            result = cur2.fetchone()
            cur2.execute("SELECT data FROM user_frases WHERE iduser = ?", (str(ctx.author.id),))
            result2 = cur2.fetchone()
            
            data = datetime.datetime.now()
            now = data.strftime("%d/%m")
            if result == None or str(now) != result2[0]:

                try:
                    emb = discord.Embed(
                        
                        description=f"""
✨ **Frase do dia** ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━

*{resultado[0]}*

━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                    colour=49663
                )
                    await dm_user.send(embed=emb)
                except:
                    await ctx.reply('Não foi possível te mandar uma frase motivacional na DM pois ela está fechada.')

                else:
                    await ctx.reply('Uma mensagem motivacional foi enviada na sua DM!!')
                    if result != None:
                        cur2.execute("UPDATE user_frases SET data = ? WHERE iduser = ?", (str(now), str(ctx.author.id)))
                        conn2.commit()
                    else:
                        cur2.execute("INSERT INTO user_frases (iduser, data) VALUES (?, ?)", (str(ctx.author.id), str(now)))
                        conn2.commit()


            else:
                await ctx.reply('Você só pode usar esse comando uma vez por dia.')


def setup(client):
    client.add_cog(frases(client))
