from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://127.0.0.1:27017")
        self.db = self.client['Attendance']
        self.MCAbatches = self.db['All_Batches']
        self.register = self.db['facultyRegister']
        self.MCA_subjects = self.db['subjectDetails']
        self.MCA_faculty = self.db['facultiesList']
        self.MCA_Students = self.db['studentList']
        self.MCA_Attendance = self.db['attendance']
        self.adminLogin = self.db['adminLogin']



class MBA_Database:
     def __init__(self):
        self.client = MongoClient("mongodb://127.0.0.1:27017")
        self.db = self.client['MBA_Attendance']
        self.MBAbatches = self.db['All_Batches']
        self.MBA_faculty = self.db['facultiesList']
        self.sub_semOne = self.db['sub_semOne']
        self.sub_semTwo = self.db['sub_semTwo']
        self.sub_semThree = self.db['sub_semThree']
        self.sub_semFour = self.db['sub_semFour']
        self.MBA_Students = self.db['studentList']
        self.MBA_sem_one = self.db['MBA_sem_one']
        self.MBA_SemIAttendance = self.db['MBA_SemIAttendance']
        self.MBA_Attendance = self.db['attendance']

