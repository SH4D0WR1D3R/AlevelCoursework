#DATABASE - QUIZ
#CREATING AND INITIALISING TABLES

import sqlite3
c = sqlite3.connect("quiz.db")
cursor = c.cursor()

def database_login(c, cursor):
    c.execute("""CREATE TABLE IF NOT EXISTS STUDENT
        (STUDENTID INTEGER PRIMARY KEY NOT NULL,
        FIRSTNAME TEXT NOT NULL,
        SURNAME TEXT NOT NULL,
        USERNAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        CLASS TEXT,
        LEVEL INTEGER);""")
    c.execute("INSERT or IGNORE INTO STUDENT (STUDENTID, FIRSTNAME, SURNAME, USERNAME, PASSWORD, CLASS, LEVEL) \
        VALUES (100, 'Shivani', 'Dave', 'sdave1', 'M45Tsf2j', 'AGE', 3)");
    c.execute("INSERT or IGNORE INTO STUDENT (STUDENTID, FIRSTNAME, SURNAME, USERNAME, PASSWORD, CLASS, LEVEL) \
        VALUES (200, 'Areeba', 'Safdar', 'asafdar2', 'a2HP0w1k', 'SKR', 2)");
    c.execute("INSERT or IGNORE INTO STUDENT (STUDENTID, FIRSTNAME, SURNAME, USERNAME, PASSWORD, CLASS, LEVEL) \
        VALUES (300, 'Fazza', 'Bajwa', 'fbajwa3', 'GL2worb68', 'AGE', 1)");
    c.commit()

def database_questions(c, cursor):
    c.execute("""CREATE TABLE IF NOT EXISTS QUESTION
        (QUESTIONID TEXT PRIMARY KEY NOT NULL,
        QUESTION TEXT NOT NULL,
        ANSWERM TEXT NOT NULL,
        TOPIC INTEGER,
        DIFFICULTY INTEGER);""")
## Different question types - multiple choice, state (text input)
## The question_type column will be used to determine which window layout is needed
## S means state, M means multiple choice
##    c.execute("INSERT or IGNORE INTO QUESTION (QUESTIONID, QUESTION, ANSWERM, TOPIC, DIFFICULTY, QUESTION_TYPE)\
##        VALUES (1, 'What is decomposition?', 'The breaking down of a problem', 1, 1, 'S')")
##    c.execute("INSERT or IGNORE INTO QUESTION (QUESTIONID, QUESTION, ANSWERM, TOPIC, DIFFICULTY, QUESTION_TYPE)\
##        VALUES (2, 'What is abstraction?', 'The removal of unnecessary data', 1, 1, 'S')")
##    c.execute("INSERT or IGNORE INTO QUESTION (QUESTIONID, QUESTION, ANSWERM, TOPIC, DIFFICULTY, QUESTION_TYPE)\
##        VALUES (1, 'What is the removal of unnecessary data?', 'Abstraction', 1, 1, 'S')")
##    c.execute("INSERT or IGNORE INTO QUESTION (QUESTIONID, QUESTION, ANSWERM, TOPIC, DIFFICULTY, QUESTION_TYPE)\
##        VALUES (2, 'What is the breaking down of a problem into smaller problems?', 'Decomposition', 1, 1, 'S')")
##    c.execute("INSERT or IGNORE INTO QUESTION (QUESTIONID, QUESTION, ANSWERM, TOPIC, DIFFICULTY, QUESTION_TYPE)\
##        VALUES (3, 'What is a logical way of getting from a problem to a solution?', 'Algorithmic Thinking', 1, 1, 'S')")
##    c.execute("INSERT or IGNORE INTO QUESTION (QUESTIONID, QUESTION, ANSWERM, TOPIC, DIFFICULTY, QUESTION_TYPE)\
##        VALUES (4, 'What is algorithmic thinking?', 'The logical way of getting from a problem to a solution', 1, 1, 'S')")
    c.commit()
    print("A")

def database_multiple_choice(c, cursor):
    c.execute("""CREATE TABLE IF NOT EXISTS TYPE
        (QUESTIONID INTEGER NOT NULL,
        QUESTION_TYPE INTEGER NOT NULL,
        OPTION1 TEXT,
        OPTION2 TEXT,
        OPTION3 TEXT,
        OPTION4 TEXT,
        FOREIGN KEY (QUESTIONID) REFERENCES QUESTION(QUESTIONID),
        PRIMARY KEY (QUESTIONID, QUESTION_TYPE));""")
    c.commit()

def database_answers(c, cursor):
    c.execute("""CREATE TABLE IF NOT EXISTS ANSWER 
         (ANSWERS TEXT NOT NULL,
         STUDENTID INTEGER NOT NULL,
         QUESTIONID INTEGER NOT NULL,
         DATE_DONE TEXT,
         SCORE INTEGER,
         FOREIGN KEY (STUDENTID) REFERENCES STUDENT(STUDENTID),
         FOREIGN KEY (QUESTIONID) REFERENCES QUESTION(QUESTIONID),
         PRIMARY KEY (ANSWERS, STUDENTID, QUESTIONID, DATE_DONE));""")
    c.commit()
    print("B")

def teacher_login(c, cursor):
    c.execute("""CREATE TABLE IF NOT EXISTS TEACHER
        (INITIALS TEXT PRIMARY KEY NOT NULL,
        USERT TEXT,
        PASST TEXT,
        NAMET TEXT);""")
    c.commit()
    print("C")

def assigned(c, cursor):
    c.execute("""CREATE TABLE IF NOT EXISTS ASSIGNED
        (STUDENTID INT NOT NULL,
        QUESTIONID INT NOT NULL,
        INITIALS TEXT NOT NULL,
        FOREIGN KEY (STUDENTID) REFERENCES STUDENT(STUDENTID),
        FOREIGN KEY (QUESTIONID) REFERENCES QUESTION(QUESTIONID),
        FOREIGN KEY (INITIALS) REFERENCES TEACHER(INITIALS),
        PRIMARY KEY (STUDENTID, QUESTIONID, INITIALS));""")
    c.commit()
        

##def database_multi():
##    global c, cursor
##    c = sqlite3.connect("quiz.db")
##    cursor = c.cursor()
##    c.execute("""CREATE TABLE IF NOT EXISTS MULTI
##        (
    
## CAN EITHER CHANGE QUESTION TABLE TO ACCOMODATE A COLUMN FOR QUESTION TYPE
## WHICH IS NOT NULL AND COLUMNS WHICH CAN BE EMPTY BUT HAVE OPTIONS FOR THE
## MULTILPE CHOICE
## OR
## CREATE A NEW TABLE TO HOLD MULTIPLE CHOICE QUESTIONS AND THE PROGRAM WOULD
## RANDOMLY CHOOSE WHICH TABLE TO USE EACH TIME A QUESTION IS GENERATED


database_login(c, cursor)
database_questions(c, cursor)
database_multiple_choice(c, cursor)
database_answers(c, cursor)
teacher_login(c, cursor)
assigned(c, cursor)

#when a database is locked, it is because the database is being used in python -  a python file is running it currently
