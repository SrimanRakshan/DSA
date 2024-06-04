from datetime import date
import pickle


# Design a Class Architecture based on /uml_diagram.puml

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
            # Create a copy of the assignment and assign it to the student
            student.view_assignments()[subject].append(self.__copy__())

    def submit(self):
        self._submitted = True

    def __copy__(self):
        return Assignment(self.name, self.subject, self.due_date)

    def __eq__(self, other):
        if isinstance(other, Assignment):
            return self.name == other.name and self.due_date == other.due_date and self.subject == other.subject
        return False


class ClassTest:
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
            student.view_tests()[self.subject][self.name] = self.__copy__()  # {Subject : {Test : mark}}

    def getmark(self):
        return self.__mark

    def __copy__(self):
        return ClassTest(self.name, self.subject)

    def __eq__(self, other):
        if isinstance(other, ClassTest):
            return self.name == other.name and self.subject == other.subject
        return False


class User:
    """
    User class to store information about the user.
    """

    def __init__(self, username: str, password: str, first_name: str, last_name: str, contact: int):
        self.username = username
        self.__password = password
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact

    def setpassword(self, password):
        self.__password = password

    def getpassword(self):
        """A Bad Practice to expose the password. Use this method only for time being."""
        return self.__password


class Student(User):
    def __init__(self, username: str, password: str,
                 first_name: str, last_name: str, batch: Batch,
                 fee: int, roll: int,
                 contact: int,
                 attendance: dict = None,
                 subjects_enrolled: list[Subject] = None):
        """
        :param username: Username of the student
        :param password: Password of the student
        :param first_name: First name of the student
        :param last_name: Last name of the student
        :param batch: Batch of the student
        :param fee: Fees of student
        :param roll: Roll number of student
        :param contact : Phone Number of student
        :param attendance: (Optional) Dictionary of attendance for each date, If not provided, initializes to None
        :param subjects_enrolled: (Optional) List of subjects enrolled, If not provided, inherits from the batch
        """
        super().__init__(username, password, first_name, last_name, contact)
        self.roll = roll
        self.fee = fee
        self.batch = batch

        # subjects_enrolled = List[Subject]
        self.subjects_enrolled = subjects_enrolled if subjects_enrolled else batch.subjects

        # attendance = Dict[Date: bool]
        self.__attendance = attendance if attendance else {}

        # assignments = Dict[Subject:List[Assignment]]
        self.__assignments = dict.fromkeys(self.subjects_enrolled, [])

        # marks = Dict[Subject:Dict[test.name: Test]]
        self.__class_tests = dict.fromkeys(self.subjects_enrolled, {})

    def get_fee(self):
        return self.fee

    def view_tests(self):
        return self.__class_tests  # Use the frontend to display the marks as a table

    def view_assignments(self):
        return self.__assignments

    def view_attendance(self):
        return self.__attendance

    def access_all_tests(self, subject: Subject):
        return self.__class_tests[subject]  # Return all {test_name: Test} of a subject

    def access_test_results(self, test: ClassTest):
        """
        Access the marks of a student for a particular test.
        :param test: Test for which the marks are accessed
        :return:
        """
        return self.view_tests()[test.subject].get(test.name)  # Return marks of the test

    @staticmethod
    def submit_assignment(assignment: Assignment):
        """
        Submit the assignment. (Get the assignment object from the student's list of assignments)
        :param assignment:
        :return:
        """
        assignment._submitted = True


