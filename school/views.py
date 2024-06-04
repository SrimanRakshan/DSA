from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.mail import send_mail

import basic_classes as fe

db = fe.Database()
for i in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']:
    try:
        db.add_batch(fe.Batch(i))
    except ValueError:
        pass


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/index.html')


# for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return HttpResponseRedirect('afterlogin')
        else:
            logout(request)
            messages.error(request, "Invalid login credentials")
    return render(request, 'school/adminclick.html')


# for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        if is_teacher(request.user):
            return HttpResponseRedirect('afterlogin')
        else:
            logout(request)
            messages.error(request, "Invalid login credentials")
    return render(request, 'school/teacherclick.html')


# for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        if is_student(request.user):
            return HttpResponseRedirect('afterlogin')
        else:
            logout(request)
            messages.error(request, "Invalid login credentials")
    return render(request, 'school/studentclick.html')


def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request, 'school/adminsignup.html', {'form': form})


def student_signup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            student = fe.Student(form1.cleaned_data['username'],
                                 form1.cleaned_data['password'],
                                 form1.cleaned_data['first_name'],
                                 form1.cleaned_data['last_name'],
                                 db.get_batch(form2.cleaned_data['cl']),
                                 form2.cleaned_data['fee'],
                                 form2.cleaned_data['roll'],
                                 form2.cleaned_data['mobile'])
            db.add_student(student)
            db.save()

            # Django Implementation
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request, 'school/studentsignup.html', context=mydict)


def teacher_signup_view(request):
    form1 = forms.TeacherUserForm()
    form2 = forms.TeacherExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST)
        form2 = forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            teacher = fe.Teacher(username=form1.cleaned_data['username'],
                                 password=form1.cleaned_data['password'],
                                 first_name=form1.cleaned_data['first_name'],
                                 last_name=form1.cleaned_data['last_name'],
                                 contact=form2.cleaned_data['mobile'],
                                 salary=form2.cleaned_data['salary']
                                 )
            db.add_teacher(teacher)
            db.save()

            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request, 'school/teachersignup.html', context=mydict)


# for checking user is teacher , student or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval = models.TeacherExtra.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request, 'school/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval = models.StudentExtra.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request, 'school/student_wait_for_approval.html')


# for dashboard of admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount = db.get_teacher_count(status=True)
    pendingteachercount = db.get_teacher_count(status=False)

    studentcount = db.get_student_count(status=True)
    pendingstudentcount = db.get_student_count(status=False)

    teachersalary = db.get_total_salary()
    pendingteachersalary = db.get_total_salary(status=False)

    studentfee = db.get_total_fees()
    pendingstudentfee = db.get_total_fees(status=False)

    notice = models.Notice.objects.all()

    # aggregate function return dictionary so fetch data from dictionay
    mydict = {
        'teachercount': teachercount,
        'pendingteachercount': pendingteachercount,

        'studentcount': studentcount,
        'pendingstudentcount': pendingstudentcount,

        'teachersalary': teachersalary,
        'pendingteachersalary': pendingteachersalary,

        'studentfee': studentfee,
        'pendingstudentfee': pendingstudentfee,

        'notice': notice

    }

    return render(request, 'school/admin_dashboard.html', context=mydict)


