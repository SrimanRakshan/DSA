from datetime import date
import json


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

    # Update methods for each table would be implemented here
    def update_student(self, student_username: str, password=None, first_name=None, last_name=None, attendance=None,
                       marks=None):
        if password:
            self.students_table[student_username]["password"] = password
        if first_name:
            self.students_table[student_username]["student"].first_name = first_name
        if last_name:
            self.students_table[student_username]["student"].last_name = last_name

    def update_teacher(self, teacher_username: str, **kwargs):
        for attr, value in kwargs.items():
            self.teachers_table[teacher_username]["teacher"].attr = value

    def update_batch(self, batch_id: int):
        pass

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
    def __init__(self, id: int, name: str, section: str):
        self.id = id
        self.name = name
        self.section = section
        self.students = []  # List of students enrolled in the batch
        self.subjects = []  # List of subjects taught in the batch

    def add_student(self, student):
        self.students.append(student)

    def add_subject(self, subject):
        self.subjects.append(subject)


class Assignment:
    def __init__(self, id: int, name: str, subject: Subject, due_date: date):
        self.id = id
        self.name = name
        self.due_date = due_date
        self.subject = subject
        # self.submissions = []

    def assign_to_batch(self, subject: Subject, batch: Batch):
        for student in batch.students:
            student.assigments[subject] = self


class Test:
    def __init__(self, id: int, name: str, subject: Subject, date: date):
        self.id = id
        self.name = name
        self.subject = subject
        self.date = date

    def assign_to_batch(self, batch: Batch):
        pass


class Teacher:
    def __init__(self, username: str, password: str, first_name: str, last_name: str):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.assigned_classes = []

    @staticmethod
    def assign_assignment_to_class(batch, subject, assignment):
        assignment.assign_to_batch(subject, batch)

    def update_student_marks(self, student_username, marks):
        # Logic to update student marks
        pass

    def access_test_results(self, test: Test):
        # Logic to access test results
        pass


class Student:
    def __init__(self, username: str, password: str, first_name: str, last_name: str, batch: Batch,
                 subjects_enrolled: list[Subject] = []):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.batch = batch
        self.attendance = dict.fromkeys(subjects_enrolled, None)  # Mapping of subject to attendance percentage
        self.assignments = dict.fromkeys(subjects_enrolled)
        # self.marks = dict.fromkeys(subjects_enrolled)  # List of marks for each subject (represents a mapping of
        # subject to marks)

    def view_marks(self):
        # Logic to view marks
        pass

    def submit_assignment(self, assignment: Assignment):
        # Logic to submit assignment
        pass

    def view_attendance(self):
        # Logic to view attendance
        pass

    def access_test_results(self, test: Test):
        # Logic to access test results
        pass
