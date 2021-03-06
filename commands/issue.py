import discord
from discord.ext import commands

@commands.command(brief="Allows you to create issue", description="Allows you to create issue")
async def issue(ctx):
    gitlabembed = discord.Embed(colour=ctx.author.top_role.colour, description="[Click here to create issue on GitLab](https://git.randomchars.net/Reviath/sakuya-izayoi) \n[If you don't know how to use GitLab, you can come to our server and specify the problem.](https://discord.gg/Nvte7RYfqY)")
    await ctx.send(embed=gitlabembed)

def setup(client):
    client.add_command(issue)
