import datetime

class Course:
    def __init__(self, department, name, number, credits):
        self.department = department # if not department.isupper(): department.upper()
        self.name = name
        self.number = number
        self.credits = credits

    def __str__(self):
        return 'Name: ' + self.name + ' ' + str(self.number) + '\n' + \
        'Department: ' + self.department + '\n' + \
        'Credits: ' + str(self.credits)

    def __repr__(self):
        return self.name




class CourseOffering:
    def __init__(self, course, section_number, instructor, year, quarter):
        self.course = course
        self.section_number = section_number
        self.instructor = instructor
        self.year = year
        self.quarter = quarter
        self.students_registered = []
        instructor.courses.append(self)
        self.student_grades = {}   #

    def register_students(self, *args):
        for arg in args:
            if not isinstance(arg, Student):
                raise TypeError('must be instance of Student')
            else:
                self.students_registered.append(arg)
                arg.courses.append(self)

    def get_students(self):
        return [repr(x) for x in self.students_registered]


    def submit_grade(self, identification, grade):  #identification is either instance of student OR student username
        if isinstance(identification, Student):
            self.student_grades[identification.username] = grade
        else:
    #        for x in self.students_registered:
    #            if x.username == identification
    #                identification = x
            self.student_grades[identification] = grade

    def get_grade(self, identification): #identifiction is either student name OR student username
        if isinstance(identification, Student):
            return self.student_grades[identification.username]
        else:
            return self.student_grades[identification]


    def __str__(self):
        return 'Course: ' + repr(self.course) + '\n' + \
        'Section: ' + str(self.section_number) + '\n' + \
        'Instructor: ' + repr(self.instructor) + '\n' + \
        'Year: ' + str(self.year) + '\n' + \
        'Quarter: ' + self.quarter

    def __repr__(self):
        return repr(self.course) + ': ' + str(self.quarter) + ' ' + str(self.year)

class Institution:
    def __init__(self, name):
        self.name = name
        self.matriculation = {}
        self.faculty = {}
        self.course_catalog = []
        self.course_schedule = []

    @property
    def domain(self):
        domain = self.name.replace(' ','').replace('The','').replace('University','U')
        return domain

    def list_students(self):
        return list(self.matriculation.values())

    def enroll_student(self, student):
        if isinstance(student, Student):
            self.matriculation[student.username] = student
        else:
            raise TypeError('must be instance of Student')

    def list_instructors(self):
        return list(self.faculty.values())

    def hire_instructor(self, instructor):
        if isinstance(instructor, Instructor):
            self.faculty[instructor.username] = instructor
        else:
            raise TypeError('must be instance of Instructor')

    def list_course_catalog(self):
        return self.course_catalog

    def list_course_schedule(self, year, quarter, department=None):
        if department:
            my_list1 = filter(lambda x: x.year==year and x.quarter==quarter and x.course.department==department, self.course_schedule)
            return list(my_list1)
        else:
            my_list2 = filter(lambda x: x.year==year and x.quarter==quarter, self.course_schedule)
            return list(my_list2)

    def add_course(self, course):
        if isinstance(course, Course):
            self.course_catalog.append(course)
        else:
            raise TypeError('must be instance of Course')

    def add_course_offering(self, course):
        if isinstance(course, CourseOffering):
            self.course_schedule.append(course)
        else:
            raise TypeError('must be instance of CourseOffering')

    def __str__(self):
        return 'Institution :' + self.name


class Person:
    def __init__(self, last_name, first_name, school, date_of_birth, username, affiliation):
        self.last_name = last_name
        self.first_name = first_name
        self.school = school
        self.date_of_birth = date_of_birth
        self.username = username
        self.affiliation = affiliation

    @property
    def email(self):
        mail = self.username + '@' + self.school.domain + '.edu'
        return mail


class Instructor(Person):
    def __init__(self, last_name, first_name, school, date_of_birth, username):
        Person.__init__(self, last_name, first_name, school, date_of_birth, username, 'instructor')
        self.courses = []

    def list_courses(self, year=None, quarter=None):
        if year and quarter:
            my_list = filter(lambda x: x.year==year and x.quarter==quarter, self.course_schedule)
            sorted(my_list, key = lambda x: (x.year, x.quarter), reverse=True)
        elif year:
            my_list = filter(lambda x: x.year==year, self.course_schedule)
            sorted(my_list, key = lambda x: (x.year, x.quarter), reverse=True)
        elif quarter:
            my_list = filter(lambda x: x.quarter==quarter, self.course_schedule)
            sorted(my_list, key = lambda x: (x.year, x.quarter), reverse=True)
        else:
            my_list = sorted(self.courses, key = lambda x: (x.year, x.quarter), reverse=True)
            return [repr(x) for x in my_list]

    def __str__(self):
        return 'Name :' + self.first_name + ' ' + self.last_name + '\n' + \
        'School: ' + self.school.name + '\n' + \
        'DOB: ' + str(self.date_of_birth) + '\n' + \
        'Username: ' + self.username + '\n' + \
        'Status: ' + self.affiliation

    def __repr__(self):
        return self.first_name + ' ' + self.last_name


