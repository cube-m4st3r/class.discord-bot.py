import discord
from discord import app_commands
from discord.ext import commands
from classes.school_lesson import School_Lesson
from classes.school_teacher import School_Teacher
from utils.utils import no_permissions_embed
from config import botConfig, config


class LessonManipulation():
    ADD_LESSON = "add_lesson"
    DELETE_LESSON = "delete_lesson"
    UPDATE_LESSON = "update_lesson"

    @classmethod
    async def _add_lesson_to_database(cls, interaction: discord.Interaction, name: str):
        idteacher_list = School_Teacher()._retrieve_idteacher_list()
        
        teacher_list = list()
        for idteacher in idteacher_list:
            teacher = School_Teacher(id=idteacher)
            teacher_list.append(teacher)
        
        lesson = School_Lesson()
        lesson._set_name(name=name)

        await interaction.followup.send(content=f"Lesson name: **{lesson._get_name()}**", 
                                        view=Select_School_Teacher_View(list=teacher_list, 
                                                                        lesson=lesson,
                                                                        func=LessonManipulation.ADD_LESSON))

    @classmethod
    async def _delete_lesson_from_database(cls, interaction: discord.Interaction, lesson: School_Lesson):
        ...

    @classmethod
    async def _update_lesson_in_database(cls, interaction: discord.Interaction, lesson: School_Lesson):
        ...

class LessonGroup(app_commands.Group):
    @app_commands.command(description="Add a lesson to the database.")
    @app_commands.checks.has_role(config["class_manager_role_str"])
    async def add(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        
        await LessonManipulation._add_lesson_to_database(interaction=interaction, name=name)
    
    @add.error
    async def on_add_error(self, interaction: discord.Interaction, error: app_commands.errors.MissingRole):
        await interaction.response.send_message(embed=no_permissions_embed)

    @app_commands.command(description="Delete a lesson from the database.")
    @app_commands.checks.has_role(config["class_manager_role_str"])
    async def delete(self, interaction: discord.Interaction):
        await interaction.response.defer()

        
    
    @delete.error
    async def on_add_error(self, interaction: discord.Interaction, error: app_commands.errors.MissingRole):
        await interaction.response.send_message(embed=no_permissions_embed)

    #@app_commands.command(description="Get an overview of lessons")
    #async def overview(self, interaction: discord.Interaction):
    #    await interaction.response.defer()
    # added in the future
    
class Select_School_Teacher(discord.ui.Select):
    def __init__(self, list: list, lesson: School_Lesson, func: str):
        super().__init__(placeholder="Select a teacher", max_values=1)
        self.__lesson = lesson
        self.__func = func

        match self.__func:
            case LessonManipulation.ADD_LESSON:
                for teacher in list:
                    self.add_option(label=f"{teacher._get_surname()}, {teacher._get_givenname()}", 
                                    description="Teacher", 
                                    value=teacher._get_id())
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        teacher = School_Teacher(id=self.values[0])

        self.__lesson.add_lesson_to_database(name=self.__lesson._get_name(), 
                                             idteacher=teacher._get_id())
        
        await interaction.message.edit(content=f"You added **{self.__lesson._get_name()}** with **{teacher._get_givenname()} {teacher._get_surname()}** as the teacher.", 
                                       view=None)

class Select_School_Teacher_View(discord.ui.View):
    def __init__(self, list: list, lesson: School_Lesson, func: str):
        super().__init__()
        self.add_item(Select_School_Teacher(teacher_list=list, lesson=lesson, func=func))

class Lesson(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    lesson_group = LessonGroup(name="lesson", description="Commands related to lessons.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Lesson(client=client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))