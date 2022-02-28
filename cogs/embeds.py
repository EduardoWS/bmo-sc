import discord
from discord.ext import commands
import infos

canais_permitidos = infos.canais_perm()


class embeds(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    
    @commands.command(aliases=['help', 'ajudaforca', 'comandos', 'comando', 'ajudacomandos', 'comousar'])
    async def ajuda(self, ctx):
        if ctx.channel.id in canais_permitidos:
            emb = discord.Embed(
                title = 'COMANDOS FORCA',
                description = '''
`??fs`
Comando para jogar Forca no modo single-player

`??forca @user1`
Comando para jogar Forca com user1

`??forca @user1 @user2`
Comando para jogar Forca com user1 e user2

`??forca @user1 @user2 @user3`
Comando para jogar Forca com user1, user2 e user3 (limite máximo)

`chutar palavra` (coloque o que você acha que é no lugar de palavra)
Usado para chutar alguma palavra caso já saiba qual é (se errar o jogo acaba e você perde)

━━━━━━━━━━━━━━━━━━━━━━━━━━
                ''',
                colour = 16715320
            )
            emb.set_footer(text='Página 1/3')
            msg = await ctx.reply(embed = emb)
            await msg.add_reaction('◀️')
            await msg.add_reaction('▶️')
            cont = 1

            emb2 = discord.Embed(
                title='COMANDOS FRASES',
                description='''
`??addfrase [escreva a frase aqui]` (Sem as chaves [])
Comando para enviar uma frase para ser analisada e posteriormente adicionada

`??frase` (sua DM precisa estar aberta)
Comando para o BMO enviar uma frase em sua DM

━━━━━━━━━━━━━━━━━━━━━━━━━━
**COMANDOS ABAIXO SÃO APENAS PARA MODS**

`??inserirfrase [escreva a frase aqui]`
Comando para adicionar frases analisadas no BMO

━━━━━━━━━━━━━━━━━━━━━━━━━━
                ''',
                colour=16715320
            )
            emb2.set_footer(text='Página 2/3')
            emb3 = discord.Embed(
                title='COMANDOS QUIZ',
                description='''
`??quiz` (só funciona na DM do BMO)
Comando para o BMO enviar as questões do QUIZ

━━━━━━━━━━━━━━━━━━━━━━━━━━
**COMANDOS ABAIXO SÃO APENAS PARA MODS**

`??addquiz`
Comando para adicionar uma questão para o QUIZ

`??startquiz`
Comando para iniciar o QUIZ e anunciar em determinado canal que ele começou

`??stopquiz` 
Comando para encerrar o QUIZ e anunciar em determinado canal que ele encerrou (Ao encerrar o QUIZ ninguém poderá usar mais o comando `??quiz` até que outro QUIZ seja iniciado)

`??removequiz`
Comando para excluir todas as questões do banco de dados

━━━━━━━━━━━━━━━━━━━━━━━━━━
    ''',
                colour=16715320
            )
            emb3.set_footer(text='Página 3/3')
            while True:
                def checkmenu(reaction, user):
                    if user == ctx.author and (str(reaction.emoji) == '◀️' or str(reaction.emoji) == '▶️'):
                        return checkmenu
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=180, check=checkmenu)

                except:
                    break
                else:
                    if cont == 1 and str(reaction.emoji) == '▶️':
                        await msg.edit(embed = emb2)
                        await msg.remove_reaction('▶️', ctx.author)
                        cont = 2
                    elif cont == 2 and str(reaction.emoji) == '▶️':
                        await msg.edit(embed = emb3)
                        await msg.remove_reaction('▶️', ctx.author)
                        cont = 3
                    elif cont == 2 and str(reaction.emoji) == '◀️':
                        await msg.edit(embed = emb)
                        await msg.remove_reaction('◀️', ctx.author)
                        cont = 1
                    elif cont == 3 and str(reaction.emoji) == '◀️':
                        await msg.edit(embed = emb2)
                        await msg.remove_reaction('◀️', ctx.author)
                        cont = 2


def setup(client):
    client.add_cog(embeds(client))