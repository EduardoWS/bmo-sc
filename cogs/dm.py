import discord
from discord.ext import commands
from discord.message import Message

from infos import canais_perm

class dm(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def dm(self, ctx, id, *, message):
        canal_perm = [924789989559115846]
        if ctx.channel.id in canal_perm:
            dm_user = self.client.get_user(int(id))
            
            try:
                await dm_user.send(message)
            
            except:
                await ctx.send('Berserker, socorro!! Não consigo enviar a mensagem AAAAAAA')
            
            else:
                await ctx.send(f'━━━━━━━━━━━━━━━━━━━━━━━━━━ \nMensagem enviada para <@{int(id)}>: \n> {message}')





def setup(client):
    client.add_cog(dm(client))