class Teacher(User):
    """
    Teacher class to store information about the teacher.
    This teacher class is a utility class (has only static methods).
    """

    def __init__(self, username: str, password: str, first_name: str, last_name: str, contact: int, salary: int,
                 join_date: date = date.today()):
        """
        :param username: Username of the teacher
        :param password: Password of the teacher
        :param first_name: First name of the teacher
        :param last_name: Last name of the teacher
        :param contact: Contact of the teacher
        :param salary: Salary of the teacher
        :param join_date:
        """
        super().__init__(username, password, first_name, last_name, contact)
        self.salary = salary
        self.join_date = join_date

    def get_salary(self):
        return self.salary

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
    def assign_test_to_class(batch: Batch, test: ClassTest):
        """
        Assign a test to a batch. (Update Marks after assigning the test)
        :param batch: Batch to which the test is assigned
        :param test: Test object to be assigned (Provide a Test object)
        :return:
        """
        test.assign_to_batch(batch)

    @staticmethod
    def get_student_attendance(student: Student, attendance_date: date):
        """
        Get the attendance of a student on a particular date.
        If keyError, add date as key and value as False.
        :param student: Student whose attendance is accessed
        :param attendance_date: Date of the attendance
        :return: Dictionary of attendance for the subject
        """
        attendance = student.view_attendance().get(attendance_date)
        if not attendance:
            student.view_attendance()[attendance_date] = False
        return student.view_attendance()[attendance_date]

    @staticmethod
    def update_student_attendance(student: Student, attendance_date: date, present: bool):
        """
        Update the attendance of a student for a particular subject.
        :param student: Student whose attendance is updated
        :param attendance_date: Date of the attendance
        :param present: Boolean value indicating whether the student is present or not
        :return:
        """
        # print(f"{student.view_attendance()=}")
        student.view_attendance()[attendance_date] = present

    @staticmethod
    def update_student_marks(student: Student, test: ClassTest, marks: int):
        """
        Update the marks of a student for a particular subject. (Assign test before updating marks)
        :param test: Test for which the marks are updated (Provide a Test object)
        :param student: Student whose marks are updated
        :param marks: Marks of the student, which is to be added
        :return:
        """
        student.view_tests()[test.subject][test.name] = marks

    @staticmethod
    def access_test_results(batch: Batch, test: ClassTest):
        """
        Access the test results of all students in a batch.
        :param batch: Batch to which the test is assigned
        :param test: Test for which the results are accessed (Provide a Test object)
        :return:
        """
        marks = {}
        for student in batch.students:
            marks[student.first_name + ' ' + student.last_name] = student.view_tests()[test.subject][test]
        return marks


