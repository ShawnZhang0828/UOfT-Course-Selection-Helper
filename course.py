
class Course:
    '''
        This class manipulate the content from the website, and 
        organize it into intended format
    '''

    def __init__(self, info):
        self.info = info
        self.course_code = list(info)[0]
        self.sessionIDs = self.get_sessionIDs()
        self.occupied_time = self.get_occupied_time()

    def get_sessionIDs(self):
        sessionIDs = []
        course_info = self.info[self.course_code]

        # iterate through certain portion of the dictionary to find session IDs
        for key,value in course_info['meetings'].items():
            sessionIDs.append(key)

        return sessionIDs

    @staticmethod
    def time_convertor(weekday, time):
        '''
            This method converts time in xx:xx (weekday) to a number
            The number start from 0 when 00:00 in Monday, and add one per minute
        '''
        time = time.split(':')
        time = int(time[0]) * 60 + int(time[1])

        day = {
            'MO' : 0,
            'TU' : 1,
            'WE' : 2,
            'TH' : 3,
            'FR' : 4
        }
        time = 24 * 60 * day.get(weekday) + time
        
        return time

    @staticmethod
    def reverse_time_convertor(interval):
        '''
            This method performs the reverse convertion against the above function
        '''

        interval = list(interval)
        minute = [time % 60 for time in interval]
        interval[0] -= minute[0]
        interval[1] -= minute[1]
        day = [time // (24 * 60) for time in interval]
        hour = [time // 60 for time in interval]
        hour[0] -= day[0] * 24
        hour[1] -= day[1] * 24
        
        day_word = {
            '0' : 'Monday',
            '1' : 'Tuesday',
            '2' : 'Wednesday',
            '3' : 'Thursday',
            '4' : 'Friday'
        }

        day = [day_word.get(str(day_num)) for day_num in day]

        return minute, hour, day


    def get_occupied_time(self):
        '''
            This method find the time interval required by each session and
            store them in a dictionary
        '''
        occupied = {}
        time_info = self.info[self.course_code]['meetings']

        # iterate certain portion of the dictionary and find session information
        for key1,value1 in time_info.items():
            if key1 in self.sessionIDs:
                # all the time interval required for one session
                week_occupied = []
                if (type(value1['schedule'])) == list:
                    break
                for key2,value2 in value1['schedule'].items():
                    week_day = value2['meetingDay']
                    start_time = Course.time_convertor(week_day, value2['meetingStartTime'])
                    end_time = Course.time_convertor(week_day, value2['meetingEndTime'])
                    week_occupied.append((start_time, end_time))
                occupied[key1] = week_occupied

        return occupied
