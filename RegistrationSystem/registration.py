import registrar
import pandas as pd
import datetime
import pickle

print('Welcome​ ​to​ ​the​ ​Registration​ ​System')

optional = input('Would you like to load existing data? Enter Yes or No: ')
optional.lower()
if optional == 'yes':
    file_path = input('Please enter the filepath: ')
    the_file = open(file_path, 'rb')
    my_institution = pickle.load(the_file)

else:
    user_input = input('Please​ ​enter​ ​the​ ​name​ ​of​ ​your​ ​institution:​ ​')

    my_institution = registrar.Institution(user_input)

user_input2 = 0
while user_input2 != '13':

    print('Please​ ​select​ ​an​ ​option​ ​from​ ​the​ ​following: ' + '\n' + \
    '1' + '  ' + 'Create​ ​a​ ​course' + '\n' + \
    '2' + '  ' + 'Schedule a course offering' + '\n' + \
    '3' + '  ' + 'List course catalog' + '\n' + \
    '4' + '  ' + 'List course schedule' + '\n' + \
    '5' + '  ' + 'Hire an instructor' + '\n' + \
    '6' + '  ' + 'Assign an instructor to a course' + '\n' + \
    '7' + '  ' + 'Enroll a student' + '\n' + \
    '8' + '  ' + 'Register a student for a course' + '\n' + \
    '9' + '  ' + 'List enrolled students' + '\n' + \
    '10' + '  ' + 'List students registered for a course' + '\n' + \
    '11' + '  ' + 'Submit student grade' + '\n' + \
    '12' + '  ' + 'Get student records' + '\n' + \
    '13' + '  ' + 'Exit')

    user_input2 = input('Please​ ​enter​ ​your​ ​choice:​ ')

    if user_input2 == '1':
        dep = input('Please enter the department of the course: ')
        nam = input('Please enter the name of the course: ')
        num = input('Please enter the course number: ')
        cred = input('Please enter the number of credits: ')
        new_course = registrar.Course(dep, nam, num, cred)
        my_institution.course_catalog.append(new_course)
        print('Course created!')

    elif user_input2 == '2':
        cors = input('Enter the generic name of the course from the course catalog: ')
        for x in my_institution.course_catalog:
            if x.name == cors:
                cors = x
                break
        section_number = input('Please enter the section number of the course: ')
        nam = input('Please enter the username of the instructor of the course: ')
        the_right_instructor = my_institution.faculty[nam]
#        for x in my_institution.faculty:
#            if x.username == nam:
#                break
#            the_right_instructor = x
        year = input('Please enter the year the course will be offered: ')
        quarter = input('Please enter the quarter the course will be offered: ')
        new_course_offering = registrar.CourseOffering(cors, section_number, the_right_instructor, year, quarter)
        my_institution.course_schedule.append(new_course_offering)
        print('Course Offering created!')

    elif user_input2 == '3':
        for x in my_institution.list_course_catalog():
            print(x)
        #print(my_institution.list_course_catalog())


    elif user_input2 == '4':
        input_year = input('Please enter a year: ')
        input_quarter = input('Please enter a quarter: ')
        for x in my_institution.course_schedule:
            if x.year == input_year and x.quarter == input_quarter:
                print(x)
    #    for x in my_institution.list_course_schedule(input_year, input_quarter):
    #        print(x)


    elif user_input2 == '5':
        last = input('Please enter the last name of the instructor: ')
        first = input('Please enter the first name of the instructor: ')
    #    dob = input('Please enter the birth date of the instructor, separated by commas \
    #    without space in order year, month, day. Ex: (1980,3,15): ')
        dobyear = int(input('Please enter the year the instructor was born (an integer): '))
        dobmon = int(input('Please enter the month the instructor was born (an integer): '))
        dobday = int(input('Please enter the day the instructor was born (an integer): '))
        date_of_birth = datetime.date(dobyear,dobmon,dobday)
        username = input('Please enter the username of the instructor (first initial + last name, all lowercase): ')
        new_instructor = registrar.Instructor(last, first, my_institution, date_of_birth, username)
        my_institution.faculty[username] = new_instructor
#        my_institution.faculty.append(new_instructor)
        print('Instructor hired!')

    elif user_input2 == '6':
        nam = input('Please enter the username of the instructor to be assigned to the course: ')
        the_right_instructor = my_institution.faculty[nam]
#        for x in my_institution.faculty:
#            if x.username == nam:
#                break
#            the_right_instructor = x
        cors = input('Enter the generic name of the course from the course catalog: ')
        sec_num = input('Please enter the section number of the course: ')
        dep =  input('Please enter the department of the course: ')
        num = input('Please enter the course number of the course: ')
        year = input('Please enter the year of the course: ')
        quarter = input('Please enter the quarter of the course: ')
        valid_list = my_institution.course_schedule
