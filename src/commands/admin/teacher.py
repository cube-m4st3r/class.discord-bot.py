import discord
from discord import app_commands
from discord.ext import commands
from classes.school_teacher import School_Teacher
from classes.person import Person
from config import botConfig


class TeacherGroup(app_commands.Group):
    @app_commands.command()
    async def add(self, interaction: discord.Interaction, givenname: str, surname: str):
        await interaction.response.defer()
        idperson = Person().add_person_to_database(givenname=givenname, surname=surname)
        idteacher = School_Teacher().add_teacher_to_database(idperson=idperson)
        teacher = School_Teacher(id=idteacher)
        await interaction.followup.send(content=f"You added {teacher.get_givenname()} {teacher.get_surname()} as a teacher.")

class Teacher(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    teacher_group = TeacherGroup(name="teacher", description="Commands related to teachers, for admins only.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Teacher(client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))