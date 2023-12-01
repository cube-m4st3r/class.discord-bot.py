from typing import Any
import discord
from discord import app_commands
from discord.ext import commands
from discord.interactions import Interaction
from classes.school_teacher import School_Teacher
from classes.school_lesson import School_Lesson
from classes.person import Person
from utils.utils import no_permissions_embed
from config import botConfig, config


class TeacherManipulation():
    DELETE_TEACHER = "delete_teacher"
    UPDATE_TEACHER = "update_teacher"

    @classmethod
    async def _add_teacher_to_database(cls, interaction: discord.Interaction, givenname: str, surname: str):
        idperson = Person()._add_person_to_database(givenname=givenname, surname=surname)
        idteacher = School_Teacher()._add_teacher_to_database(idperson=idperson)
        teacher = School_Teacher(id=idteacher)
        await interaction.followup.send(content=f"You added **{teacher._get_givenname()} {teacher._get_surname()}** as a teacher.")

    @classmethod
    async def _delete_teacher_from_database(cls, interaction: discord.Interaction, teacher: School_Teacher):
        if len(teacher._retrieve_teacher_lessons_from_database()) == 0:
            teacher._delete_teacher_from_database()
            await interaction.message.edit(content=f"You deleted **{teacher._get_givenname()} {teacher._get_surname()}**.", view=None)
        else:
            await interaction.message.edit(content=f"**{teacher._get_givenname()} {teacher._get_surname()}** is still teaching. Make sure to delete the lesson!", view=None)

class TeacherGroup(app_commands.Group):
    @app_commands.command(description="Add a teacher to the database.")
    @app_commands.checks.has_role(config["class_manager_role_str"])
    async def add(self, interaction: discord.Interaction, givenname: str, surname: str):
        await interaction.response.defer()

        await TeacherManipulation._add_teacher_to_database(interaction=interaction, givenname=givenname, surname=surname)
    
    @add.error
    async def on_add_error(self, interaction: discord.Interaction, error: app_commands.errors.MissingRole):
        await interaction.response.send_message(embed=no_permissions_embed)

    @app_commands.command(description="Delete a teacher from the database.")
    @app_commands.checks.has_role(config["class_manager_role_str"])
    async def delete(self, interaction: discord.Interaction):
        await interaction.response.defer()

        await interaction.followup.send(view=Select_School_Teacher_View(list=School_Teacher()._retrieve_idteacher_list()))
    
    @delete.error
    async def on_add_error(self, interaction: discord.Interaction, error: app_commands.errors.MissingRole):
        await interaction.response.send_message(embed=no_permissions_embed)

    #@app_commands.command(description="Update a teacher in the database.")
    #to be added in the future

class Select_School_Teacher(discord.ui.Select):
    def __init__(self, list: list):
        super().__init__(placeholder="Select a teacher", max_values=1)
        self.__list = list

        for idteacher in self.__list:
            teacher = School_Teacher(id=idteacher)
            self.add_option(label=f"{teacher._get_givenname()} {teacher._get_surname()}", description="", value=teacher._get_id())

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()

        await TeacherManipulation._delete_teacher_from_database(interaction=interaction, teacher=School_Teacher(id=self.values[0]))

class Select_School_Teacher_View(discord.ui.View):
    def __init__(self, list: list):
        super().__init__(timeout=None)
        self.add_item(Select_School_Teacher(list=list))

class Teacher(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    teacher_group = TeacherGroup(name="teacher", description="Commands related to teachers, for admins only.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Teacher(client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))