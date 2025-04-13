import pandas as pd
from faker import Faker
import random 


fake = Faker() 
email_count = {} 
def emails(name,num):
    unique_emails = []
    for i in range(num):
        whole_name = name[i].replace(" ", "")
        base = f"{whole_name}@uwi.mona.edu"
        count = email_count.get(base, 0)

        email = base if count == 0 else f"{whole_name}{count + 1}@uwi.mona.edu"
        email_count[base] = count + 1
        unique_emails.append(email)
    return unique_emails

course_names = {
        "COMP": ["Intro to Computing", "Data Structures", "Algorithms", "Operating Systems", "Software Engineering", "Database Systems", "Artificial Intelligence", "Computer Networks"],
        "PHYS": ["General Physics", "Mechanics", "Electromagnetism", "Thermodynamics", "Quantum Physics", "Optics", "Nuclear Physics"],
        "MATH": ["Calculus I", "Calculus II", "Linear Algebra", "Discrete Mathematics", "Probability Theory", "Abstract Algebra", "Differential Equations"],
        "CHEM": ["General Chemistry", "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Analytical Chemistry", "Biochemistry"],
        "BIOL": ["Intro to Biology", "Genetics", "Microbiology", "Cell Biology", "Ecology", "Human Anatomy", "Evolution"],
        "ECON": ["Microeconomics", "Macroeconomics", "Econometrics", "Public Economics", "International Economics", "Game Theory"],
        "PSYC": ["Intro to Psychology", "Developmental Psychology", "Social Psychology", "Abnormal Psychology", "Cognitive Psychology"],
        "HIST": ["World History", "Ancient Civilizations", "Modern History", "American History", "European History"],
        "ENGL": ["English Composition", "Creative Writing", "Literary Analysis", "Shakespeare Studies", "Modern Literature"],
        "PHIL": ["Intro to Philosophy", "Ethics", "Logic", "Philosophy of Mind", "Political Philosophy"],
        "STAT": ["Intro to Statistics", "Probability and Statistics", "Regression Analysis", "Statistical Inference", "Time Series Analysis"],
        "SOCI": ["Intro to Sociology", "Social Theory", "Urban Sociology", "Sociology of Education", "Gender Studies"],
        "GEOG": ["Physical Geography", "Human Geography", "Cartography", "Geographical Information Systems", "Environmental Geography"],
        "ARTS": ["Art History", "Painting Techniques", "Sculpture Basics", "Modern Art", "Photography"],
        "MUSC": ["Music Theory", "History of Music", "Composition", "Instrumental Techniques", "Choral Studies"]
        }

subject_codes = [
"COMP",  # Computer Science
"PHYS",  # Physics
"MATH",  # Mathematics
"CHEM",  # Chemistry
"BIOL",  # Biology
"ECON",  # Economics
"PSYC",  # Psychology
"HIST",  # History
"ENGL",  # English
"PHIL",  # Philosophy
"STAT",  # Statistics
"SOCI",  # Sociology
"GEOG",  # Geography
"ARTS",  # Arts
"MUSC",  # Music
]

def insert_person(type,num):
    data = pd.DataFrame()
    
    if type == "Student":
        ids = [fake.unique.random_int(min=620000000, max=629999999) for _ in range(num)]
       
        name = [fake.first_name() +" "+ fake.last_name() for x in range(0,num)]
        unique_emails = emails(name,num)
        role = [type for _ in range(num)]

        data["user_id"] = ids
        data["name"] = name
        data["email"] = unique_emails
        data["role"] = role             
        return data
    
    elif type == "Lecturer":
        ids = [fake.unique.random_int(min=1000000, max=1009999) for _ in range(num)]
       
        name = [fake.name() for _ in range(0,num)]
        unique_emails = emails(name,num)
        role = [type for _ in range(num)]

        data["user_id"] = ids
        data["name"] = name
        data["email"] = unique_emails
        data["role"] = role 
        return data
    
    elif type == "Admin":
        ids = [fake.unique.random_int(min=99900000, max=99999999) for _ in range(num)]
       
        name = [fake.name() for _ in range(0,num)]
        unique_emails = emails(name,num)
        role = [type for _ in range(num)]
        
        data["user_id"] = ids
        data["name"] = name
        data["email"] = unique_emails
        data["role"] = role 
        return data

def insert_course(num):
    data = pd.DataFrame()
    def generate_course_data(num):
        
        course_name = []
        course_code = []

        def generate_course_number():
            first_digit = random.choice(['1', '2', '3'])
            remaining_digits = ''.join(random.choices('0123456789', k=3))
            return first_digit + remaining_digits


        courses = [f"{random.choice(subject_codes)} {generate_course_number()}" for _ in range(num)]
        
        for course in courses:
            subject_code = course.split()[0]
            course_title = random.choice(course_names.get(subject_code, ["Special Topics"]))
            course_code.append(course.replace(" ",""))
            course_name.append(course_title)

        return course_code,course_name
    
    ids = [fake.unique.random_int(min=0, max=99999) for _ in range(num)]
    course,course_title  = generate_course_data(num)

    data["Course ID"] = ids
    data["Course_Name"] = course_title
    data["Course_Code"] = course

    return data

