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
        if not lesson._check_lesson_contains_student_grades():
            lesson._delete_lesson_from_database()
            await interaction.message.edit(
                content=f"{lesson._get_name()} has been deleted from the database.",
                view=None
            )
        else:
            await interaction.message.edit(
                content=f"{lesson._get_name()} has grades added and therefore can't be deleted.",
                view=None
            )


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

        await interaction.followup.send(view=Select_School_Lesson_View(list=School_Lesson()._retrieve_idlesson_list(),
                                                                       func=LessonManipulation.DELETE_LESSON))
    
    @delete.error
    async def on_delete_error(self, interaction: discord.Interaction, error: app_commands.errors.MissingRole):
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

        self.__lesson._add_lesson_to_database(name=self.__lesson._get_name(), 
                                             idteacher=teacher._get_id())
        
        await interaction.message.edit(content=f"You added **{self.__lesson._get_name()}** with **{teacher._get_givenname()} {teacher._get_surname()}** as the teacher.", 
                                       view=None)

class Select_School_Lesson(discord.ui.Select):
    def __init__(self, list: list, func: str):
        super().__init__(placeholder="Select a lesson", max_values=1)
        self.__list = list
        self.__func = func

        match self.__func:
            case LessonManipulation.DELETE_LESSON:
                for idlesson in self.__list:
                    lesson = School_Lesson(id=idlesson)
                    self.add_option(label=f"{lesson._get_name()}",
                                    description=f"Teacher: {lesson._get_school_teacher()._get_full_name() if not None else ''}",
                                    value=lesson._get_id())
                    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
       
        match self.__func:
            case LessonManipulation.DELETE_LESSON:
                await LessonManipulation._delete_lesson_from_database(interaction=interaction, 
                                                                lesson=School_Lesson(id=self.values[0]))

class Select_School_Teacher_View(discord.ui.View):
    def __init__(self, list: list, lesson: School_Lesson, func: str):
        super().__init__()
        self.add_item(Select_School_Teacher(list=list, lesson=lesson, func=func))

class Select_School_Lesson_View(discord.ui.View):
    def __init__(self, list: list, func: str):
        super().__init__()
        self.add_item(Select_School_Lesson(list=list, func=func))

class Lesson(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    lesson_group = LessonGroup(name="lesson", description="Commands related to lessons.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Lesson(client=client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))