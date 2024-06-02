from datetime import date
import json


# Test Class is not implemented!
# Design a Class Architecture based on /umldiagram.puml

class Database:
    def __init__(self):
        if not self.load():
            self.teachers_table = {}
            self.students_table = {}
            self.batches_table = {}
            self.subjects_table = []

    def add_student(self, student):
        self.students_table[student.username] = {"password": student.password, "student": student}

    def add_teacher(self, teacher):
        self.teachers_table[teacher.username] = {"password": teacher.password, "teacher": teacher}

    def add_subject(self, subject):
        self.subjects_table.append(subject)

    def add_batch(self, batch):
        self.batches_table[batch.name] = batch

    def update_student(self, student_username: str, password=None, first_name=None, last_name=None):
        if password:
            self.students_table[student_username]["password"] = password
        if first_name:
            self.students_table[student_username]["student"].first_name = first_name
        if last_name:
            self.students_table[student_username]["student"].last_name = last_name

    def update_teacher(self, teacher_username: str, password=None, first_name=None, last_name=None):
        if password:
            self.teachers_table[teacher_username]["password"] = password
        if first_name:
            self.teachers_table[teacher_username]["teacher"].first_name = first_name
        if last_name:
            self.teachers_table[teacher_username]["teacher"].last_name = last_name

    def save(self):
        # Save the database to a json file
        with open("database.json", "w") as f:
            json.dump(self.__dict__, f)

    def load(self) -> bool:
        # Load the database from a json file
        try:
            with open("database.json", "r") as f:
                data = json.load(f)
                self.__dict__.update(data)

        except FileNotFoundError:
            print("Database file not found")
            return False
        else:
            return True


class Subject:
    def __init__(self, name: str):
        self.name = name


class Batch:
    def __init__(self, name: str, section: str):
        self.name = name
        self.section = section
        self.students = []  # List of students enrolled in the batch
        self.subjects = []  # List of subjects taught in the batch

    def add_student(self, student):
        self.students.append(student)

    def add_subject(self, subject):
        self.subjects.append(subject)


class Assignment:
    # Each Student has a list of assignments for each subject
    def __init__(self, name: str, subject: Subject, due_date: date):
        self.name = name
        self.due_date = due_date
        self.subject = subject
        self.status = "Pending"

    def assign_to_batch(self, subject: Subject, batch: Batch):
        """
        Assign the assignment to all students in the batch
        :param subject: Subject to which the assignment belongs
        :param batch: Batch to which the assignment is assigned
        :return:
        """
        for student in batch.students:
            student.assigments[
                subject].append(self.__copy__())  # Create a copy of the assignment and assign it to the student

    def __copy__(self):
        return Assignment(self.name, self.subject, self.due_date)


class Test:
    def __init__(self, id: int, name: str, subject: Subject, date: date):
        self.id = id
        self.name = name
        self.subject = subject
        self.date = date

    def assign_to_batch(self, batch: Batch):
        pass


class Student:
    def __init__(self, username: str, password: str, first_name: str, last_name: str, batch: Batch,
                 subjects_enrolled: list[Subject] = None, marks: dict[Subject, int] = None):
        """

        :param username: Username of the student
        :param password: Password of the student
        :param first_name: First name of the student
        :param last_name: Last name of the student
        :param batch: Batch of the student
        :param subjects_enrolled: (Optional) List of subjects enrolled, If not provided, inherits from the batch
        :param marks: (Optional) Dictionary of marks for each subject, If not provided, initializes to None
        """
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.batch = batch

        self.subjects_enrolled = subjects_enrolled if subjects_enrolled else batch.subjects
        self.attendance = dict.fromkeys(subjects_enrolled, None)  # Mapping of subject to attendance percentage
        self.assignments = dict.fromkeys(subjects_enrolled)
        self.marks = dict.fromkeys(subjects_enrolled)  # Mapping of subject to marks

    def view_marks(self):
        return self.marks  # Use the frontend to display the marks as a table

    def view_assignments(self):
        return self.assignments

    @staticmethod
    def submit_assignment(assignment: Assignment):
        assignment.status = "Submitted"

    def view_attendance(self):
        return self.attendance

    def access_test_results(self, test: Test):
        # Logic to access test results
        return


class Teacher:
    def __init__(self, username: str, password: str, first_name: str, last_name: str):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        # self.assigned_classes = []  Unused for now!

    @staticmethod
    def assign_assignment_to_class(batch, subject, assignment):
        assignment.assign_to_batch(subject, batch)

    @staticmethod
    def update_student_marks(self, subject: Subject, student: Student, marks):
        student.marks[subject] = marks

    @staticmethod
    def access_test_results(self, test: Test):
        # Logic to access test results
        pass
