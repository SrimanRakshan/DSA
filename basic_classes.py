from datetime import date


# Design a Class Architecture based on /umldiagram.puml

class Database:
    def __init__(self):
        self.students_table = []
        self.teachers_table = []
        self.subjects_table = []
        self.batches_table = []
        self.assignments_table = []
        self.tests_table = []

    def add_student(self, student):
        self.students_table.append(student)

    def add_teacher(self, teacher):
        self.teachers_table.append(teacher)

    def add_subject(self, subject):
        self.subjects_table.append(subject)

    def add_batch(self, batch):
        self.batches_table.append(batch)

    def add_assignment(self, assignment):
        self.assignments_table.append(assignment)

    def add_test(self, test):
        self.tests_table.append(test)

    # Update methods for each table would be implemented here
    def update_student(self, student_id: int):
        pass

    def update_teacher(self, teacher_id: int):
        pass

    def update_batch(self, batch_id: int):
        pass


class Subject:
    def __init__(self, id: int, name: str):
        self.id = id
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

    def assign_to_batch(self, batch: Batch):
        pass


class Test:
    def __init__(self, id: int, name: str, subject: Subject, date: date):
        self.id = id
        self.name = name
        self.subject = subject
        self.date = date

    def assign_to_batch(self, batch: Batch):
        pass


class Student:
    def __init__(self, id: int, username: str, password: str, name: str, subjects_enrolled: list[Subject]):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.subjects_enrolled = subjects_enrolled
        self.attendance = dict.fromkeys(subjects_enrolled, None)  # Mapping of subject to attendance percentage
        # self.marks = dict.fromkeys(subjects_enrolled)  # List of marks for each subject (represents a mapping of
        # subject to marks)

    def login(self):
        # Login logic here
        pass

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


class Teacher:
    def __init__(self, id: int, username: str, password: str, name: str):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.assigned_classes = []

    def login(self):
        # Login logic here
        pass

    def edit_student_credentials(self, student_id, new_username, new_password):
        # Logic to edit student credentials
        pass

    def assign_assignment_to_class(self, batch_id, assignment):
        # Logic to assign assignment to class
        pass

    def update_student_marks(self, student_id, marks):
        # Logic to update student marks
        pass
