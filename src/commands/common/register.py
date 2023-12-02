import discord
from discord import app_commands
from discord.ext import commands
from classes.user import User
from classes.school_student import School_Student
from classes.person import Person
from config import botConfig

class Register(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="register", description="Register to the database.")
    async def register(self, interaction: discord.Interaction, givenname: str, surname: str):
        await interaction.response.defer()

        iduser = User()._add_user_to_database(id=interaction.user.id, username=interaction.user.name)

        idperson = Person()._add_person_to_database(givenname=givenname, surname=surname)
        idstudent = School_Student()._add_school_student_to_database(idperson=idperson, iduser=iduser)
        student = School_Student(id=idstudent)
        await interaction.followup.send(content=f"***{student._user._get_username()}***, you have been registered as **{student._get_full_name()}**.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Register(client=client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))


