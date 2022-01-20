from spider import Spider
from course import Course
from timetable import TimeTable

course_list = ['mat235', 'eco200', 'eco202', 'mat224', 'sta237']
course_schedule = {}

for course in course_list:
    mySpider = Spider(course)
    info = mySpider.start()

    f_course = Course(info)
    course_schedule[course] = f_course.occupied_time

myTimeTable = TimeTable(course_schedule)
pairs = myTimeTable.get_all_pairs()
myTimeTable.get_schedule(0, [], 0, pairs)
# print ('--->', myTimeTable.available_schedule, '<----')
myTimeTable.available_schedule = TimeTable.time_filter(myTimeTable.available_schedule)
# print (myTimeTable.available_schedule)
myTimeTable.display_result()


