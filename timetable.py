
from course import Course

class TimeTable:
    '''
        This class create the time table and do all the filtering work
    '''

    def __init__(self, course_schedule):
        self.course_schedule = course_schedule
        self.courseIDs = list(self.course_schedule.keys())
        self.available_schedule = []

    def get_all_pairs(self):
        pairs = []

        for courseID, sessions in self.course_schedule.items():
            lec_times = TimeTable.extract_lec(sessions)
            tut_times = TimeTable.extract_tut(sessions)
            valid_pair = TimeTable.get_tut_lec_pair(lec_times, tut_times)
            pairs.append(valid_pair)

        return pairs

    def get_schedule(self, current_course, current_chosen, pair_num, pairs):
        # find the time that is occupied by what has been determined
        if current_course != 0:
            current_occupied = []
            for index, chosen_session in enumerate(current_chosen):
                current_occupied += TimeTable.get_pair_occupied(chosen_session[self.courseIDs[index]])[0]
        else:
            current_occupied = []

        # do nothing if the current_course and pair_num exceeds the maximum value
        if current_course <= len(self.courseIDs) - 1 and pair_num <= len(pairs[current_course]) - 1:
            # find the time that is required for the current session
            session_dict = pairs[current_course][pair_num]
            current_time = TimeTable.get_pair_occupied(session_dict)[0]
            # check whether this session is valid
            overlap = TimeTable.check_list_overlap(current_occupied, current_time)
        else:
            overlap = True

        # start a new list to work with when comes to the first course 
        if current_course == 0:
            if pair_num <= len(pairs[0]) - 1:  
                # continue to check the next session of this course
                self.get_schedule(0, [{self.courseIDs[0] : pairs[0][pair_num]}], pair_num + 1, pairs)
                # move to the next course
                self.get_schedule(1, [{self.courseIDs[0] : pairs[0][pair_num]}], 0, pairs)
        elif current_course == len(self.courseIDs) - 1:    
            # avoid repetition
            keys_list = list(map(lambda course: list(course.keys())[0], current_chosen)) + [self.courseIDs[current_course]]
            if overlap == False:
                # if no overlap, add the final list to available schedules as an option
                if keys_list.count(max(set(keys_list), key=keys_list.count)) == 1:
                    current_chosen.append({self.courseIDs[current_course] : pairs[current_course][pair_num]})
                    self.available_schedule.append(current_chosen)
            # continue to check the next session of this course
            if pair_num <= len(pairs[current_course]) - 1: 
                self.get_schedule(current_course, current_chosen, pair_num + 1, pairs)
        else:
            # continue to check the next session of this course
            if pair_num <= len(pairs[current_course]) - 1: 
                self.get_schedule(current_course, current_chosen, pair_num + 1, pairs)
            # avoid repetition
            keys_list = list(map(lambda course: list(course.keys())[0], current_chosen)) + [self.courseIDs[current_course]]
            # keys_list = [self.courseIDs[current_course]]
            # for dict in current_chosen:
            #     keys_list += list(dict.keys())
            if overlap == False:
                # if no overlap, save the result and move to the next course
                if keys_list.count(max(set(keys_list), key=keys_list.count)) == 1:
                    current_chosen.append({self.courseIDs[current_course] : pairs[current_course][pair_num]})
                    if pair_num <= len(pairs[current_course]) - 1:            
                        self.get_schedule(current_course + 1, current_chosen, 0, pairs)

    def display_result(self):
        for i, option in enumerate(self.available_schedule):
            print (f'Option {i+1}: \n')
            for course in option:
                for courseID, sessions in course.items():
                    print (f'{courseID}:')
                    for sessionID, session_times in sessions.items():
                        print (f'\t{sessionID}: ')
                        for session_time in session_times:
                            minute, hour, day = Course.reverse_time_convertor(session_time)
                            print (f'\t\t{day[0]} {hour[0]}:{minute[0]}0 - {hour[1]}:{minute[1]}0')
                    
            print ('=======================================================================')

    @staticmethod
    def time_filter(options_list):
        options_list_copy = options_list.copy()
        for option in options_list_copy:
            weekday_list = []
            for course in option:                
                for courseID, session_times in course.items():
                    for sessionID, session_time in session_times.items():
                        for time in session_time:
                            # hour = Course.reverse_time_convertor(time)[1]
                            # if hour[0] >= 18:
                            #     try:                                
                            #         options_list.remove(option)
                            #     except:
                            #         pass
                            days = Course.reverse_time_convertor(time)[2]
                            weekday_list += days
            if ('Monday' in weekday_list) and ('Tuesday' in weekday_list) and ('Wednesday' in weekday_list) and ('Thursday'
                     in weekday_list) and ('Friday' in weekday_list): 
                options_list.remove(option)
        return options_list

    @staticmethod
    def get_pair_occupied(d):
        occupied = []
        occupiedID = []

        for sessionID, session_time in d.items():
            occupied += session_time
            occupiedID.append(sessionID)

        return occupied, occupiedID


    @staticmethod
    def extract_tut(d):
        return {sessionID:schedule for sessionID,schedule in d.items() if 'TUT-' in sessionID}

    @staticmethod
    def extract_lec(d):
        return {sessionID:schedule for sessionID,schedule in d.items() if 'LEC-' in sessionID}

    @staticmethod
    def check_overlap(time_interval1, time_interval2):
        range1 = range(time_interval1[0], time_interval1[1])
        range2 = range(time_interval2[0], time_interval2[1])
        range1_set = set(range1)
        overlap = range1_set.intersection(range2)

        return False if len(overlap) == 0 else True

    @staticmethod
    def check_list_overlap(list1, list2):
        overlap = False
        for interval1 in list1:
            for interval2 in list2:
                overlap = TimeTable.check_overlap(interval1, interval2)
                if overlap == True:
                    break
            if overlap == True:
                break
        return overlap

    @staticmethod
    def get_tut_lec_pair(lec_times, tut_times):
        valid_pair = []
        for lectureID, lec_time in lec_times.items():
            if len(tut_times) != 0:
                for tutorialID, tut_time in tut_times.items():
                    overlap = TimeTable.check_list_overlap(lec_time, tut_time)
                    if overlap == False:
                        valid_pair.append({lectureID : lec_time, tutorialID : tut_time})
            else:
                valid_pair.append({lectureID : lec_time})
            
        return valid_pair


