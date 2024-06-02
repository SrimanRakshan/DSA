from datetime import date
import json


# ClassroomInteraction is not implemented yet!
# Design a Class Architecture based on /uml_diagram.puml

class Database:
    """
    Database class to store all the data of the school.
    Batches must be created before students are added to the database.
    """

    def __init__(self):
        if not self.load():
            self.__teachers_table = {}  # Dict[username: Dict[password: str, teacher: Teacher]]
            self.__students_table = {}  # Dict[username: Dict[password: str, student: Student]]
            self.__batches_table = {}  # Dict[batch_name: Batch]

            self.save()  # Save the database to a json file

    def add_student(self, student):
        """
        Add a student to the database. Also add the student to the batch. (Assuming the batch is already present)
        :param student:
        :return:
        """
        self.__students_table[student.username] = {"password": student.__password, "student": student}
        self.__batches_table[student.batch.name].add_student(student)

    def add_teacher(self, teacher):
        """
        Add a teacher to the database.
        :param teacher: Teacher object
        :return:
        """
        self.__teachers_table[teacher.username] = {"password": teacher.__password, "teacher": teacher}

    def add_batch(self, batch):
        """
        Add a batch to the database.
        :param batch: Batch object
        :return:
        """
        self.__batches_table[batch.name] = batch

    def update_student(self, student_username: str, password=None, first_name=None, last_name=None):
        """
        Update the student details in the database.
        :param student_username: Student username
        :param password: Password of the student (Optional)
        :param first_name: First name of the student (Optional)
        :param last_name: Last name of the student (Optional)
        :return:
        """
        if password:
            self.__students_table[student_username]["password"] = password
        if first_name:
            self.__students_table[student_username]["student"].first_name = first_name
        if last_name:
            self.__students_table[student_username]["student"].last_name = last_name

    def update_teacher(self, teacher_username: str, password=None, first_name=None, last_name=None):
        """
        Update the teacher details in the database.
        :param teacher_username: Teacher username
        :param password: Password of the teacher (Optional)
        :param first_name: First name of the teacher (Optional)
        :param last_name: Last name of the teacher (Optional)
        :return:
        """
        if password:
            self.__teachers_table[teacher_username]["password"] = password
        if first_name:
            self.__teachers_table[teacher_username]["teacher"].first_name = first_name
        if last_name:
            self.__teachers_table[teacher_username]["teacher"].last_name = last_name

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
    def __init__(self, name: str):
        self.name = name
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
        self._submitted = False

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

    def submit(self):
        self._submitted = True

    def __copy__(self):
        return Assignment(self.name, self.subject, self.due_date)


class Test:
    def __init__(self, name: str, subject: Subject):
        self.name = name
        self.subject = subject
        self.__mark = None

    def assign_to_batch(self, batch: Batch):
        """
        Assign the test to all students in the batch.
        :param batch: Batch to which the test is assigned
        :return:
        """
        for student in batch.students:
            student.tests.append(self.__copy__())

    def getmark(self):
        return self.__mark

    def __copy__(self):
        return Test(self.name, self.subject)


class Student:
    def __init__(self, username: str, password: str, first_name: str, last_name: str, batch: Batch,
                 attendance: dict = None,
                 subjects_enrolled: list[Subject] = None):
        """
        :param username: Username of the student
        :param password: Password of the student
        :param first_name: First name of the student
        :param last_name: Last name of the student
        :param batch: Batch of the student
        :param attendance: (Optional) Dictionary of attendance for each subject, If not provided, initializes to None
        :param subjects_enrolled: (Optional) List of subjects enrolled, If not provided, inherits from the batch
        """
        self.username = username
        self.__password = password
        self.first_name = first_name
        self.last_name = last_name
        self.batch = batch

        # subjects_enrolled = List[Subject]
        self.subjects_enrolled = subjects_enrolled if subjects_enrolled else batch.subjects

        # attendance = Dict[Subject:Dict[Date: bool]]
        self.__attendance = attendance if attendance else dict.fromkeys(subjects_enrolled, None)

        # assignments = Dict[Subject:List[Assignment]]
        self.__assignments = dict.fromkeys(subjects_enrolled)

        # marks = Dict[Subject:Dict[Test: float]]
        self.__marks = dict.fromkeys(subjects_enrolled, {})

    def view_marks(self):
        return self.__marks  # Use the frontend to display the marks as a table

    def view_assignments(self):
        return self.__assignments

    def view_attendance(self):
        return self.__attendance

    def access_all_tests(self, subject: Subject):
        return self.__marks[subject]  # Return {Test: marks} for the subject

    def access_test_results(self, test: Test):
        return self.view_marks()[test.subject][test]

    @staticmethod
    def submit_assignment(assignment: Assignment):
        """
        Submit the assignment. (Get the assignment object from the student's list of assignments)
        :param assignment:
        :return:
        """
        assignment._submitted = True


class Teacher:
    """
    Teacher class to store information about the teacher.
    This teacher class is a utility class (has only static methods).
    """

    def __init__(self, username: str, password: str, first_name: str, last_name: str):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def assign_assignment_to_class(batch: Batch, subject: Subject, assignment: Assignment):
        """
        Assign an assignment to a batch.
        :param batch: Batch to which the assignment is assigned
        :param subject: Subject to which the assignment belongs
        :param assignment: Assignment object to be assigned (Provide an Assignment object)
        :return:
        """
        assignment.assign_to_batch(subject, batch)

    @staticmethod
    def assign_test_to_class(batch: Batch, test: Test):
        """
        Assign a test to a batch. (Update Marks after assigning the test)
        :param batch: Batch to which the test is assigned
        :param test: Test object to be assigned (Provide a Test object)
        :return:
        """
        test.assign_to_batch(batch)

    @staticmethod
    def update_student_attendance(student: Student, subject: Subject, date: date, present: bool):
        """
        Update the attendance of a student for a particular subject.
        :param student: Student whose attendance is updated
        :param subject: Subject for which the attendance is updated
        :param date: Date of the attendance
        :param present: Boolean value indicating whether the student is present or not
        :return:
        """
        student.view_attendance()[subject][date] = present

    @staticmethod
    def update_student_marks(student: Student, test: Test):
        """
        Update the marks of a student for a particular subject. (Assign test before updating marks)
        :param test: Test for which the marks are updated (Provide a Test object)
        :param student: Student whose marks are updated
        :return:
        """
        student.view_marks()[test.subject][test] = test.getmark()

    @staticmethod
    def access_test_results(batch: Batch, test: Test):
        """
        Access the test results of all students in a batch.
        :param batch: Batch to which the test is assigned
        :param test: Test for which the results are accessed (Provide a Test object)
        :return:
        """
        marks = {}
        for student in batch.students:
            marks[student.first_name + ' ' + student.last_name] = student.__marks[test.subject][test]
        return marks
