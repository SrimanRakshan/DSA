from basic_classes import *

db = Database()
db.reset()

# Add a batch
batch = Batch("Class 1")
batch.add_subject("Maths")
batch.add_subject("Science")
batch.add_subject("Social")
batch.add_subject("English")
batch.add_subject("Tamil")
db.add_batch(batch)

# Add a student (Need to provide batch)
student = Student("mNandhu", "123", "Kiruthik", "Nandhan", batch)
db.add_student(student)

# Add a teacher
teacher = Teacher("SrimanRakshan", "123", "Sriman", "Rakshan")
db.add_teacher(teacher)

db.save()   # ALWAYS SAVE DATA MANUALLY

# Check History
del db

db = Database()
student = db.get_student("mNandhu")
teacher = db.get_teacher("SrimanRakshan")
batch = db.get_batch("Class 1")
print(student.username)
print(teacher.username)
print(batch.name,batch.subjects)