#        valid_list = list(my_institution.list_course_schedule(year, quarter, dep))
        the_right_course = None
        for x in valid_list:
            if x.course.name==cors and x.section_number == sec_num and x.course.number == num:
                the_right_course = x
                break
        the_right_course.instructor = the_right_instructor
        print('Instructor assigned!')

    elif user_input2 == '7':
        last = input('Please enter the last name of the student: ')
        first = input('Please enter the first name of the student: ')
        dobyear = int(input('Please enter the year the student was born (an integer): '))
        dobmon = int(input('Please enter the month the student was born (an integer): '))
        dobday = int(input('Please enter the day the student was born (an integer): '))
        date_of_birth = datetime.date(dobyear,dobmon,dobday)
        username = input('Please enter the username of the instructor (first initial + last name, all lowercase): ')
        new_student = registrar.Student(last, first, my_institution, date_of_birth, username)
        my_institution.enroll_student(new_student)
#        my_institution.matriculation.append(new_student)
        print('Student Enrolled!')

    elif user_input2 == '8':
        nam = input('Please enter the username of the student to be registered to the course: ')
#        for y in my_institution.matriculation:
#            if y.username == the_student:
#                break
#            the_student = y
        the_student = my_institution.matriculation[nam]
        cors = input('Enter the generic name of the course from the course catalog: ')
        sec_num = input('Please enter the section number of the course: ')
        dep =  input('Please enter the department of the course: ')
        num = input('Please enter the course number of the course: ')
        year = input('Please enter the year of the course: ')
        quarter = input('Please enter the quarter of the course: ')
        valid_list = my_institution.course_schedule
#        valid_list = my_institution.list_course_schedule(year, quarter, dep)
        the_right_course = None
        for x in valid_list:
            if x.course.name==cors and x.section_number == sec_num and x.course.number == num:
                the_right_course = x
                break
        the_right_course.register_students(the_student)
        print('Student registered!')


    elif user_input2 == '9':
        for x in my_institution.list_students():
            print(x)


    elif user_input2 == '10':
        cors = input('Enter the generic name of the course from the course catalog: ')
        sec_num = input('Please enter the section number of the course: ')
        dep =  input('Please enter the department of the course: ')
        num = input('Please enter the course number of the course: ')
        year = input('Please enter the year of the course: ')
        quarter = input('Please enter the quarter of the course: ')
        valid_list = my_institution.course_schedule
        the_right_course = None
        for x in valid_list:
            if x.course.name==cors and x.section_number == sec_num and x.course.number == num:
                the_right_course = x
                break
        print(the_right_course.students_registered)

    elif user_input2 == '11':
        ident = input('Please enter the username of the student to be assigned a grade: ')
        cors = input('Enter the generic name of the course from the course catalog: ')
        sec_num = input('Please enter the section number of the course: ')
        dep =  input('Please enter the department of the course: ')
        num = input('Please enter the course number of the course: ')
        year = input('Please enter the year of the course: ')
        quarter = input('Please enter the quarter of the course: ')
        grade = input('Please enter the grade to be assigned: ')
        valid_list = my_institution.course_schedule
#        valid_list = list(my_institution.list_course_schedule(year, quarter, dep))
        the_right_course = None
        for x in valid_list:
            if x.course.name==cors and x.section_number == sec_num and x.course.number == num:
                the_right_course = x
                break
        the_right_course.submit_grade(ident, grade)
        print('Grade assigned!')

    elif user_input2 == '12':
        nam = input('Please enter the username of the student: ')
        the_student = my_institution.matriculation[nam]
#        for x in my_institution.matriculation:
#            if x.username == the_student:
#                break
#            the_student = x
        gpa = the_student.gpa()
        creds = the_student.credits()
        crs = the_student.list_courses()
        print('GPA: ' + gpa)
        print('Credits: ' + creds)
        print('Courses: ' + crs)

    elif user_input2 == '13':
        pass

    else:
        print('Please enter a proper selection')


    while(True):
        x = input('Please hit enter to continue: ')
        if x == '':
            break


file_name = input('Please enter a filename for saving your data (this is a .pickle file): ')
#location = input('Please input a location to save your information: ')

the_file = open(file_name, 'wb')

pickle.dump(my_institution, the_file)
the_file.close
#my_dataframe = pd.DataFrame(my_institution)
#my_dataframe.write_csv(location)


#my_dataframe = pd.read_csv(location)

print('all done!')
