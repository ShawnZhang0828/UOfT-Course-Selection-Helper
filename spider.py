import requests
from bs4 import BeautifulSoup as soup
import json

class Spider:
    '''
        This class crawls the website and performs search on the website using GET method
    '''

    url = 'https://timetable.iit.artsci.utoronto.ca/api/20219/courses'

    def __init__(self, courseID):
        self.courseID = courseID

    def find_course_info(self):
        '''
            This method performs GET and extract the content from the website
        '''
        # if it is a seasonal course
        if self.courseID[-1] == 'S' or self.courseID[-1] == 'F':
            courseID = self.courseID.strip('SF')
            course_code = { 'code' : courseID, 
                            'section' : self.courseID[-1]}
        else:
            course_code = {'code' : self.courseID}
        
        response = requests.get(Spider.url, params = course_code)
        content = response.content

        return content

    def organize_info(self, content):
        content = str(content, encoding='utf-8')
        content_str = json.loads(content)
        # convert the website content to a python dictionary
        result = Spider.organize_dict(content_str, content_str)

        return result
        
    @staticmethod    
    def organize_dict(d, current):
        '''
            Get rid of "\n " in front of items in a dictionary using recursion
        '''
        try:
            for key,value in current.items():
                old_key = key
                new_key = old_key.strip('\n ')
                new_value = value.strip('\n')
                d[new_key] = new_value
                Spider.organize_dict(d, value)
        except:
            return d

    def start(self):
        content = self.find_course_info()
        content = self.organize_info(content)

        return content



    


        