class Database:
    """
    Database class to store all the data of the school.
    Batches must be created before students are added to the database.
    """

    def __init__(self, save_file='database.bin'):
        self.save_file = save_file
        if not self.load():
            self.__teachers_table = {}  # Dict[username: Dict[teacher: Teacher, status : str]]
            self.__students_table = {}  # Dict[username: Dict[student: Student, status : str]]
            self.__batches_table = {}  # Dict[batch_name: Batch]

            self.save()  # Save the database to a json file

    def display_in_terminal(self):
        print("Teachers:")
        print('First Name', 'Last Name', 'Username', 'Password', 'Contact', 'Salary', 'Status')
        for teacher in self.__teachers_table:
            print(self.__teachers_table[teacher]["teacher"].first_name,
                  self.__teachers_table[teacher]["teacher"].last_name,
                  self.__teachers_table[teacher]["teacher"].username,
                  self.__teachers_table[teacher]["teacher"].getpassword(),
                  self.__teachers_table[teacher]["teacher"].contact,
                  self.__teachers_table[teacher]["teacher"].salary, self.__teachers_table[teacher]["status"])
        print("\nStudents:")
        print('First Name', 'Last Name', 'Username', 'Password', 'Contact', 'Fee', 'Status')
        for student in self.__students_table:
            print(self.__students_table[student]["student"].first_name,
                  self.__students_table[student]["student"].last_name,
                  self.__students_table[student]["student"].username,
                  self.__students_table[student]["student"].getpassword(),
                  self.__students_table[student]["student"].contact,
                  self.__students_table[student]["student"].fee, self.__students_table[student]["status"])
        print("\nBatches:")
        print('Batch Name', 'Students', 'Subjects')
        for batch in self.__batches_table:
            print(self.__batches_table[batch].name, [i.username for i in self.__batches_table[batch].students],
                  [i.name for i in self.__batches_table[batch].subjects])

    def login(self, username, password, as_admin=False, as_teacher=False, as_student=False) -> bool:
        if as_admin:
            return True
        if as_teacher:
            account = self.__teachers_table.get(username)
            if account and password == self.__teachers_table[username]["teacher"].getpassword():
                return True
        if as_student:
            account = self.__students_table.get(username)
            if account and password == self.__students_table[username]["student"].getpassword():
                return True
        return False

    def add_student(self, student, status=False):
        """
        Add a student to the database. Also add the student to the batch. (Assuming the batch is already present)
        :param student:
        :param status: Status of Student (True: Approved, False: Waiting for approval)
        :return:
        """
        if student.username in self.__students_table:
            raise ValueError("Student already exists.")

        self.__students_table[student.username] = {"password": student.getpassword(), "student": student,
                                                   "status": status}
        self.__batches_table[student.batch.name].add_student(student)

    def add_teacher(self, teacher, status=False):
        """
        Add a teacher to the database.
        :param teacher: Teacher object
        :param status: Status of Teacher (True: Approved, False: Waiting for approval)
        :return:
        """
        if teacher.username in self.__teachers_table:
            raise ValueError("Teacher already exists.")
        self.__teachers_table[teacher.username] = {"password": teacher.getpassword, "teacher": teacher,
                                                   "status": status}

    def add_batch(self, batch):
        """
        Add a batch to the database.
        :param batch: Batch object
        :return:
        """
        if batch.name in self.__batches_table:
            raise ValueError("Batch already exists.")
        self.__batches_table[batch.name] = batch

    def get_batch(self, batch_name: str) -> Batch | None:
        """
        Get the batch object from the database.
        :param batch_name: Batch name
        :return: Batch object
        """
        return self.__batches_table.get(batch_name)

    def get_student(self, student_username: str) -> Student | None:
        """
        Get the student object from the database.
        :param student_username: Student username
        :return: Student object
        """
        student = self.__students_table.get(student_username)
        if student:
            return student["student"]
        return None

    def get_teacher(self, teacher_username: str) -> Teacher | None:
        """
        Get the teacher object from the database.
        :param teacher_username: Teacher username
        :return: Teacher object
        """
        teacher = self.__teachers_table.get(teacher_username)
        if teacher:
            return teacher["teacher"]
        return None

    def get_all_teachers(self, status=True) -> list[Teacher]:
        return [self.__teachers_table[i]["teacher"] for i in self.__teachers_table if
                self.__teachers_table[i]["status"] == status]

    def get_all_students(self, status=True) -> list[Student]:
        return [self.__students_table[i]["student"] for i in self.__students_table if
                self.__students_table[i]["status"] == status]

    def get_total_salary(self, status=True) -> int:
        return sum([self.__teachers_table[i]["teacher"].get_salary() for i in self.__teachers_table if
                    self.__teachers_table[i]["status"] == status])

    def get_total_fees(self, status=True) -> int:
        return sum([self.__students_table[i]["student"].get_fee() for i in self.__students_table if
                    self.__students_table[i]["status"] == status])

    def update_student(self, student_username: str, password=None, first_name=None, last_name=None,
                       batch : Batch=None,fee=None, contact=None, roll=None, status=None):
        """
        Update the student details in the database. (Only the ones that are defined at login)
        :param batch: Batch of the Student (Optional) (Removes student from current batch and adds to new batch)
        :param student_username: Student username
        :param password: Password of the student (Optional)
        :param first_name: First name of the student (Optional)
        :param last_name: Last name of the student (Optional)
        :param fee: Fee of student
        :param contact: Contact of student
        :param roll: Roll of student
        :param status: Status of Student (True: Approved, False: Waiting for approval)
        :return:
        """
        student = self.__students_table.get(student_username)
        if not student:
            raise ValueError("Student not found.")

        if password:
            student["student"].setpassword(password)
        if first_name:
            student["student"].first_name = first_name
        if last_name:
            student["student"].last_name = last_name
        if fee:
            student["student"].fee = fee
        if status:
            student["status"] = status
        if contact:
            student["student"].contact = contact
        if roll:
            student["student"].roll = roll
        if batch:
            old_batch = self.__batches_table[student["student"].batch.name]
            old_batch.students.remove(student["student"])
            student["student"].batch = batch
            batch.students.append(student["student"])
        # if student_username:
        #     student = self.__students_table.pop(student["student"].username)
        #     student["student"].username = student_username
        #     self.__students_table[student_username] = student

    def update_teacher(self, teacher_username: str,
                       password: str = None,
                       first_name: str = None,
                       last_name: str = None,
                       contact: str = None,
                       salary: str = None,
                       status: bool = None, ):
        """
        Update the teacher details in the database.
        :param teacher_username: Teacher username (current)
        :param password: Password of the teacher (Optional)
        :param first_name: First name of the teacher (Optional)
        :param last_name: Last name of the teacher (Optional)
        :param contact: Contact of the teacher (Optional)
        :param salary: Salary of Teacher (Optional)
        :param status: Status of Teacher (Optional)(True: Approved, False: Waiting for approval)
        :return:
        """
        teacher = self.__teachers_table.get(teacher_username)
        if not teacher:
            raise ValueError("Teacher not found.")

        if password:
            teacher["teacher"].setpassword(password)
        if first_name:
            teacher["teacher"].first_name = first_name
        if last_name:
            teacher["teacher"].last_name = last_name
        if contact:
            teacher["teacher"].contact = contact
        if salary:
            teacher["teacher"].salary = salary
        if status:
            teacher["status"] = status

    def update_batch(self, batch_name: str, students=None, subjects=None):
        """
        Update the batch details in the database.
        :param batch_name: Batch name
        :param students: List of students in the batch (Optional)
        :param subjects: List of subjects in the batch (Optional)
        :return:
        """
        if batch_name not in self.__batches_table:
            raise ValueError("Batch not found.")
        if students:
            self.__batches_table[batch_name].students = students
        if subjects:
            self.__batches_table[batch_name].subjects = subjects

    def get_student_count(self, status=None) -> int:
        if status is not None:
            return sum([1 for i in self.__students_table if self.__students_table[i]["status"] == status])
        else:
            return len(self.__students_table)

    def get_teacher_count(self, status=None) -> int:
        if status is not None:
            return sum([1 for i in self.__teachers_table if self.__teachers_table[i]["status"] == status])
        else:
            return len(self.__teachers_table)

    def remove_teacher(self, teacher_username: str):
        if teacher_username not in self.__teachers_table:
            raise ValueError("Teacher not found.")
        self.__teachers_table.pop(teacher_username)

    def remove_student(self, student_username: str):
        if student_username not in self.__students_table:
            raise ValueError("Student not found.")
        student = self.__students_table.pop(student_username)["student"]
        batch = self.__batches_table[student.batch.name]
        batch.students.remove(student)

    def save(self):
        # Save the database to a json file
        with open(self.save_file, "wb") as f:
            pickle.dump([self.__students_table, self.__teachers_table, self.__batches_table], f)

    def load(self) -> bool:
        # Load the database from a json file
        try:
            with open(self.save_file, "rb") as f:
                data = pickle.load(f)
                self.__students_table = data[0]
                self.__teachers_table = data[1]
                self.__batches_table = data[2]

        except FileNotFoundError:
            print("...Initializing a new database.")
            return False
        else:
            return True

    def reset(self):
        # Remove the json file
        import os
        print("trying to remove database file")
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
            self.__teachers_table = {}
            self.__batches_table = {}
            self.__students_table = {}
