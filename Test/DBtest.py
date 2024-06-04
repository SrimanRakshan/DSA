import unittest
from basic_classes import *
import datetime


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.database = Database('testDatabase.bin')
        self.database.reset()

        self.batch = Batch('batch1')
        self.subject = Subject('Math')

        self.batch.add_subject(self.subject)

        self.student = Student('student1', 'password', 'John', 'Doe', self.batch, 1000, 1, 1234567890)
        self.teacher = Teacher('teacher1', 'password', 'Jane', 'Doe', 5000, 12345)

        self.assignment = Assignment('Assignment1', self.subject, due_date=datetime.date.today())
        self.assignment.assign_to_batch(self.subject, self.batch)

        self.test = ClassTest('Test1', self.subject)
        self.test.assign_to_batch(self.batch)

        self.database.add_batch(self.batch)
        # Student, Teacher, Batch are added to the database in the tests

    def test_student_addition(self):
        self.database.add_student(self.student)
        self.assertEqual(self.database.get_student('student1'), self.student)

    def test_teacher_addition(self):
        self.database.add_teacher(self.teacher)
        self.assertEqual(self.database.get_teacher('teacher1'), self.teacher)

    def test_student_removal(self):
        self.database.add_student(self.student)
        self.database.remove_student('student1')
        self.assertIsNone(self.database.get_student('student1'))

    def test_teacher_removal(self):
        self.database.add_teacher(self.teacher)
        self.database.remove_teacher('teacher1')
        self.assertIsNone(self.database.get_teacher('teacher1'))

    def test_student_login(self):
        self.database.add_student(self.student)
        self.assertTrue(self.database.login('student1', 'password', as_student=True))

    def test_teacher_login(self):
        self.database.add_teacher(self.teacher)
        self.assertTrue(self.database.login('teacher1', 'password', as_teacher=True))

    def test_incorrect_login(self):
        self.assertFalse(self.database.login('student1', 'wrong_password', as_student=True))
        self.assertFalse(self.database.login('teacher1', 'wrong_password', as_teacher=True))

    def test_batch_addition(self):
        test_batch = Batch('batch2')
        self.database.add_batch(test_batch)  # Empty batch to test
        self.assertEqual(self.database.get_batch('batch2'), test_batch)

    def test_update_student(self):
        self.database.add_student(self.student)
        self.database.update_student('student1', password='newpassword', first_name='NewJohn', last_name='NewDoe',
                                     status=True, fee=2000)
        updated_student = self.database.get_student('student1')
        self.assertEqual(updated_student.getpassword(), 'newpassword')
        self.assertEqual(updated_student.first_name, 'NewJohn')
        self.assertEqual(updated_student.last_name, 'NewDoe')
        self.assertEqual(updated_student.get_fee(), 2000)

    def test_update_teacher(self):
        self.database.add_teacher(self.teacher)
        self.database.update_teacher('teacher1',
                                     password='newpassword',
                                     first_name='NewJane',
                                     last_name='NewDoe',
                                     status=True, salary=6000)
        updated_teacher = self.database.get_teacher('teacher1')
        self.assertEqual(updated_teacher.getpassword(), 'newpassword')
        self.assertEqual(updated_teacher.first_name, 'NewJane')
        self.assertEqual(updated_teacher.last_name, 'NewDoe')
        self.assertEqual(updated_teacher.get_salary(), 6000)

    def test_update_batch(self):
        # self.database.add_batch(self.batch)
        new_students = [Student('student2', 'password', 'John', 'Doe', Batch('batch1'), 1000, 2, 1234567890)]
        new_subjects = [Subject('Math')]
        self.database.update_batch('batch1', students=new_students, subjects=new_subjects)
        updated_batch = self.database.get_batch('batch1')
        self.assertEqual(updated_batch.students, new_students)
        self.assertEqual(updated_batch.subjects, new_subjects)

    def test_get_total_salary(self):
        self.database.add_teacher(self.teacher)
        self.assertEqual(self.database.get_total_salary(), 12345)

    def test_get_total_fees(self):
        self.database.add_student(self.student)
        self.assertEqual(self.database.get_total_fees(), 1000)

    def test_get_student_count(self):
        self.database.add_student(self.student)
        self.assertEqual(self.database.get_student_count(), 1)

    def test_get_teacher_count(self):
        self.database.add_teacher(self.teacher)
        self.assertEqual(self.database.get_teacher_count(), 1)

    def test_reset(self):
        self.database.add_student(self.student)
        self.database.add_teacher(self.teacher)
        self.database.reset()
        self.assertEqual(self.database.get_student_count(), 0)
        self.assertEqual(self.database.get_teacher_count(), 0)

    # Student class methods tests
    def test_student_view_marks(self):
        self.database.add_student(self.student)
        self.assertIsNotNone(self.student.view_tests())

    def test_student_view_assignments(self):
        self.database.add_student(self.student)
        self.assertIsNotNone(self.student.view_assignments())

    def test_student_view_attendance(self):
        self.database.add_student(self.student)
        self.assertIsNotNone(self.student.view_attendance())

    def test_student_access_all_tests(self):
        self.database.add_student(self.student)
        self.assertIsNotNone(self.student.access_all_tests(self.subject))

    def test_student_access_test_results(self):
        self.database.add_student(self.student)
        self.test.assign_to_batch(self.batch)
        self.teacher.update_student_marks(self.student, self.test, 90)
        self.assertIsNotNone(self.student.access_test_results(self.test))

    def test_student_submit_assignment(self):
        self.database.add_student(self.student)
        self.student.submit_assignment(self.assignment)
        self.assertTrue(self.assignment._submitted)

    # Teacher class methods tests
    def test_teacher_assign_assignment_to_class(self):
        self.database.add_student(self.student)
        self.database.add_teacher(self.teacher)
        self.teacher.assign_assignment_to_class(self.batch, self.subject, self.assignment)

        self.assertIn(self.assignment, self.student.view_assignments()[self.subject])

    def test_teacher_assign_test_to_class(self):
        self.database.add_student(self.student)
        self.database.add_teacher(self.teacher)
        self.teacher.assign_test_to_class(self.batch, self.test)
        self.assertIn(self.test.name, self.student.view_tests()[self.subject])

    def test_teacher_get_student_attendance(self):
        self.database.add_teacher(self.teacher)
        self.database.add_student(self.student)
        attendance_date = date.today()
        self.assertIsNotNone(self.teacher.get_student_attendance(self.student, attendance_date))

    def test_teacher_update_student_attendance(self):
        self.database.add_teacher(self.teacher)
        self.database.add_student(self.student)
        attendance_date = date.today()
        self.teacher.update_student_attendance(self.student, attendance_date, True)
        self.assertTrue(self.student.view_attendance()[attendance_date])

    def test_teacher_update_student_marks(self):
        self.database.add_teacher(self.teacher)
        self.database.add_student(self.student)
        self.teacher.update_student_marks(self.student, self.test, 90)
        self.assertIsNotNone(self.student.view_tests()[self.test.subject][self.test.name])

    def test_teacher_access_test_results(self):
        self.database.add_teacher(self.teacher)
        # self.database.add_batch(self.batch)
        self.assertIsNotNone(self.teacher.access_test_results(self.batch, self.test))

    def test_add_existing_student(self):
        self.database.add_student(self.student)
        with self.assertRaises(ValueError):
            self.database.add_student(self.student)

    def test_remove_nonexistent_student(self):
        with self.assertRaises(ValueError):
            self.database.remove_student('nonexistent_student')

    def test_update_nonexistent_student(self):
        with self.assertRaises(ValueError):
            self.database.update_student('nonexistent_student', password='newpassword')

    def test_login_nonexistent_user(self):
        self.assertFalse(self.database.login('nonexistent_user', 'password', as_student=True))

    def test_add_existing_batch(self):
        with self.assertRaises(ValueError):
            self.database.add_batch(self.batch)

    def test_update_nonexistent_batch(self):
        with self.assertRaises(ValueError):
            self.database.update_batch('nonexistent_batch', students=[], subjects=[])


if __name__ == '__main__':
    unittest.main()
