import discord
from discord import app_commands
from discord.ext import commands
import config


class GradeGroup(app_commands.Group):
    @app_commands.command()
    async def add(self, interaction: discord.Interaction, grade: str):
        await interaction.response.defer()
        await interaction.followup.send(content=f"You added {grade} to subject")

    @app_commands.command()
    async def delete(self, interaction: discord.Interaction, grade: str):
        await interaction.response.defer()
        await interaction.followup.send(content=f"You deleted {grade} from subject")

class Grade(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    grade = GradeGroup(name="grade", description="Grade related commands")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Grade(client), guild=discord.Object(id=1091022611779174470))
