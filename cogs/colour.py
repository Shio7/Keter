import time
import aiohttp
import discord
import openpyxl
import importlib
import os
import sys

from discord.ext import commands
from evs import permissions, default, http, dataIO


class Colour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command(aliases=['import color', 'import colour'])
    @commands.has_permissions(administrator=True, manage_messages=True, manage_roles=True)
    async def import_color(self, ctx, *, content: str):
        """ Loads color roles. """
        if not permissions.manage_roles(ctx):
            return await ctx.send("I don't have permission to manage roles ;-;")
        roles = ctx.guild.roles
        position = 0
        for i in range(0, len(roles)):
            if roles[i].name == content:
                position = roles[i].position
        if position == 0:
            return await ctx.send("I can't understand of position ;-;")
        filename = "lib/color.xlsx"
        book = openpyxl.load_workbook(filename)
        sheet = book.active
        for i in range(3, 137):
            name = sheet["B" + str(i)].value
            color_code = sheet["C" + str(i)].value
            color = int(color_code, 16)
            role = await ctx.guild._add_role(name=name, color=color)
            positions = {role: position}
            await ctx.guild.edit_role_positions(positions=positions)
        embed = discord.Embed(title='**Import**', description='Completely imported whole roles.', colour=0xeff0f1)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Colour(bot))