import discord
from discord import app_commands
from discord.ext import commands
import config


class MathGroup(app_commands.Group):
    @app_commands.command()
    async def add(self, interaction: discord.Interaction, num1: int, num2: int):
        await interaction.response.defer()
        await interaction.followup.send(content=f"Your result is: {num1 + num2}!")

    @app_commands.command()
    async def subtract(self, interaction: discord.Interaction, num1: int, num2: int):
        await interaction.response.defer()
        await interaction.followup.send(content=f"Your result is: {num1 - num2}!")

    @app_commands.command()
    async def divide(self, interaction: discord.Interaction, num1: int, num2: int):
        await interaction.response.defer()
        await interaction.followup.send(content=f"Your result is: {num1 % num2}!")

    @app_commands.command()
    async def multiply(self, interaction: discord.Interaction, num1: int, num2: int):
        await interaction.response.defer()
        await interaction.followup.send(content=f"Your result is: {num1 * num2}!")


class Math(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    math = MathGroup(name="math", description="Math related commands")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Math(client), guild=discord.Object(id=config.botConfig["hub-server-guild-id"]))
