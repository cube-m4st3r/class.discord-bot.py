import discord
from discord import app_commands
from discord.ext import commands
from classes.lesson_grade import Lesson_Grade


class GradeGroup(app_commands.Group):
    @app_commands.command()
    async def add(self, interaction: discord.Interaction, input: str):
        await interaction.response.defer()
        grade = Lesson_Grade(id=1)
        await interaction.followup.send(content=f"You added {input} with id: {grade._id} to subject")

    @app_commands.command()
    async def delete(self, interaction: discord.Interaction, input: str):
        await interaction.response.defer()
        await interaction.followup.send(content=f"You deleted {input} from subject")

class Grade(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    grade_group = GradeGroup(name="grade", description="Grade related commands")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Grade(client), guild=discord.Object(id=1091022611779174470))
