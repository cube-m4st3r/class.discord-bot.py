import discord
from discord import app_commands
from discord.ext import commands
from classes.lesson_grade import Lesson_Grade
from classes.school_lesson import School_Lesson
from classes.school_student import School_Student
from config import botConfig

class GradeManipulation():
    ADD_GRADE = "add_grade"
    DELETE_GRADE = "delete_grade"

    @classmethod
    async def _add_grade_to_selected_lesson(cls, interaction, lesson_grade):
        lesson = lesson_grade._get_school_lesson()
        idstudent = School_Student()._retrieve_student_by_userid(id=interaction.user.id)[0]
        lesson_grade._add_grade_to_database(lesson=lesson, 
                                            student=School_Student(id=idstudent), 
                                            grade=lesson_grade._get_grade())
        lesson_grade._set_school_student(student=School_Student(id=idstudent))

        await interaction.message.edit(content=f"The grade: **{lesson_grade._get_grade()}** has been added to: ***{lesson_grade._lesson._get_name()}***, for you **{lesson_grade._get_school_student()._get_givenname()}**", 
                                       view=None)

    @classmethod
    async def _delete_grade_from_selected_lesson(cls, interaction, lesson_grade):
        idstudent = School_Student()._retrieve_student_by_userid(id=interaction.user.id)[0]
        idlesson_grades_list = Lesson_Grade()._retrieve_idlesson_grades_from_lesson_for_student(student=School_Student(id=idstudent), 
                                                                                                lesson=lesson_grade._get_school_lesson())
        lesson_grade_list = [Lesson_Grade(id=idlesson_grade[0]) for idlesson_grade in idlesson_grades_list]
        lesson_grade._set_school_student(student=School_Student(id=idstudent))

        await interaction.message.edit(view=Select_Grade_From_School_Lesson_View(lesson_grade_list=lesson_grade_list, 
                                                                                 lesson_grade=lesson_grade))

class GradeGroup(app_commands.Group):
    @app_commands.rename(input='grade')
    @app_commands.command(description="Add a grade to selected lesson.")
    async def add(self, interaction: discord.Interaction, input: int):
        await interaction.response.defer()

        if input <= 6:
            idlesson_list = School_Lesson().retrieve_idlesson_list()
            lesson_list = list()

            for idlesson in idlesson_list:
                lesson_list.append(School_Lesson(id=idlesson))

            lesson_grade = Lesson_Grade()
            lesson_grade._set_grade(grade=input)

            await interaction.followup.send(content=f"To which lesson would you like to add the grade: **{lesson_grade._get_grade()}**?", 
                                            view=Select_School_Lesson_View(list=lesson_list, 
                                                                           lesson_grade=lesson_grade, 
                                                                           func="add_grade"))
        else:
            out_of_range_embed = discord.Embed()
            out_of_range_embed.title = "Your input grade is not valid. Please use the command again!"
            out_of_range_embed.color = discord.Colour.red()
            await interaction.followup.send(embed=out_of_range_embed)

    @app_commands.command(description="Delete a grade from a selected lesson.")
    async def delete(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        idstudent = School_Student()._check_if_user_is_student(iduser=interaction.user.id)
        student = School_Student(id=idstudent)

        lesson_grade = Lesson_Grade()

        await interaction.followup.send(content=f"From which lesson should a grade be deleted from?",
                                        view=Select_School_Lesson_View(list=student._retrieve_attending_lessons(), 
                                                                       lesson_grade=lesson_grade,
                                                                       func="delete_grade"))

    @app_commands.command(description="Get a list of your current grades.")
    async def overview(self, interaction: discord.Interaction):
        await interaction.response.defer()

        idstudent = School_Student()._check_if_user_is_student(iduser=interaction.user.id)

        if idstudent is not None:
            idlesson_grades_list = Lesson_Grade()._retrieve_idlesson_grades_for_student(student=School_Student(id=idstudent))

            lesson_grade_list = [Lesson_Grade(id=idlesson_grade[0]) for idlesson_grade in idlesson_grades_list]

            if lesson_grade_list is not None:
                grades = discord.Embed(title="List of your grades")

                for lesson_grade in lesson_grade_list:
                    grades.add_field(name=f"{lesson_grade._lesson._get_name()}", 
                                     value=f"Grade: {lesson_grade._get_grade()}", 
                                     inline=False)

                await interaction.followup.send(embed=grades)
            else: 
                await interaction.followup.send("You don't have any grades added.")
        else:
            await interaction.followup.send("You are not registered as a student. Please use `/register` to register yourself!")

class Select_School_Lesson(discord.ui.Select):
    def __init__(self, list, func, lesson_grade):
        super().__init__(placeholder="Select a lesson", max_values=1)
        self.__list = list
        self.__lesson_grade = lesson_grade
        self.__func = func

        match self.__func:
            case GradeManipulation.ADD_GRADE:
                for lesson in self.__list:
                    self.add_option(label=f"{lesson._get_name()}", 
                                    description=f"Teacher: {lesson._teacher._full_name()}", 
                                    value=lesson._get_id())
            case GradeManipulation.DELETE_GRADE:
                for lesson in self.__list:
                    self.add_option(label=f"{lesson._get_name()}", 
                                    description=f"Teacher: {lesson._teacher._full_name()}", 
                                    value=lesson._get_id())

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        match self.__func:
            case GradeManipulation.ADD_GRADE:
                self.__lesson_grade._set_school_lesson(lesson=School_Lesson(id=self.values[0]))
                await GradeManipulation._add_grade_to_selected_lesson(interaction=interaction, 
                                                                      lesson_grade=self.__lesson_grade)
            case GradeManipulation.DELETE_GRADE:
                self.__lesson_grade._set_school_lesson(lesson=School_Lesson(id=self.values[0]))
                await GradeManipulation._delete_grade_from_selected_lesson(interaction=interaction, 
                                                                           lesson_grade=self.__lesson_grade)

class Select_Grade_From_School_Lesson(discord.ui.Select):
    def __init__(self, lesson_grade_list, lesson_grade):
        super().__init__(placeholder="Select a grade", max_values=1)
        self.__lesson_grade = lesson_grade
        for lesson_grade in lesson_grade_list:
            value_str = f"{lesson_grade._get_id()}:{lesson_grade._get_grade()}"
            self.add_option(label=f"Grade: {lesson_grade._get_grade()}", 
                            description=None, 
                            value=value_str)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        selected_value = self.values[0]
        id, grade = selected_value.split(":")

        self.__lesson_grade._set_id(id=id)
        self.__lesson_grade._set_grade(grade=grade)

        self.__lesson_grade._delete_grade_from_database()
        await interaction.message.edit(content=f"The grade: **{self.__lesson_grade._get_grade()}** has been deleted from: ***{self.__lesson_grade._get_school_lesson()._get_name()}***, for you **{self.__lesson_grade._get_school_student()._get_givenname()}**", 
                                       view=None)

class Select_School_Lesson_View(discord.ui.View):
    def __init__(self, list, lesson_grade, func):
        super().__init__()
        self.add_item(Select_School_Lesson(list=list, lesson_grade=lesson_grade, func=func))

class Select_Grade_From_School_Lesson_View(discord.ui.View):
    def __init__(self, lesson_grade_list, lesson_grade):
        super().__init__()
        self.add_item(Select_Grade_From_School_Lesson(lesson_grade_list=lesson_grade_list, lesson_grade=lesson_grade))

class Grade(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    grade_group = GradeGroup(name="grade", description="Grade related commands")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Grade(client), guild=discord.Object(id=botConfig["hub-server-guild-id"]))