def Student_Course(students,courses):

    s_id = students["user_id"].tolist()
    c_id = courses["Course ID"].tolist()
    S_C_num = [random.randint(3,6) for _ in range(len(s_id))]

    c_s_id_list ={}
    s_c_id_list = {}
    for i in range(0,len(s_id)):
        lst = []
        for j in range(0,S_C_num[i]):

            keys = list(s_c_id_list.keys())
            course = str(random.choice(c_id))

            while course in lst:
                course = str(random.choice(c_id))
                

            lst.append(course)

            if course in (keys):
                s_c_id_list[str(course)] += 1
            else:
                s_c_id_list[str(course)] = 1


        c_s_id_list[str(s_id[i])] = lst


    keys = list(s_c_id_list.keys())

    for key in keys:
        while (s_c_id_list[key]) < 10:
            i = random.randint(0,len(s_id)-1)
            if S_C_num[i] <= 5:
                if key not in c_s_id_list[str(s_id[i])]:
                    c_s_id_list[str(s_id[i])].append(str(key))
                    s_c_id_list[key] += 1
                    S_C_num[i] += 1
    
    return (c_s_id_list)

def Lecturers_course(lecturers,courses):
    l_id = lecturers["user_id"].tolist()
    c_id = courses["Course ID"].tolist()
    L_C_num = [random.randint(1,5) for _ in range(len(l_id))]

    l_c_id_list ={}
    c_l_id_list ={}
    for i in range(0,len(l_id)):
        lst = []
        for j in range(0,L_C_num[i]):

            course = str(random.choice(c_id))
            while course in lst:
                course = str(random.choice(c_id))

            lst.append(course)

            keys = list(l_c_id_list.keys())

            if course in (keys):
                l_c_id_list[str(course)] += 1

            else:
                l_c_id_list[str(course)] = 1

        c_l_id_list[str(l_id[i])] = lst
    
    for key in c_id:
        while str(key) not in list(l_c_id_list.keys()):
            i = random.randint(0,len(l_id)-1)
            if L_C_num[i] <= 4:
                c_l_id_list[str(l_id[i])].append(str(key))
                l_c_id_list[str(key)] = 1
                L_C_num[i] += 1
            
    return c_l_id_list

def default_login(users):
    data = pd.DataFrame()
    password= []

    for user in users:
        password.append(fake.password())
    
    data["user_id"] = users
    data["password"] = password
    return data

def login_insert(user,sql,user_type):
    sql.write(f"\n-- {user_type} Login Inserts\n")
    for i in range(len(user["user_id"])):
        sql.write(
            f"""INSERT INTO Logins(user_id, user_password) Values("{user["user_id"][i]}","{user["password"][i]}");\n""")

def user_insert(user,sql,user_type):
    sql.write(f"\n-- {user_type} User Inserts\n")
    for i in range(len(user["user_id"])):
        sql.write(
            f"""INSERT INTO User(user_id,name,email,role) Values("{user["user_id"][i]}","{user["name"][i]}","{user["email"][i]}","{user["role"][i]}");\n""")

def course_insert(course,sql):
    sql.write(f"\n-- Course Inserts\n")
    for i in range(len(course["Course ID"])):
        sql.write(
            f"""INSERT INTO Course(course_id,course_name,course_code) Values("{course["Course ID"][i]}","{course["Course_Name"][i]}","{course["Course_Code"][i]}");\n""")

def user_course_insert(register,sql,user_type):
    sql.write(f"\n-- {user_type} Course Inserts\n")
    for user in (register.keys()):
        for course in (register[user]):
            sql.write(
            f"""INSERT INTO User_Course(user_id,course_id) Values("{user}","{course}");\n""")

if __name__ == '__main__':
    print("Start")
    students = insert_person("Student",1000000)
    lecturers = insert_person("Lecturer",100)
    admin = insert_person("Admin",30)

    students_pw = default_login(students["user_id"])
    lecturers_pw = default_login(lecturers["user_id"])
    admin_pw = default_login(admin["user_id"])

    courses = insert_course(300)

    Student_Register  = (Student_Course(students,courses))
    Lecturers_Register = Lecturers_course(lecturers,courses)

    with open ("Scripts\\insert.sql","w") as sql:

        user_insert(students,sql,"students")
        user_insert(lecturers,sql,"lecturers")
        user_insert(admin,sql,"admin")


        login_insert(students_pw,sql,"students")
        login_insert(lecturers_pw,sql,"lecturers")
        login_insert(admin_pw,sql,"admin")

        course_insert(courses,sql)

        user_course_insert(Student_Register,sql,"students")
        user_course_insert(Lecturers_Register,sql,"lecturers")

    sql.close()
