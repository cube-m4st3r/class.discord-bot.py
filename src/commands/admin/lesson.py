import discord
from discord import app_commands
from discord.ext import commands
from classes.school_lesson import School_Lesson
from classes.school_teacher import School_Teacher
from utils.utils import no_permissions_embed
from config import botConfig, config


class LessonGroup(app_commands.Group):
    @app_commands.command()
    @app_commands.checks.has_role(config["class_manager_role_str"])
    async def add(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        idteacher_list = School_Teacher().retrieve_idteacher_list()
        teacher_list = list()
        for idteacher in idteacher_list:
            teacher = School_Teacher(id=idteacher)
            teacher_list.append(teacher)
        
        lesson = School_Lesson()
        lesson._set_name(name=name)

        await interaction.followup.send(content=f"Lesson name: **{lesson._get_name()}**", 
                                        view=Select_School_Teacher_View(teacher_list=teacher_list, lesson=lesson))
    
    @add.error
    async def on_add_error(self, interaction: discord.Interaction, error: app_commands.errors.MissingRole):
        await interaction.response.send_message(embed=no_permissions_embed)


class Select_School_Teacher(discord.ui.Select):
    def __init__(self, teacher_list, lesson):
        super().__init__(placeholder="Select a teacher", max_values=1)
        self.__lesson = lesson
        for teacher in teacher_list:
            self.add_option(label=f"{teacher._get_surname()}, {teacher._get_givenname()}", description="Teacher", value=teacher._get_id())
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        teacher = School_Teacher(id=self.values[0])

        self.__lesson.add_lesson_to_database(name=self.__lesson._get_name(), idteacher=teacher.get_id())
        
        await interaction.message.edit(content=f"You added **{self.__lesson._get_name()}** with **{teacher.get_givenname()} {teacher.get_surname()}** as the teacher.", view=None)

class Select_School_Teacher_View(discord.ui.View):
    def __init__(self, teacher_list, lesson):
        super().__init__()
        self.add_item(Select_School_Teacher(teacher_list=teacher_list, lesson=lesson))

class Lesson(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    lesson_group = LessonGroup(name="lesson", description="Commands related to lessons.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Lesson(client=client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))