# for teacher section by admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request, 'school/admin_teacher.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1 = forms.TeacherUserForm()
    form2 = forms.TeacherExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST)
        form2 = forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            teacher = fe.Teacher(username=form1.cleaned_data['username'],
                                 password=form1.cleaned_data['password'],
                                 first_name=form1.cleaned_data['first_name'],
                                 last_name=form1.cleaned_data['last_name'],
                                 contact=form2.cleaned_data['mobile'],
                                 salary=form2.cleaned_data['salary']
                                 )
            db.add_teacher(teacher, status=True)
            db.save()

            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request, 'school/admin_add_teacher.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers = db.get_all_teachers(status=True)
    return render(request, 'school/admin_view_teacher.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers = db.get_all_teachers(status=False)
    return render(request, 'school/admin_approve_teacher.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request, pk):
    user = models.User.objects.get(username=pk)
    teacher = models.TeacherExtra.objects.get(user=user)
    teacher.status = True
    teacher.save()

    db.update_teacher(pk, status=True)
    db.save()
    return redirect(reverse('admin-approve-teacher'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request, pk):
    user = models.User.objects.get(username=pk)
    teacher = models.TeacherExtra.objects.get(user=user)
    user.delete()
    teacher.delete()

    db.remove_teacher(pk)
    db.save()
    return redirect('admin-approve-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request, pk):
    user = models.User.objects.get(username=pk)
    teacher = models.TeacherExtra.objects.get(user=user)
    user.delete()
    teacher.delete()

    db.remove_teacher(pk)
    db.save()
    return redirect('admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request, pk):
    teacher_username = db.get_teacher(pk).username
    user = models.User.objects.get(username=teacher_username)
    teacher = models.TeacherExtra.objects.get(user=user)
    form1 = forms.TeacherUserForm(instance=user)
    form2 = forms.TeacherExtraForm(instance=teacher)
    mydict = {'form1': form1, 'form2': form2}

    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST, instance=user)
        form2 = forms.TeacherExtraForm(request.POST, instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            db.update_teacher(teacher_username=teacher_username,
                              # form1.cleaned_data['password'],
                              first_name=form1.cleaned_data['first_name'],
                              last_name=form1.cleaned_data['last_name'],
                              contact=form2.cleaned_data['mobile'],
                              salary=form2.cleaned_data['salary']
                              )
            db.save()

            user = form1.save()  # Changing UserName doesn't work as of now
            # user.set_password(user.password) # Changing Password doesn't work as of now
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            return redirect('admin-view-teacher')
    return render(request, 'school/admin_update_teacher.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers = db.get_all_teachers(status=True)
    return render(request, 'school/admin_view_teacher_salary.html', {'teachers': teachers})


# for student by admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request, 'school/admin_student.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            student = fe.Student(username=form1.cleaned_data['username'],
                                 password=form1.cleaned_data['password'],
                                 first_name=form1.cleaned_data['first_name'],
                                 last_name=form1.cleaned_data['last_name'],
                                 contact=form2.cleaned_data['mobile'],
                                 batch=db.get_batch(form2.cleaned_data['cl']),
                                 fee=form2.cleaned_data['fee'],
                                 roll=form2.cleaned_data['roll']
                                 )
            db.add_student(student, status=True)
            db.save()

            print("form is valid")
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request, 'school/admin_add_student.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    # students = models.StudentExtra.objects.all().filter(status=True)
    students = db.get_all_students(status=True)
    return render(request, 'school/admin_view_student.html', {'students': students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request, pk):
    user = models.User.objects.get(username=pk)
    student = models.StudentExtra.objects.get(user=user)
    user.delete()
    student.delete()

    db.remove_student(pk)
    db.save()
    return redirect('admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request, pk):
    user = models.User.objects.get(username=pk)
    student = models.StudentExtra.objects.get(user=user)
    user.delete()
    student.delete()

    db.remove_student(pk)
    db.save()
    return redirect('admin-approve-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request, pk):
    student_username = db.get_student(pk).username
    user = models.User.objects.get(username=student_username)
    student = models.StudentExtra.objects.get(user=user)
    form1 = forms.StudentUserForm(instance=user)
    form2 = forms.StudentExtraForm(instance=student)
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST, instance=user)
        form2 = forms.StudentExtraForm(request.POST, instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            db.update_student(student_username=student_username,
                              # form1.cleaned_data['password'],
                              first_name=form1.cleaned_data['first_name'],
                              last_name=form1.cleaned_data['last_name'],
                              contact=form2.cleaned_data['mobile'],
                              fee=form2.cleaned_data['fee'],
                              batch=db.get_batch(form2.cleaned_data['cl']),
                              roll=form2.cleaned_data['roll']
                              )
            db.save()

            user = form1.save()
            # user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            return redirect('admin-view-student')
    return render(request, 'school/admin_update_student.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students = db.get_all_students(status=False)
    return render(request, 'school/admin_approve_student.html', {'students': students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request, pk):
    user = models.User.objects.get(username=pk)
    students = models.StudentExtra.objects.get(user=user)
    students.status = True
    students.save()

    db.update_student(pk, status=True)
    db.save()
    return redirect(reverse('admin-approve-student'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request):
    students = db.get_all_students(status=True)
    return render(request, 'school/admin_view_student_fee.html', {'students': students})


# attendance related view
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request, 'school/admin_attendance.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request, cl):
    students = models.StudentExtra.objects.all().filter(cl=cl)
    print(students)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('present_status')
            date = form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel = models.Attendance()
                AttendanceModel.cl = cl
                AttendanceModel.date = date
                AttendanceModel.present_status = Attendances[i]
                AttendanceModel.roll = students[i].roll
                AttendanceModel.save()
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request, 'school/admin_take_attendance.html', {'students': students, 'aform': aform})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request, cl):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = models.Attendance.objects.all().filter(date=date, cl=cl)
            studentdata = models.StudentExtra.objects.all().filter(cl=cl)
            mylist = zip(attendancedata, studentdata)
            return render(request, 'school/admin_view_attendance_page.html', {'cl': cl, 'mylist': mylist, 'date': date})
        else:
            print('form invalid')
    return render(request, 'school/admin_view_attendance_ask_date.html', {'cl': cl, 'form': form})


# fee related view by admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fee_view(request):
    return render(request, 'school/admin_fee.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fee_view(request, cl):
    batch = db.get_batch(cl)
    feedetails = batch.students
    return render(request, 'school/admin_view_fee.html', {'feedetails': feedetails, 'cl': cl})


# notice related views
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form = forms.NoticeForm()
    if request.method == 'POST':
        form = forms.NoticeForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.by = request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request, 'school/admin_notice.html', {'form': form})


# for TEACHER  LOGIN    SECTION
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    # teacherdata = models.TeacherExtra.objects.all().filter(status=True, user_id=request.user.id)
    teacher = db.get_teacher(request.user.username)
    notice = models.Notice.objects.all()
    mydict = {
        'salary': teacher.salary,
        'mobile': teacher.contact,
        'date': teacher.join_date,
        'notice': notice
    }
    return render(request, 'school/teacher_dashboard.html', context=mydict)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request, 'school/teacher_attendance.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request, cl):
    students = models.StudentExtra.objects.all().filter(cl=cl)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('present_status')
            date = form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel = models.Attendance()
                AttendanceModel.cl = cl
                AttendanceModel.date = date
                AttendanceModel.present_status = Attendances[i]
                AttendanceModel.roll = students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request, 'school/teacher_take_attendance.html', {'students': students, 'aform': aform})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request, cl):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = models.Attendance.objects.all().filter(date=date, cl=cl)
            studentdata = models.StudentExtra.objects.all().filter(cl=cl)
            mylist = zip(attendancedata, studentdata)
            return render(request, 'school/teacher_view_attendance_page.html',
                          {'cl': cl, 'mylist': mylist, 'date': date})
        else:
            print('form invalid')
    return render(request, 'school/teacher_view_attendance_ask_date.html', {'cl': cl, 'form': form})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form = forms.NoticeForm()
    if request.method == 'POST':
        form = forms.NoticeForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.by = request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request, 'school/teacher_notice.html', {'form': form})


# FOR STUDENT AFTER THEIR Login
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    # studentdata = models.StudentExtra.objects.all().filter(status=True, user_id=request.user.id)
    student = db.get_student(request.user.username)
    notice = models.Notice.objects.all()
    mydict = {
        'roll': student.roll,
        'mobile': student.contact,
        'fee': student.fee,
        'notice': notice
    }
    return render(request, 'school/student_dashboard.html', context=mydict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            studentdata = models.StudentExtra.objects.all().filter(user_id=request.user.id, status=True)
            attendancedata = models.Attendance.objects.all().filter(date=date, cl=studentdata[0].cl,
                                                                    roll=studentdata[0].roll)
            mylist = zip(attendancedata, studentdata)
            return render(request, 'school/student_view_attendance_page.html', {'mylist': mylist, 'date': date})
        else:
            print('form invalid')
    return render(request, 'school/student_view_attendance_ask_date.html', {'form': form})


# for about us and contact us
def aboutus_view(request):
    return render(request, 'school/aboutus.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'school/contactussuccess.html')
    return render(request, 'school/contactus.html', {'form': sub})


def logout_view(request):
    logout(request)
    return render(request, 'school/logout.html')


def index_view(request):
    return render(request, 'school/index.html')