class Student(Person):
    def __init__(self, last_name, first_name, school, date_of_birth, username):
        Person.__init__(self, last_name, first_name, school, date_of_birth, username, 'student')
        self.courses = []


    def list_courses(self):   #returns list of CourseOfferings
        my_list = sorted(self.courses, key = lambda x: (x.year, x.quarter), reverse=True)
        return [repr(x) for x in my_list]


    def credits(self):
        count = 0
        for x in self.courses:
            #count += x.credits
            count += x.course.credits
        return count


    def gpa(self):
        conversion_dict = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, \
        'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, \
        'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0}
        grade_points = 0
        total_creds = 0
        for x in self.courses:
            grade_points += (conversion_dict[x.get_grade(self)] * x.course.credits)
            total_creds += x.course.credits
        grade_point_avg = grade_points / total_creds
        return grade_point_avg


    def __str__(self):
        return 'Name :' + self.first_name + ' ' + self.last_name + '\n' + \
        'School: ' + self.school.name + '\n' + \
        'DOB: ' + str(self.date_of_birth) + '\n' + \
        'Username: ' + self.username + '\n' + \
        'Status: ' + self.affiliation

    def __repr__(self):
        return self.first_name + ' ' + self.last_name







UofC = Institution('The University of Chicago')

print('Students and Instructors...')
Sally_Joe = Student('Joe', 'Sally', UofC, datetime.date(1990,3,10), 'sjoe')
print(Sally_Joe)
print(Sally_Joe.email)
Bobby_Brown = Student('Brown', 'Bobby', UofC, datetime.date(1992,10,15),'bbrown')
Jane_Smith = Student('Smith','Jane',UofC, datetime.date(1991,1,5),'jsmith')
Nick_Flees = Instructor('Flees', 'Nick', UofC, datetime.date(1980,5,5), 'nflees')
Gerry_Brady = Instructor('Brady', 'Gerry', UofC, datetime.date(1805, 6, 6), 'gbrady')
print(Nick_Flees)

print('------------')
MPCS_10112 = Course('MPCS', 'Python Programming', 10112, 3)
print('Testing Course Creation ...')
print(MPCS_10112)
MPCS_66666 = Course('MPCS', 'Algorithms', 66666, 4)
ENG_32145 = Course('ENG', 'Eccentric Moderns', 32145, 4)

print(' ----------- ')
Algorithms_Winter_2018 = CourseOffering(MPCS_66666, 2, Gerry_Brady, 2018, 'Winter')
Python_Fall_2017 = CourseOffering(MPCS_10112, 1, Nick_Flees, 2017, 'Fall')
print('Testing CourseOffering Creation ...')
print(Python_Fall_2017)
Python_Fall_2017.register_students(Sally_Joe, Bobby_Brown, Jane_Smith)
Algorithms_Winter_2018.register_students(Sally_Joe)
print(Python_Fall_2017.get_students())
print(Algorithms_Winter_2018.get_students())

print('____________')
print('Testing Registrations...')

#Sally_Joe.courses.append(Python_Fall_2017)
#Sally_Joe.courses.append(Algorithms_Fall_2017)
print(Sally_Joe.list_courses())
print(Sally_Joe.credits())
print(Nick_Flees.list_courses())
print(Gerry_Brady.list_courses())

print('____________')
print('Testing Institutions...')
print(UofC)
UofC.enroll_student(Sally_Joe)
UofC.enroll_student(Bobby_Brown)
UofC.enroll_student(Jane_Smith)
print(UofC.list_students())
UofC.hire_instructor(Nick_Flees)
UofC.hire_instructor(Gerry_Brady)
print(UofC.list_instructors())
UofC.add_course(MPCS_10112)
UofC.add_course(MPCS_66666)
UofC.add_course_offering(Python_Fall_2017)
UofC.add_course_offering(Algorithms_Winter_2018)
print(UofC.list_course_catalog())
print(UofC.list_course_schedule(2017, 'Fall'))
#print(Sally_Joe.gpa())

print('____________')
print('Testing Filtering...')
print(UofC.list_course_catalog())
print(UofC.list_course_schedule(2017, 'Fall'))
print(UofC.list_course_schedule(2017, 'Fall', 'MPCS'))

print('____________')
print('Testing Grading...')
Python_Fall_2017.submit_grade(Sally_Joe, 'A')
sally_python_grade = Python_Fall_2017.get_grade(Sally_Joe)
print(sally_python_grade)
Algorithms_Winter_2018.submit_grade(Sally_Joe, 'B+')
sally_algorithms_grade = Algorithms_Winter_2018.get_grade(Sally_Joe)
print(sally_algorithms_grade)
sally_gpa = Sally_Joe.gpa()
print(sally_gpa)
