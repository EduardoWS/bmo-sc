import discord
from discord.ext import commands
import psycopg2 as db
import infos
import asyncio

canais_permitidos = infos.canais_perm()

db_host = ""
db_user = ""
db_name = ""
db_pass = ""

class forca(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def forca(self, ctx, member1: discord.Member, member2: discord.Member=None, member3: discord.Member=None):
        
        
        if ctx.channel.id in canais_permitidos:
            conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
            cur = conn.cursor()
            cur.execute("SELECT id FROM idforca WHERE idc=%s", (str(ctx.channel.id,), ))
            resultado_id = cur.fetchone()
            

            if resultado_id[0] == 0:
                if member2 == None:
                    if ctx.author.id == member1.id:
                        await ctx.send(f'Você não pode jogar com você mesmo, seu solitário.')
                        return
                    else:
                        cur.execute("UPDATE idforca SET id = 1 WHERE idc = %s", (str(ctx.channel.id), ))
                        conn.commit()
                        confirm = await ctx.send('Clique em ✅ para confirmar a partida.')
                        await confirm.add_reaction('✅')
                        

                        def check3(reaction, user):

                            if user == member1 and str(reaction.emoji) == '✅':
                                return check3
                                

                        try:
                            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check3)
                        except asyncio.TimeoutError:
                            await ctx.send('Parece que alguém não reagiu. **Cancelando partida...**')
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            return False
                        else:
                            
                            await ctx.send(f'{member1.mention} aguarde o **{ctx.author.name}** escolher uma palavra!')
        
                            


                elif member2 != None and member3 == None:
                    if ctx.author.id == member1.id or ctx.author.id == member2.id:
                        await ctx.send(f'Você não pode jogar com você mesmo, seu solitário.')
                        return
                    else:
                        cur.execute("UPDATE idforca SET id = 1 WHERE idc = %s", (str(ctx.channel.id), ))
                        conn.commit()
                        confirm = await ctx.send('Cliquem em ✅ para confirmar a partida.')
                        await confirm.add_reaction('✅')
                        def check3(reaction, user):

                            return user == member1 or (user == member2) and str(reaction.emoji) == '✅'

                        try:
                            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check3)
                            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check3)
                        except asyncio.TimeoutError:
                            await ctx.send('Parece que alguém não reagiu. **Cancelando partida...**')
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            return False

                        else:
                            
                            await ctx.send(f'{member1.mention} e {member2.mention} aguardem o **{ctx.author.name}** escolher uma palavra!')


                elif member3 != None:
                    if ctx.author.id == member1.id or ctx.author.id == member2.id or ctx.author.id == member3.id:
                        await ctx.send(f'Você não pode jogar com você mesmo, seu solitário.')
                        return
                    else:
                        cur.execute("UPDATE idforca SET id = 1 WHERE idc = %s", (str(ctx.channel.id), ))
                        conn.commit()
                        confirm = await ctx.send('Cliquem em ✅ para confirmar a partida.')
                        await confirm.add_reaction('✅')
                        def check3(reaction, user):

                            return user == member1 or (user == member2) or (user == member3) and str(reaction.emoji) == '✅'

                        try:
                            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check3)
                            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check3)
                            reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check3)

                        except asyncio.TimeoutError:
                            await ctx.send('Parece que alguém não reagiu. **Cancelando partida...**')
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            return False

                        else:
                            
                            await ctx.send(f'{member1.mention}, {member2.mention} e {member3.mention} aguardem o **{ctx.author.name}** escolher uma palavra!')
                            

                escolhas = self.client.get_user(ctx.author.id)
                await escolhas.send('Escolha uma palavra:')

                def check(message):
                    if message.author == ctx.author and not message.guild:
                        return check 
                def check4(reaction, user):

                    return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '⛔')
                

                try:
                    palavra = await self.client.wait_for('message', check=check, timeout=180)
                    palavra = palavra.content.upper()
                    await escolhas.send('Agora digite uma dica:')
                    dica = await self.client.wait_for('message', check=check, timeout=180)
                    dica = dica.content.upper()

                    confirm2 = await escolhas.send('\✅ - confirmar\n\⛔ - cancelar')
                    await confirm2.add_reaction('✅')
                    await confirm2.add_reaction('⛔')
                    reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check4)

                    if not user.bot and str(reaction.emoji) == '⛔':
                        cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                        conn.commit()
                        await escolhas.send('**Cancelando...**\nColoque o comando `??forca @user` novamente no canal adequado.')
                        return

                    
                except asyncio.TimeoutError:
                    cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                    conn.commit()
                    await escolhas.send('Tempo expirado. Coloque o comando `??forca @user` novamente no canal adequado.')
                    return False
                
                
                
                
                
                
                
                palavra_secreta = '_' * len(palavra)
                t = ''
                jog1 = member1
                jog2 = member2
                jog3 = member3

                def encaixar(tent: str, palavra: str, palavra_secreta: str) -> str:
                    palavra_lista = list(palavra_secreta)

                    for index, letra in enumerate(list(palavra)):
                        if letra == tent:
                            palavra_lista[index] = tent
                    
                    palavra_secreta = "".join(palavra_lista)

                    return palavra_secreta




                vez = jog1
                vida = 5
                spc = ''
                cont = 0

                while True:

                    for n in range(1, len(palavra_secreta) + 1):
                        spc += palavra_secreta[n-1] + ' '
                    
                    if vida == 5:
                        h = '\❤️\❤️\❤️\❤️\❤️'
                    elif vida == 4:
                        h = '\❤️\❤️\❤️\❤️'
                    elif vida == 3:
                        h = '\❤️\❤️\❤️'
                    elif vida == 2:
                        h = '\❤️\❤️'
                    elif vida == 1:
                        h = '\❤️'
                    emb = discord.Embed(
                    title='JOGO DA FORCA',
                    description=f'''
DICA: `{dica}`

{t}

` {spc}`


VIDAS: {h}

RODADA: {vez.mention}        
                '''
            )
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                    await ctx.send(embed=emb)
                    def check2(message):
                        
                        flag = 0
                        msg = message.content
                        if msg.isalnum() or msg.isascii():
                            flag = 1
                        
                        if message.author == vez and ctx.channel == message.channel and len(message.content) == 1 and flag == 1:
                            return check2
                        elif message.author == vez and ctx.channel == message.channel and message.content.upper()[:6] == 'CHUTAR':
                            return check2
                    
                    try:
                        tent = await self.client.wait_for('message', check=check2, timeout=60)
                        tent = tent.content.upper()
                        
                    except:
                        if cont == 1 or vida == 1:
                            await ctx.send(f'{vez.mention} pensou tanto que perdeu.')
                            spc = ''
                            for n in range(1, len(palavra) + 1):
                                spc += palavra[n-1] + ' '
                            emb = discord.Embed(
                                title='FIM DE JOGO ⚰️',
                                description=f'''
A palavra que o(a) {ctx.author.mention} escolheu foi:

` {spc}`

**USE `??forca @user` PARA COMEÇAR OUTRO JOGO**

Feedback da partida:
                            '''
                        )
                            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                            p = await ctx.send(embed=emb)
                            await p.add_reaction('👍')
                            await p.add_reaction('👎')

                            if member2 == None:
                                valid_users = [member1.id]
                            elif member2 != None and member3 == None:
                                valid_users = [member1.id, member2.id]
                            else:
                                valid_users = [member1.id, member2.id, member3.id]
                            valid_reactions = ['✅', '👍', '👎']
                            def check5(reaction, user):

                                return user.id in valid_users and str(reaction.emoji) in valid_reactions


                            band_m = 0
                            try:
                                if member2 == None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 and str(reaction.emoji) == '👍':
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                elif member2 != None and member3 == None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                        band_m += 1
                                        
                                    if band_m == 2:
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')


                                elif member3 != None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        band_m += 1
                                        
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        
                                        band_m += 1

                                    if band_m == 3:
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                
                                else:
                                    await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                            

                            except asyncio.TimeoutError:
                                cur.execute("UPDATE idforca SET id = 0")
                                conn.commit()
                                return False

                            cur.execute("UPDATE idforca SET id = 0")
                            conn.commit()
                            break

                        else:
                            if member2 == None:
                                await ctx.send(f'{vez.mention} pensou demais e perdeu 1 \❤️!')
                                spc = ''
                                vida -= 1
                                cont += 1
                                continue
                            elif member2 != None and member3 == None:
                                await ctx.send(f'{vez.mention} pensou demais. Perdeu a vez e 1 \❤️!')
                                spc = ''
                                vida -= 1
                                cont += 1
                                if vez == jog1:
                                    vez = jog2
                                else:
                                    vez = jog1
                                continue
                            elif member3 != None:
                                await ctx.send(f'{vez.mention} pensou demais. Perdeu a vez e 1 \❤️!')
                                spc = ''
                                vida -= 1
                                cont += 1
                                if vez == jog1:
                                    vez = jog2
                                elif vez == jog2:
                                    vez = jog3
                                elif vez == jog3:
                                    vez = jog1
                                continue


                    if tent[:6] == 'CHUTAR':
                        if tent[7:] == palavra:
                            
                            spc = ''
                            for n in range(1, len(palavra) + 1):
                                spc += palavra[n-1] + ' '
                            emb = discord.Embed(
                                title='🎉 TEMOS UM GANHADOR 🎉',
                                description=f'''
**PARABÉNS {vez.mention} !!**

` {spc}`

VIDAS: {h}

Feedback da partida:
                        '''
                    )
                            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                            p = await ctx.send(embed=emb)
                            await p.add_reaction('👍')
                            await p.add_reaction('👎')
                            

                            if member2 == None:
                                valid_users = [member1.id]
                            elif member2 != None and member3 == None:
                                valid_users = [member1.id, member2.id]
                            else:
                                valid_users = [member1.id, member2.id, member3.id]
                            valid_reactions = ['✅', '👍', '👎']
                            def check5(reaction, user):

                                return user.id in valid_users and str(reaction.emoji) in valid_reactions


                            band_m = 0
                            try:
                                if member2 == None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 and str(reaction.emoji) == '👍':
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                elif member2 != None and member3 == None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    if band_m == 2:
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')


                                elif member3 != None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        band_m += 1
                                        
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        
                                        band_m += 1

                                    if band_m == 3:
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                
                                else:
                                    await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                            

                            except asyncio.TimeoutError:
                                cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                                conn.commit()
                                return False

                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            break





                        else:
                            spc = ''
                            for n in range(1, len(palavra) + 1):
                                spc += palavra[n-1] + ' '
                            emb = discord.Embed(
                                title='FIM DE JOGO ⚰️',
                                description=f'''
A palavra que o(a) {ctx.author.mention} escolheu foi:

` {spc}`

Lembre-se que se errar o chute você perde!!

**USE `??forca @user` PARA COMEÇAR OUTRO JOGO**

Feedback da partida:
                        '''
                        )
                            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                            p = await ctx.send(embed=emb)
                            await p.add_reaction('👍')
                            await p.add_reaction('👎')
                            

                            if member2 == None:
                                valid_users = [member1.id]
                            elif member2 != None and member3 == None:
                                valid_users = [member1.id, member2.id]
                            else:
                                valid_users = [member1.id, member2.id, member3.id]
                            valid_reactions = ['✅', '👍', '👎']
                            def check5(reaction, user):

                                return user.id in valid_users and str(reaction.emoji) in valid_reactions


                            band_m = 0
                            try:
                                if member2 == None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 and str(reaction.emoji) == '👍':
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                elif member2 != None and member3 == None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    if band_m == 2:
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')


                                elif member3 != None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        band_m += 1
                                        
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        
                                        band_m += 1

                                    if band_m == 3:
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                
                                else:
                                    await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                            

                            except asyncio.TimeoutError:
                                cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                                conn.commit()
                                return False
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            break



                    if tent in t and tent != '':
                        await ctx.send(f'{vez.mention} já tentaram essa letra!!')
                        if member2 != None and member3 == None:
                            if vez == jog1:
                                vez = jog2
                            else:
                                vez = jog1
                        elif member3 != None:
                            if vez == jog1:
                                vez = jog2
                            elif vez == jog2:
                                vez = jog3
                            elif vez == jog3:
                                vez = jog1
                        spc = ''
                        continue
                        
                    else:
                        t += tent + ' '
                        



                    if tent in palavra:
                        palavra_secreta = encaixar(tent, palavra, palavra_secreta)


                    else:
                        vida -= 1
                        if vida == 0:
                            spc = ''
                            for n in range(1, len(palavra) + 1):
                                spc += palavra[n-1] + ' '
                            emb = discord.Embed(
                                title='FIM DE JOGO ⚰️',
                                description=f'''
A palavra que o(a) {ctx.author.mention} escolheu foi:

` {spc}`

**USE `??forca @user` PARA COMEÇAR OUTRO JOGO**

Feedback da partida:
                            '''
                        )
                            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                            p = await ctx.send(embed=emb)
                            await p.add_reaction('👍')
                            await p.add_reaction('👎')
                            

                            if member2 == None:
                                valid_users = [member1.id]
                            elif member2 != None and member3 == None:
                                valid_users = [member1.id, member2.id]
                            else:
                                valid_users = [member1.id, member2.id, member3.id]
                            valid_reactions = ['✅', '👍', '👎']
                            def check5(reaction, user):

                                return user.id in valid_users and str(reaction.emoji) in valid_reactions


                            band_m = 0
                            try:
                                if member2 == None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 and str(reaction.emoji) == '👍':
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                elif member2 != None and member3 == None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    if band_m == 2:
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')


                                elif member3 != None:
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        band_m += 1
                                        
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        band_m += 1
                                    
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                    if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        
                                        band_m += 1

                                    if band_m == 3:
                                        cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                        conn.commit()
                                        await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                    else:
                                        
                                        await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                
                                else:
                                    await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                            

                            except asyncio.TimeoutError:
                                cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                                conn.commit()
                                return False
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            break




                    if palavra_secreta == palavra:
                        spc = ''
                        for n in range(1, len(palavra_secreta) + 1):
                            spc += palavra_secreta[n-1] + ' '
                        emb = discord.Embed(
                            title='🎉 TEMOS UM GANHADOR 🎉',
                            description=f'''
**PARABÉNS {vez.mention} !!**

` {spc}`

VIDAS: {h}

Feedback da partida:
                        '''
                    )
                        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                        p = await ctx.send(embed=emb)
                        await p.add_reaction('👍')
                        await p.add_reaction('👎')
                            

                        if member2 == None:
                            valid_users = [member1.id]
                        elif member2 != None and member3 == None:
                            valid_users = [member1.id, member2.id]
                        else:
                            valid_users = [member1.id, member2.id, member3.id]
                        valid_reactions = ['✅', '👍', '👎']
                        def check5(reaction, user):

                            return user.id in valid_users and str(reaction.emoji) in valid_reactions


                        band_m = 0
                        try:
                            if member2 == None:
                                reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                if user == member1 and str(reaction.emoji) == '👍':
                                    cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                    conn.commit()
                                    await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                else:
                                    await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                            elif member2 != None and member3 == None:
                                reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                    band_m += 1
                                reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                if user == member1 or (user == member2) and str(reaction.emoji) == '👍':
                                    band_m += 1
                                if band_m == 2:
                                    cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                    conn.commit()
                                    await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                else:
                                    await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')


                            elif member3 != None:
                                reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                    band_m += 1
                                        
                                reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                    band_m += 1
                                    
                                reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check5)
                                if user == member1 or user == member2 or user == member3 and str(reaction.emoji) == '👍':
                                        
                                    band_m += 1

                                if band_m == 3:
                                    cur.execute("INSERT INTO forca (palavra, dica) VALUES (%s, %s)", (palavra, dica))
                                    conn.commit()
                                    await ctx.send('Obrigado pelo seu feedback! Palavra e dica adicionada com sucesso.')
                                else:
                                        
                                    await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                                
                            else:
                                await ctx.send('Obrigado pelo seu feedback! As palavras não foram adicionadas.')
                            

                        except asyncio.TimeoutError:
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            return False
                        cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                        conn.commit()
                        break

                    if member2 != None and member3 == None:
                        if vez == jog1:
                            vez = jog2
                        else:
                            vez = jog1
                    elif member3 != None:
                        if vez == jog1:
                            vez = jog2
                        elif vez == jog2:
                            vez = jog3
                        elif vez == jog3:
                            vez = jog1

                    spc = ''
                    cont = 0

            else:
                await ctx.send(f'{ctx.author.mention} já estão jogando comigo neste canal! Por favor, aguarde o jogo terminar.')
        else:
            await ctx.send('Canal errado, bobinho(a)')
        cur.close()
        conn.close()


    @commands.command()
    async def fs(self, ctx):
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        
        if ctx.channel.id in canais_permitidos:
            cur.execute("SELECT id FROM idforca WHERE idc=%s", (str(ctx.channel.id,), ))
            resultado_id = cur.fetchone()
            
            if resultado_id[0] == 0:

                cur.execute("SELECT * FROM forca ORDER BY random() LIMIT 1")
                resultado = cur.fetchall()

                palavra = resultado[0][0].upper()
                dica = resultado[0][1].upper()

                palavra_secreta = '_' * len(palavra)
                t = ''

                cur.execute("UPDATE idforca SET id = 1 WHERE idc = %s", (str(ctx.channel.id), ))
                conn.commit()

                def encaixar(tent: str, palavra: str, palavra_secreta: str) -> str:
                    palavra_lista = list(palavra_secreta)

                    for index, letra in enumerate(list(palavra)):
                        if letra == tent:
                            palavra_lista[index] = tent
                    
                    palavra_secreta = "".join(palavra_lista)

                    return palavra_secreta

                vida = 5
                spc = ''
                cont = 0

                while True:

                    for n in range(1, len(palavra_secreta) + 1):
                        spc += palavra_secreta[n-1] + ' '
                    
                    if vida == 5:
                        h = '\❤️\❤️\❤️\❤️\❤️'
                    elif vida == 4:
                        h = '\❤️\❤️\❤️\❤️'
                    elif vida == 3:
                        h = '\❤️\❤️\❤️'
                    elif vida == 2:
                        h = '\❤️\❤️'
                    elif vida == 1:
                        h = '\❤️'
                    emb = discord.Embed(
                    title='JOGO DA FORCA SINGLEPLAYER',
                    description=f'''
DICA: `{dica}`

{t}

` {spc}`


VIDAS: {h}

JOGADOR: {ctx.author.mention}
            
                '''
            )
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                    await ctx.send(embed=emb)
                    def check2(message):
                        flag = 0
                        msg = message.content
                        if msg.isascii() or msg.isalnum():
                            flag = 1
                            
                        if message.author == ctx.author and ctx.channel == message.channel and len(message.content) == 1 and flag == 1:
                            return check2
                        elif message.author == ctx.author and ctx.channel == message.channel and message.content.upper()[:6] == 'CHUTAR':
                            return check2
                    
                    try:
                        tent = await self.client.wait_for('message', check=check2, timeout=60)
                        tent = tent.content.upper()
                        
                        

                        
                    except:
                        if cont == 1 or vida == 1:
                            await ctx.send(f'{ctx.author.mention} pensou tanto que perdeu.')
                            spc = ''
                            for n in range(1, len(palavra) + 1):
                                spc += palavra[n-1] + ' '
                            emb = discord.Embed(
                                title='FIM DE JOGO ⚰️',
                                description=f'''
A palavra que eu escolhi foi:

` {spc}`

**USE `??fs` PARA COMEÇAR OUTRO JOGO**
                            '''
                        )
                            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                            await ctx.send(embed=emb)
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            break


                        else:
                            await ctx.send(f'{ctx.author.mention} pensou demais e perdeu 1 \❤️!')
                            spc = ''
                            vida -= 1
                            cont += 1
                            continue
                        
                        
                    if tent[:6] == 'CHUTAR':
                        if tent[7:] == palavra:
                            
                            spc = ''
                            for n in range(1, len(palavra) + 1):
                                spc += palavra[n-1] + ' '
                            emb = discord.Embed(
                                title='🎉 TEMOS UM GANHADOR 🎉',
                                description=f'''
**PARABÉNS {ctx.author.mention} !!**

` {spc}`

VIDAS: {h}

**USE `??fs` PARA COMEÇAR OUTRO JOGO**
                        '''
                    )
                            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                            await ctx.send(embed=emb)
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            break
                        else:
                            spc = ''
                            for n in range(1, len(palavra) + 1):
                                spc += palavra[n-1] + ' '
                            emb = discord.Embed(
                                title='FIM DE JOGO ⚰️',
                                description=f'''
A palavra que eu escolhi foi:

` {spc}`

Lembre-se que se errar o chute você perde!!

**USE `??fs` PARA COMEÇAR OUTRO JOGO**
                        '''
                        )
                            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                            await ctx.send(embed=emb)
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            break



                    if tent in t and tent != '':
                        await ctx.send(f'{ctx.author.mention} você já tentou essa letra!!')
                        
                    else:
                        t += tent + ' '
                        



                    if tent in palavra:
                        palavra_secreta = encaixar(tent, palavra, palavra_secreta)


                    else:
                        vida -= 1
                        if vida == 0:
                            spc = ''
                            for n in range(1, len(palavra) + 1):
                                spc += palavra[n-1] + ' '
                            emb = discord.Embed(
                                title='FIM DE JOGO ⚰️',
                                description=f'''
A palavra que eu escolhi foi:

` {spc}`

**USE `??fs` PARA COMEÇAR OUTRO JOGO**
                            '''
                        )
                            emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                            await ctx.send(embed=emb)
                            cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                            conn.commit()
                            break




                    if palavra_secreta == palavra:
                        spc = ''
                        for n in range(1, len(palavra_secreta) + 1):
                            spc += palavra_secreta[n-1] + ' '
                        emb = discord.Embed(
                            title='🎉 TEMOS UM GANHADOR 🎉',
                            description=f'''
**PARABÉNS {ctx.author.mention} !!**

` {spc}`

VIDAS: {h}

**USE `??fs` PARA COMEÇAR OUTRO JOGO**
                        '''
                    )
                        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/843496086089629716/863886769882923009/hangman-game-og-share.png')
                        await ctx.send(embed=emb)
                        cur.execute("UPDATE idforca SET id = 0 WHERE idc = %s", (str(ctx.channel.id), ))
                        conn.commit()
                        break

                    spc = ''
                    cont = 0

            else:
                await ctx.send(f'{ctx.author.mention} já estão jogando comigo neste canal! Por favor, aguarde o jogo terminar.')

        else:
            await ctx.send('Canal errado bobinho(a)')

        cur.close()
        conn.close()

def setup(client):
    client.add_cog(forca(client))