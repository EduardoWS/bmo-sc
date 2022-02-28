import discord
from discord.ext import commands
import infos
import sqlite3
import os
import asyncio

canais_permitidos = infos.canais_perm()


class quiz(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def addquiz(self, ctx):
        if ctx.channel.id in canais_permitidos:
            caminho = f'{os.getcwd()}/bmoBD.db'
            conn = sqlite3.connect(caminho)
            cur = conn.cursor()

            cur.execute('SELECT id FROM quizid')
            resultado = cur.fetchone()
            cur.execute('SELECT * FROM quiz')
            resultado2 = cur.fetchall()

            if resultado[0] == 0 and len(resultado2) < 4:

                def check(message):
                    if message.author == ctx.author and ctx.channel == message.channel:
                        return check
                
                try:
                    await ctx.send('Envia a pergunta:')
                    perg = await self.client.wait_for('message', timeout=180, check=check)
                    perg = perg.content
                    
                    await ctx.send('Agora me envia o gabarito: ')
                    gab = await self.client.wait_for('message', timeout=120, check=check)
                    gab = gab.content.lower()
                    cur.execute('INSERT INTO quiz (quests, gab) VALUES (?, ?)', (perg, gab))
                    conn.commit()


                except:
                    await ctx.send('Tempo expirado.')

                else:
                    if len(resultado2) == 0:
                        num = 1
                    elif len(resultado2) == 1:
                        num = 2
                    elif len(resultado2) == 2:
                        num = 3
                    elif len(resultado2) == 3:
                        num = 4
                    cur.execute('SELECT gab FROM quiz')
                    resultado = cur.fetchall()
                    await ctx.send(f'Questão adicionada com sucesso! \nHá {len(resultado)} questão(ões) adicionada(s).')

                    emb = discord.Embed(
                        title='QUIZ | 120 seg',
                        description=f'''
{num}. {perg}

Gabarito: || {gab.upper()} ||
━━━━━━━━━━━━━━━━━━━━━━━━━━
                    '''
                )
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/907045502376370256/922242413894959145/ponto.png')
                    quiz = await ctx.send(embed = emb)
                    """ await quiz.add_reaction('🇦')
                    await quiz.add_reaction('🇧')
                    await quiz.add_reaction('🇨')
                    await quiz.add_reaction('🇩') """

            elif resultado[0] != 0 and len(resultado2) < 4:
                await ctx.send('O Quiz está ativo neste momento. Para encerrar digite `??stopquiz`')
            elif resultado[0] == 0 and len(resultado2) >= 4:
                await ctx.send('O limite máximo de 4 quests já foi atingido!')
    
    @commands.command()
    async def startquiz(self, ctx):
        if ctx.channel.id in canais_permitidos:
            emb = discord.Embed(
                title='O QUIZ FOI INICIADO!!',
                description='''
Para participar do Quiz você deve enviar o comando `??quiz` na minha DM.
Depois de ter feito isso, eu vou te mandar uma questão de cada vez e você terá um certo tempo para responder. Se acabar o tempo você perde a questão.

No final eu vou te mostrar o gabarito de todas as questões junto com os seus acertos e erros.
                '''
            )
            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/907045502376370256/922242413894959145/ponto.png')

            caminho = f'{os.getcwd()}/bmoBD.db'
            conn = sqlite3.connect(caminho)
            cur = conn.cursor()
            cur.execute("SELECT id FROM quizid")
            resultado = cur.fetchone()
            cur.execute('SELECT * FROM quiz')
            resultado2 = cur.fetchall()

            if resultado[0] == 0 and len(resultado2) == 4:
                cur.execute("UPDATE quizid SET id=1")
                conn.commit()
                canal = self.client.get_channel(929800532397260821)
                squiz = await canal.send(embed = emb)
            elif resultado[0] != 0 and resultado2 != None:
                await ctx.send('O Quiz está ativo neste momento. Para encerrar digite `??stopquiz`')
            elif resultado[0] == 0 and resultado2 == None:
                await ctx.send('Não há questões no banco de dados!')
            elif resultado[0] == 0 and len(resultado2) < 4:
                await ctx.send(f'Só há {len(resultado2)} questão(ões) no banco de dados. É preciso ter 4')


    @commands.command()
    async def stopquiz(self, ctx):
        if ctx.channel.id in canais_permitidos:
            caminho = f'{os.getcwd()}/bmoBD.db'
            conn = sqlite3.connect(caminho)
            cur = conn.cursor()
            cur.execute("SELECT id FROM quizid")
            resultado = cur.fetchone()

            if resultado[0] == 0:
                await ctx.send('O Quiz já foi parado! Use `??startquiz` para iniciar outro.')
            else:
                cur.execute('UPDATE quizid SET id=0')
                conn.commit()
                await ctx.send('Quiz encerrado com sucesso!')
    
    @commands.command()
    async def removequiz(self, ctx):
        if ctx.channel.id in canais_permitidos:
            caminho = f'{os.getcwd()}/bmoBD.db'
            conn = sqlite3.connect(caminho)
            cur = conn.cursor()
            cur.execute("SELECT * FROM quiz")
            resultado = cur.fetchall()

            if resultado == None:
                await ctx.send('Não há questões salvas. Use `??addquests` para adicionar novas questões.')
            else:
                cur.execute('UPDATE quizid SET id=0')
                cur.execute('DELETE FROM quiz')
                cur.execute("DELETE FROM user_quiz")
                conn.commit()
                await ctx.send('Questões apagadas com sucesso!')
    

    @commands.command()
    async def quiz(self, ctx):
        if type(ctx.channel) == discord.DMChannel:
            caminho = f'{os.getcwd()}/bmoBD.db'
            conn = sqlite3.connect(caminho)
            cur = conn.cursor()
            cur.execute('SELECT id FROM quizid')
            resultado = cur.fetchone()
            cur.execute("SELECT iduser FROM user_quiz WHERE iduser = ?", (str(ctx.author.id), ))
            result = cur.fetchone()

            if result == None:
                if resultado[0] == 1:
                    cur.execute('SELECT * FROM quiz')
                    resultado2 = cur.fetchall()
                
                    def check(reaction, user):
                        if user == ctx.author and (str(reaction.emoji) == '🇦' or str(reaction.emoji) == '🇧' or str(reaction.emoji) == '🇨' or str(reaction.emoji) == '🇩'):
                            return check
                    perg1 = resultado2[0][0]
                    emb = discord.Embed(
                        title='QUIZ | 120 seg',
                        description=f'''
1. {perg1}

━━━━━━━━━━━━━━━━━━━━━━━━━━
                    '''
                )
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/907045502376370256/922242413894959145/ponto.png')
                    msg = await ctx.send(embed=emb)
                    await msg.add_reaction('🇦')
                    await msg.add_reaction('🇧')
                    await msg.add_reaction('🇨')
                    await msg.add_reaction('🇩')

                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
                    except:
                        await ctx.send('🔴 Acabou o tempo e você não respondeu. Questão ficará sem resposta.')
                        quest1 = '🔴'
                    else:
                        if str(reaction.emoji) == '🇦' and resultado2[0][1] == 'a':
                            quest1 = '🟢'
                        elif str(reaction.emoji) == '🇧' and resultado2[0][1] == 'b':
                            quest1 = '🟢'
                        elif str(reaction.emoji) == '🇨' and resultado2[0][1] == 'c':
                            quest1 = '🟢'
                        elif str(reaction.emoji) == '🇩' and resultado2[0][1] == 'd':
                            quest1 = '🟢'
                        else:
                            quest1 = '🔴'

                        resp = await ctx.send('**Registrando resposta...**')
                        await asyncio.sleep(2.5)
                        await resp.edit(content = '**Resposta registrada, bora pra próxima!!**')
                    
                    perg2 = resultado2[1][0]
                    emb = discord.Embed(
                        title='QUIZ | 120 seg',
                        description=f'''
2. {perg2}

━━━━━━━━━━━━━━━━━━━━━━━━━━
                    '''
                )
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/907045502376370256/922242413894959145/ponto.png')
                    msg = await ctx.send(embed=emb)
                    await msg.add_reaction('🇦')
                    await msg.add_reaction('🇧')
                    await msg.add_reaction('🇨')
                    await msg.add_reaction('🇩')

                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
                    except:
                        await ctx.send('🔴 Acabou o tempo e você não respondeu. Questão ficará sem resposta.')
                        quest2 = '🔴'
                    else:
                        if str(reaction.emoji) == '🇦' and resultado2[1][1] == 'a':
                            quest2 = '🟢'
                        elif str(reaction.emoji) == '🇧' and resultado2[1][1] == 'b':
                            quest2 = '🟢'
                        elif str(reaction.emoji) == '🇨' and resultado2[1][1] == 'c':
                            quest2 = '🟢'
                        elif str(reaction.emoji) == '🇩' and resultado2[1][1] == 'd':
                            quest2 = '🟢'
                        else:
                            quest2 = '🔴'
                        resp = await ctx.send('**Registrando resposta...**')
                        await asyncio.sleep(2.5)
                        await resp.edit(content = '**Resposta registrada, bora pra próxima!!**')
                        
                    
                    perg3 = resultado2[2][0]
                    emb = discord.Embed(
                        title='QUIZ | 120 seg',
                        description=f'''
3. {perg3}

━━━━━━━━━━━━━━━━━━━━━━━━━━
                    '''
                )
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/907045502376370256/922242413894959145/ponto.png')
                    msg = await ctx.send(embed=emb)
                    await msg.add_reaction('🇦')
                    await msg.add_reaction('🇧')
                    await msg.add_reaction('🇨')
                    await msg.add_reaction('🇩')

                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
                    except:
                        await ctx.send('🔴 Acabou o tempo e você não respondeu. A questão ficará sem resposta.')
                        quest3 = '🔴'
                    else:
                        if str(reaction.emoji) == '🇦' and resultado2[2][1] == 'a':
                            quest3 = '🟢'
                        elif str(reaction.emoji) == '🇧' and resultado2[2][1] == 'b':
                            quest3 = '🟢'
                        elif str(reaction.emoji) == '🇨' and resultado2[2][1] == 'c':
                            quest3 = '🟢'
                        elif str(reaction.emoji) == '🇩' and resultado2[2][1] == 'd':
                            quest3 = '🟢'
                        else:
                            quest3 = '🔴'
                        resp = await ctx.send('**Registrando resposta...**')
                        await asyncio.sleep(2.5)
                        await resp.edit(content = '**Resposta registrada, bora pra última!!**')
                    
                    perg4 = resultado2[3][0]
                    emb = discord.Embed(
                        title='QUIZ | 120 seg',
                        description=f'''
4. {perg4}

━━━━━━━━━━━━━━━━━━━━━━━━━━
                    '''
                )
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/907045502376370256/922242413894959145/ponto.png')
                    msg = await ctx.send(embed=emb)
                    await msg.add_reaction('🇦')
                    await msg.add_reaction('🇧')
                    await msg.add_reaction('🇨')
                    await msg.add_reaction('🇩')

                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
                    except:
                        await ctx.send('🔴 Acabou o tempo e você não respondeu. Questão ficará sem resposta.')
                        quest4 = '🔴'
                    else:
                        if str(reaction.emoji) == '🇦' and resultado2[3][1] == 'a':
                            quest4 = '🟢'
                        elif str(reaction.emoji) == '🇧' and resultado2[3][1] == 'b':
                            quest4 = '🟢'
                        elif str(reaction.emoji) == '🇨' and resultado2[3][1] == 'c':
                            quest4 = '🟢'
                        elif str(reaction.emoji) == '🇩' and resultado2[3][1] == 'd':
                            quest4 = '🟢'
                        else:
                            quest4 = '🔴'
                        resp = await ctx.send('**Registrando resposta...**')
                        await asyncio.sleep(2.5)
                        await resp.edit(content = '**Resposta registrada!!**')
                    
                    soma = quest1 + quest2 + quest3 + quest4
                    cont = soma.count('🟢')
                    if cont == 4:
                        frase = f'Parabéns, {ctx.author.mention}!! Você conseguiu acertar todas as quests do QUIZ 🎉'
                    elif cont == 3:
                        frase = f'Uau, {ctx.author.mention}! Conseguiste acertar 75% do QUIZ 👏'
                    elif cont == 2:
                        frase = f'Não desanime, {ctx.author.mention}!! Acertaste 50% do QUIZ, rumo aos 100%'
                    elif cont == 1:
                        frase = f'Poxa, {ctx.author.mention}! Acertaste apenas 25% do QUIZ :( \nBora que nos próximos o resultado será melhor!!'
                    elif cont == 0:
                        frase = f'Não tem problema você não ter acertado nenhuma quest do QUIZ, tenho certeza que você está se esforçando muito 😊'


                    emb = discord.Embed(
                        title='RESULTADOS DO QUIZ',
                        description=f'''
{frase}

**GABARITO**

{quest1} | Questão 1 - {resultado2[0][1].upper()}

{quest2} | Questão 2 - {resultado2[1][1].upper()}

{quest3} | Questão 3 - {resultado2[2][1].upper()}

{quest4} | Questão 4 - {resultado2[3][1].upper()}

━━━━━━━━━━━━━━━━━━━━━━━━━━
                    '''
                )
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/907045502376370256/922242413894959145/ponto.png')
                    await ctx.send(embed=emb)
                    cur.execute("INSERT INTO user_quiz (iduser) VALUES (?)", (str(ctx.author.id), ))
                    conn.commit()



                else:
                    await ctx.send('O Quiz não foi iniciado ainda. Espere até que um MOD o inicie.')
            else:
                await ctx.reply('Você já completou esse QUIZ, espere outro para poder jogar novamente.')



        else:
            await ctx.send('Você deve enviar este comando na minha DM!')







def setup(client):
    client.add_cog(quiz(client))
