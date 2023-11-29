import discord
from discord import app_commands
from discord.ext import commands
from classes.school_teacher import School_Teacher
from classes.person import Person
from utils.utils import no_permissions_embed
from config import botConfig, config


class TeacherGroup(app_commands.Group):
    @app_commands.command()
    @app_commands.checks.has_role(config["class_manager_role_str"])
    async def add(self, interaction: discord.Interaction, givenname: str, surname: str):
        await interaction.response.defer()
        idperson = Person()._add_person_to_database(givenname=givenname, surname=surname)
        idteacher = School_Teacher().add_teacher_to_database(idperson=idperson)
        teacher = School_Teacher(id=idteacher)
        await interaction.followup.send(content=f"You added {teacher._get_givenname()} {teacher._get_surname()} as a teacher.")
    
    @add.error
    async def on_add_error(self, interaction: discord.Interaction, error: app_commands.errors.MissingRole):
        await interaction.response.send_message(embed=no_permissions_embed)

class Teacher(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    teacher_group = TeacherGroup(name="teacher", description="Commands related to teachers, for admins only.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Teacher(client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))