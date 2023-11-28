import discord
from discord import app_commands
from discord.ext import commands
from classes.school_teacher import School_Teacher
from config import botConfig


class TeacherGroup(app_commands.Group):
    @app_commands.command()
    async def add(self, interaction: discord.Interaction, givenname: str, surname: str):
        await interaction.response.defer()
        teacher = School_Teacher(id=1)
        teacher._given_name = givenname
        teacher._surname = surname
        await interaction.followup.send(content=f"You added {givenname} {surname} as a teacher.")



class Teacher(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    teacher_group = TeacherGroup(name="teacher", description="Commands related to teachers, for admins only.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Teacher(client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))