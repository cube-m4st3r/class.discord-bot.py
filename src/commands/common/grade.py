from typing import Any
import discord
from discord import app_commands
from discord.ext import commands
from classes.lesson_grade import Lesson_Grade
from classes.school_lesson import School_Lesson
from classes.school_student import School_Student
from config import botConfig


class GradeGroup(app_commands.Group):
    @app_commands.rename(input='grade')
    @app_commands.command()
    async def add(self, interaction: discord.Interaction, input: str):
        await interaction.response.defer()

        idlesson_list = School_Lesson().retrieve_idlesson_list()
        lesson_list = list()

        for idlesson in idlesson_list:
            lesson_list.append(School_Lesson(id=idlesson))

        lesson_grade = Lesson_Grade()
        lesson_grade._set_grade(grade=input)

        await interaction.followup.send(content=f"To which lesson would you like to add the grade: **{lesson_grade._get_grade()}**?", 
                                        view=Select_School_Lesson_View(lesson_list=lesson_list, lesson_grade=lesson_grade))

    @app_commands.command()
    async def delete(self, interaction: discord.Interaction, input: str):
        await interaction.response.defer()
        await interaction.followup.send(content=f"You deleted {input} from subject")

    @app_commands.command()
    async def overview(self, interaction: discord.Interaction):
        await interaction.response.defer()

        idstudent = School_Student()._check_if_user_is_student(iduser=interaction.user.id)

        if idstudent is not None:
            idlesson_grades_list = Lesson_Grade()._retrieve_idlesson_grades_for_student(student=School_Student(id=idstudent))
            
            lesson_grade_list = list()

            for idlesson_grade in idlesson_grades_list:
                lesson_grade_list.append(Lesson_Grade(id=idlesson_grade[0]))

            grades = discord.Embed()
            grades.title = "List of your grades"

            for lesson_grade in lesson_grade_list:
                grades.add_field(name=f"{lesson_grade._lesson._get_name()}", value=f"Grade: {lesson_grade._get_grade()}", inline=False)

            await interaction.followup.send(embed=grades)
        else:
            await interaction.followup.send(content="You are not registered as a student. Please use `/register` to register yourself!")


class Select_School_Lesson(discord.ui.Select):
    def __init__(self, lesson_list, lesson_grade):
        super().__init__(placeholder="Select a lesson", max_values=1)
        self.__lesson_grade = lesson_grade
        for lesson in lesson_list:
            self.add_option(label=f"{lesson._get_name()}", description=f"Teacher: {lesson._teacher._get_givenname()} {lesson._teacher._get_surname()}", value=lesson._get_id())

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        self.__lesson_grade._set_school_lesson(lesson=School_Lesson(id=self.values[0]))
        lesson = self.__lesson_grade._get_school_lesson()

        idstudent = School_Student()._retrieve_student_by_userid(id=interaction.user.id)[0]
        Lesson_Grade()._add_grade_to_database(lesson=lesson, student=School_Student(id=idstudent), grade=self.__lesson_grade._get_grade())
        self.__lesson_grade._set_school_student(student=School_Student(id=idstudent))

        await interaction.followup.send(content=f"The grade: **{self.__lesson_grade._get_grade()}** has been added to: ***{self.__lesson_grade._lesson._get_name()}***, for you **{self.__lesson_grade._get_school_student()._get_givenname()}**")
        
class Select_School_Lesson_View(discord.ui.View):
    def __init__(self, lesson_list, lesson_grade):
        super().__init__()
        self.add_item(Select_School_Lesson(lesson_list=lesson_list, lesson_grade=lesson_grade))

class Grade(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    grade_group = GradeGroup(name="grade", description="Grade related commands")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Grade(client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))
