# Main Program AA

import sqlite3
from tkinter import *
from functools import partial
import random
import datetime
from time import sleep
from matplotlib import pyplot as plt

class Logging:
    def l_window(self, tex): # generates the tkinter window to allow users to log in
        log = Toplevel(root)
        log.title("LOG IN")
        log.geometry("300x300")
        var_u = StringVar()
        var_p = StringVar()
        Label(log, text = "Enter username: ").pack()
        Entry(log, textvariable = var_u).pack()
        Label(log, text = "Enter password: ").pack()
        Entry(log, show = '*', textvariable = var_p).pack()
        Label(log, text = tex).pack()
        var_status = StringVar()
        var_status.set("Select")
        st = {"Student", "Teacher"}
        Label(log, text = "Are you a student or a teacher?").pack()
        OptionMenu(log, var_status, *st).pack()
        Button(log, text = "Log In", command = partial(self.login, log, var_u, var_p, var_status)).pack()
        Button(log, text = "Register", command = self._register).pack()
    # Problem with variable called before assigned - was trying to put an input for label in the l_window function before the function where l_window was defined was called
    def login(self, window, var_u, var_p, var_status): # what occurs when the log in button is pressed
        status = var_status.get()
        lbl = ""
        if var_u.get() == "" or var_p.get() == "":
            pass
        elif status == "Teacher":
            cursor.execute("SELECT * FROM TEACHER WHERE usert = '%s' AND passt = '%s'" %(var_u.get(), var_p.get()))
            if cursor.fetchone() is not None:
                teacher_1 = Teacher(var_u, var_p)
                teacher_1.tm_window(window)
            else:
                sleep(1)
                window.destroy()
                self.l_window("Incorrect username or password. Please try again.")
        elif status == "Student":
            cursor.execute("SELECT * FROM STUDENT WHERE username = '%s' AND password = '%s'" %(var_u.get(), var_p.get()))
            if cursor.fetchone() is not None: #if something exists when the system has searched the database based on the requirements
                student_2 = Student(var_u, var_p)
                student_2.m_window(count_t, count_r, window)
            else:
                sleep(1)
                window.destroy()
                self.l_window("Incorrect username or password. Please try again.")
    def _register(self): # what occurs when the register button is pressed
##        window.destroy()
        wn_register = Toplevel(root)
        wn_register.title("REGISTER")
        wn_register.geometry("300x300")
        var_student_id = StringVar()
        var_first = StringVar()
        var_sur = StringVar()
        var_user = StringVar()
        var_pass = StringVar()
        var_class = StringVar()
        classes = {"None", "AGE", "SKR"}
        var_class.set("None")
        Label(wn_register, text = "Student Id").pack()
        Entry(wn_register, textvariable = var_student_id).pack()
        Label(wn_register, text = "First Name").pack()
        Entry(wn_register, textvariable = var_first).pack()
        Label(wn_register, text = "Surname").pack()
        Entry(wn_register, textvariable = var_sur).pack()
        Label(wn_register, text = "Username").pack()
        Entry(wn_register, textvariable = var_user).pack()
        Label(wn_register, text = "Password").pack()
        Entry(wn_register, textvariable = var_pass).pack()
        #COULD VERIFY PASSWORD BY MAKING THEM TYPE IT IN TWICE
        Label(wn_register, text = "Class").pack()
        OptionMenu(wn_register, var_class, *classes).pack()
        Button(wn_register, text = "DONE", command = partial(self._done, wn_register, var_student_id, var_first, var_sur, var_user, var_pass, var_class)).pack()
    def _done(self, window, var_student_id, var_first, var_sur, var_user, var_pass, var_class): # what occurs when the done button is pressed in the register window
        if self.check_user(var_student_id):
            cursor.execute("INSERT INTO STUDENT(STUDENTID, FIRSTNAME, SURNAME, USERNAME, PASSWORD, CLASS, LEVEL)\
                VALUES(?, ?, ?, ?, ?, ?, ?)", (var_student_id.get(), var_first.get(), var_sur.get(), var_user.get(), var_pass.get(), var_class.get(), 1))
            c.commit()
            window.destroy()
            logging_3 = Logging()
            logging_3.l_window(" ")
        else:
            wn_temporary = Toplevel(root)
            wn_temporary.title("ERROR")
            wn_temporary.geometry("300x50")
            Label(wn_temporary, text = "User already exists. Please enter a different student id").pack()
            Button(wn_temporary, text = "Close", command = partial(close, wn_temporary)).pack()
    def logout(self, window): # what occurs when a user presses the log out button in the main menu
        widgets = window.pack_slaves()
        for w in widgets:
            w.destroy()
        self.l_window(" ")
        window.withdraw()
    def check_user(self, var_student_id):
        cursor.execute("SELECT * FROM STUDENT WHERE STUDENTID = '%s'" %(var_student_id.get()))
        c.commit()
        if not(cursor.fetchall()):
            return True
        else:
            return False
        
class Queue: # a class to instantiate a queue
    def __init__(self):
        self._queue = []
    def get_queue(self):
        return self._queue
    def _find_length(self):
        return len(self._queue)
    def insert(self, data):
        self._queue.append(data)
    def isEmpty(self):
        if not self._queue:
            return True
        else:
            return False
    def pop(self): #coded myself
        value = self._queue[0]
        del self._queue[0]
        return value
        
class PriorityQueue(Queue): # priority queue used for tailored questions
    def __init__(self):
        Queue.__init__(self)
    def pop(self):
        try:
            min = 0
            for i in range(self._find_length()):
                if self._queue[i][1] < self._queue[min][1]:
                    min = i
            item = self._queue[min]
            del self._queue[min]
            return item
        except IndexError:
            pass

class Process:
    def __init__(self, u, p): # initialises variables for the object
        self._student = ""
        self._user = u
        self._pass = p
    def get_student(self): # used to find the student id in the student table based on the username and password
        cursor.execute("SELECT STUDENTID FROM STUDENT WHERE USERNAME = '%s' AND PASSWORD = '%s'" %(self._user, self._pass))
        c.commit()
        self._student = cursor.fetchall()[0]
        return self._student
    def get_level(self, student): # finds the difficulty level the student is currently at
        cursor.execute("SELECT LEVEL FROM STUDENT WHERE STUDENTID = '%s'" %(student))
        c.commit()
        return cursor.fetchone()
    def get_count(self): # finds the number of questions in the database
        cursor.execute("SELECT COUNT(*) FROM QUESTION")
        c.commit()
        return int(cursor.fetchone()[0])
    def get_initials(self): # used to fetch the unique identifier for the teacher
        cursor.execute("SELECT INITIALS FROM TEACHER WHERE USERT = '%s' AND PASST = '%s'" %(self._user, self._pass))
        c.commit()
        return cursor.fetchone()[0]
    def change(self, student, variable): # changes the difficulty of a student in the database
        self._student = student
        self.new = variable.get()
        sql = """UPDATE STUDENT
            SET LEVEL = '%s'
            WHERE STUDENTID = '%s'"""
        cursor.execute(sql %(self.new, self._student))
        c.commit()

class Progression:
    def __init__(self, u, p): # variables instantiated when the class is
        self.perc_q = []
        self.perc_t = []
        self.process_3 = Process(u, p)
        self.count = self.process_3.get_count()
        self.student = self.process_3.get_student()[0]
        self.level = self.process_3.get_level(self.student)
    def _get_response_correct(self, value): # returns something in integer form rather than tuple or array
        return value[0][0]
    def _calculating(self, answered, correct, i, percent): # calculates percentages using values passed in
        if answered == 0 or correct == 0:
            self.percentage = 0
        else:
            self.percentage = ((correct/answered)*100)
        percent.append((i, round(self.percentage)))
    def _output_progress(self, window, question_topic, attempts, correct): # outputs progress for the user to see
        for i in range(0, len(attempts)):
            txt = question_topic, (i+1), " ", correct[i], "/", attempts[i], " correct"
            Label(window, text = txt).pack()
    def topic_questions_p(self, topic): # this is used to help generate tailored questions for a user using the topic question window
        # it cannot use the same as the random question window as the questions need to be individual to the topic
        attempts = []
        correct = []
        perc = []
        cursor.execute("SELECT QUESTIONID FROM QUESTION WHERE TOPIC = '%s'" %(topic))
        c.commit()
        questions = cursor.fetchall()
        for i in questions:
            cursor.execute("SELECT COUNT(*) FROM ANSWER WHERE STUDENTID = '%s' AND QUESTIONID = '%s'" %(self.student, i[0]))
            c.commit()
            self.response = self._get_response_correct(cursor.fetchall())
            cursor.execute("SELECT COUNT(*) FROM ANSWER WHERE STUDENTID = '%s' AND QUESTIONID = '%s' AND SCORE = '%s'" %(int(self.student), i[0], 1))
            c.commit()
            self.correct = self._get_response_correct(cursor.fetchall())
            attempts.append(self.response)
            correct.append(self.correct)
            self._calculating(self.response, self.correct, i[0], perc)
        return perc
    def topic_p(self): # finds the percentage correct per topic
        attempts = []
        correct = []
        for i in range(1, 9):
            cursor.execute("""SELECT ANSWER.QUESTIONID FROM QUESTION, ANSWER WHERE QUESTION.TOPIC = '%s' AND ANSWER.STUDENTID = '%s'
                    AND QUESTION.QUESTIONID = ANSWER.QUESTIONID""" %(i, self.student))
            c.commit()
            self._questions_answered = cursor.fetchall()
            self.response = len(self._questions_answered)
            cursor.execute("""SELECT ANSWER.QUESTIONID FROM QUESTION, ANSWER WHERE QUESTION.TOPIC = '%s' AND ANSWER.STUDENTID = '%s'
                AND ANSWER.SCORE = 1 AND QUESTION.QUESTIONID = ANSWER.QUESTIONID""" %(i, self.student))
            c.commit()
            self._answered_correct = cursor.fetchall()
            self.corrects = len(self._answered_correct)
            self._calculating(self.response, self.corrects, i, self.perc_t)
            attempts.append(self.response)
            correct.append(self.corrects)
        return self.perc_t, attempts, correct
    def topic(self, window): # creates the progress window
        window.destroy()
        wn_subprogress = Toplevel(root)
        wn_subprogress.title("TOPIC PROGRESS")
        Button(wn_subprogress, text = "Back", command = partial(back, wn_subprogress, root)).pack()
        percentages, attempts, correct = self.topic_p()
        self._output_progress(wn_subprogress, "T", attempts, correct)
    def question_p(self): # finds the question percentages of how many times it has been answered correctly
        attempts = []
        correct = []
        for i in range(1, (self.count + 1)):
            cursor.execute("SELECT COUNT(*) FROM ANSWER WHERE STUDENTID = '%s' AND QUESTIONID = '%s'"%(self.student, i))
            c.commit()
            self.response = self._get_response_correct(cursor.fetchall())
            cursor.execute("SELECT COUNT(*) FROM ANSWER WHERE STUDENTID = '%s' AND QUESTIONID = '%s' AND SCORE = '%s'"%(int(self.student), i, 1))
            c.commit()
            self.correct = self._get_response_correct(cursor.fetchall())
            attempts.append(self.response)
            correct.append(self.correct)
            self._calculating(self.response, self.correct, i, self.perc_q)
        return self.perc_q, attempts, correct
    def question(self, window): # creates the question percentages window
        window.destroy()
        wn_subprogress = Toplevel(root)
        Button(wn_subprogress, text = "Back", command = partial(back, wn_subprogress, root)).pack()
        percentages, attempts, correct = self.question_p()
        self._output_progress(wn_subprogress, "Q", attempts, correct)
    def activity_graph(self): # creates and displays the graph for how a user has used their account
        cursor.execute("SELECT DATE_DONE FROM ANSWER WHERE STUDENTID = '%s' ORDER BY DATE_DONE ASC" %(self.student))
        c.commit()
        dates = cursor.fetchall()
        date_o = []
        for i in dates: # runs through all dates in database and organises them to be sorted through
            date_and_time = i[0].split(" ")
            date_o.append(date_and_time[0])
        prev = []
        activity = []
        for i in date_o:
            act = date_o.count(i)
            if i in prev: # could do a linear search - can't do binary search as not necessarily in order
                pass
            else:
                prev.append(i)
                activity.append(act)
        plt.plot(prev, activity)
        plt.xlabel("Date")
        plt.ylabel("Activity (questions answered per day)")
        plt.tick_params(axis = "x", rotation = 45)
        plt.show()
    def progress_graph(self): # creates and displays the graph for how they do in each topic
        percentages, attempts, correct = self.topic_p()
        topic = []
        percent = []
        for i in percentages:
            topic.append(i[0])
            percent.append(i[1])
        plt.barh(topic, percent)
        plt.xlabel("Percent correct")
        plt.ylabel("Topic number")
        plt.show()

class Question:
    def __init__(self, topic_num, window_type, window_name, u, p):
        self.process_1 = Process(u, p)
        self.student = self.process_1.get_student()
        self.level = self.process_1.get_level(self.student)
        self.topic = topic_num
        self.type = window_type
        self.window = window_name
        self.question_type = " "
        self._user = u
        self._pass = p
        if queue_wrong.isEmpty(): # if the user has not incorrectly answered any questions
            self.wrong = PriorityQueue()
            self.a_value = True
        else:
            self.a_value = False
    def _get_number(self, alist): # gets a random number from the given list
        return random.choice(alist)
    def _get_question(self, question_id): # selects the correct question from the database
        cursor.execute("SELECT QUESTION FROM QUESTION WHERE QUESTIONID = '%s' AND DIFFICULTY <= '%s'" %(question_id, self.level))
        c.commit()
        self._question = cursor.fetchone()
        Label(self.window, text = self._question).pack()
    def get_question_type(self, question_id): # this gets the question type of the question
        # useful for deciding what child class to instantiate
        cursor.execute("SELECT QUESTION_TYPE FROM TYPE WHERE QUESTIONID = '%s'" %(question_id))
        c.commit()
        return cursor.fetchone()
    def _selecting_question(self, questions): # 
        if self.type == "T":
            try:
                return self._get_number(questions)
            except IndexError:
                Label(self.window, text = "There are no questions in this topic").pack()
                return 0
        elif self.type == "R":
            try:
                return self._get_number(questions)[0]
            except IndexError:
                Label(self.window, text = "There are no questions.").pack()
                return 0
    def get_answer(self, question_id):
        cursor.execute("SELECT ANSWERM FROM QUESTION WHERE QUESTIONID = '%s'" %(question_id))
        c.commit()
        a = cursor.fetchall()[0][0]
        return a
    def _normal_question(self):
        if self.type == "T":
            cursor.execute("SELECT QUESTIONID FROM QUESTION WHERE TOPIC = '%s' AND DIFFICULTY <= '%s'" %(self.topic, self.level))
            c.commit()
            self.question_id = self._selecting_question(cursor.fetchall())
        elif self.type == "R":
            cursor.execute("SELECT QUESTIONID FROM QUESTION WHERE DIFFICULTY <= '%s'" %(self.level))
            c.commit()
            self.question_id = self._selecting_question(cursor.fetchall())
        return self.question_id
    def __wrong(self, alist, wrong):
        for a in alist:
            if a[1] <= 70:
                wrong.insert(a)
    def _tailored_question(self, topic):
        self.progression_2 = Progression(self._user, self._pass)
        if self.a_value:
            if self.type == "T":
                self._question_topic_percentages = self.progression_2.topic_questions_p(topic)
                self.__wrong(self._question_topic_percentages, self.wrong)
            elif self.type == "R":
                self._question_percentages, attempts, correct = self.progression_2.question_p()
                self.__wrong(self._question_percentages, self.wrong)
            try:
                self.question_id = self.wrong.pop()[0]
            except TypeError:
                Label(self.window, text = "There are no questions in this topic").pack()
        elif not(self.a_value) and self.type == "R": # if there are elements in the list
            self.question_id = queue_wrong.pop()
        else: # if no percentages below 70
            self.question_id = self._normal_question()
        return self.question_id
    def question(self, count):
        if (int(count)%3) == 0:
            self.question_id = self._tailored_question(self.topic)
        elif ((int(count)) == 0) or (int(count)%3 != 0):
            self.question_id = self._normal_question()
        cursor.execute("SELECT TOPIC FROM QUESTION WHERE QUESTIONID = '%s'"
                       %(self.question_id))
        c.commit()
        self.topic = cursor.fetchone()[0]
        info_button(self.window, self.topic)
        return self.question_id
    def marking(self, count, subtopic, s, opt, variables):
        return Mark(self.get_answer(self.question_id),
              count, self.question_id, self.window, self.topic,
              subtopic, self.type, self._user, self._pass)

class Multiple(Question):
    def __init__(self, topic_num, window_type, window_name, u, p, question_id):
        Question.__init__(self, topic_num, window_type, window_name, u, p)
        self.question_id = question_id
    def get_multiple_question(self, question_id):
        try:
            question_id = question_id[0]
        except TypeError:
            pass
        self._get_question(question_id)
        print(question_id)
        print(self.level)
        cursor.execute("""SELECT OPTION1, OPTION2, OPTION3, OPTION4 FROM TYPE,
                       QUESTION WHERE TYPE.QUESTIONID = '%s' AND
                       QUESTION.DIFFICULTY <= '%s' AND QUESTION.QUESTIONID
                       = TYPE.QUESTIONID""" %(question_id, self.level))
        c.commit()
        self._options = cursor.fetchall()[0]
        return self._get_multiple_variables() # returns variables, opt
    def _get_multiple_variables(self):
        var_opt = []
        var_variables = []
        for o in range(4):
            if self._options[o]:
                var_multiple_o = IntVar()
                var_variables.append(var_multiple_o)
                Checkbutton(self.window, text = self._options[o], variable = var_multiple_o).pack()
                var_opt.append((o, 0))
            else:
                pass
        return var_variables, var_opt
    def marking(self, count, subtopic, var_opt, var_variables):
        self.mark_1 = super().marking(count, subtopic, " ", var_opt, var_variables)
        Enter = Button(self.window, text = "Submit",
                       command = partial(self.mark_1.multiple, var_opt, var_variables)).pack()
    def question(self, subtopic, count):
        var_variables, var_opt = self.get_multiple_question(self.question_id)
        self.marking(count, subtopic, var_opt, var_variables)

class State(Question):
    def __init__(self, topic_num, window_type, window_name, u, p, question_id):
        Question.__init__(self, topic_num, window_type, window_name, u, p)
        self.question_id = question_id
    def get_question(self, question_id):
        var_s = StringVar()
        try:
            self._get_question(question_id[0])
        except TypeError:
            self._get_question(question_id)
        Entry(self.window, textvariable = var_s).pack(fill = X)
        return var_s
    def marking(self, count, subtopic, var_s):
        self.mark_1 = super().marking(count, subtopic, var_s, " ", " ")
        Enter = Button(self.window, text = "Submit",
                       command = partial(self.mark_1.state, var_s)).pack()
    def question(self, subtopic, count):
        var_s = self.get_question(self.question_id)
        var_variables, var_opt = " ", " "
        # EDIT MARKING CLASS
        self.marking(count, subtopic, var_s)

class Short(State, Question):
    def __init__(self, topic_num, window_type, window_name, u, p, question_id):
        State.__init__(self, topic_num, window_type, window_name, u, p, question_id)
    def marking(self, count, subtopic, var_s):
        self.mark_1  = Question.marking(self, count, subtopic, var_s, " ", " ")
        Enter = Button(self.window, text = "Submit",
                       command = partial(self.mark_1.short, var_s)).pack()

class Student:
    def __init__(self, u, p):
        try:
            self._user = u.get()
            self._pass = p.get()
        except AttributeError:
            self._user = u
            self._pass = p
    def m_window(self, count_t, count_r, window): # used to generate the main window for the student
        root.deiconify()
        window.destroy()
        root.title("MAIN MENU")
        root.geometry("300x400")
        logging_2 = Logging()
        Button(root, text = "Log Out", command = partial(logging_2.logout, root)).pack()
        Label(root, text = "Welcome").pack()
        Button(root, text = "Topics", command = self.t_window).pack()
        Button(root, text = "Random Questions", command = partial(self.r_window, count_r)).pack()
        Button(root, text = "Progress", command = self.p_window).pack()
        Button(root, text = "Assigned", command = self._get_assigned).pack()
    def t_window(self): # used to generate the topic window for the student
        root.withdraw()
        wn_topic = Toplevel(root)
        wn_topic.title("TOPIC")
        wn_topic.geometry("300x400")
        Button(wn_topic, text = "Back", command = partial(back, wn_topic, root)).pack()
        topics = open("GCSE_topics_overview.txt")
        count_i = 0
        for i in topics:
            count_i += 1
            Button(wn_topic, text = i, command = partial(self.st_window, i, count_i, count_t, wn_topic)).pack()
    def checking_question_type(self, typ, topic_num, window_type, window_name, subtopic, count, question_id):
        if typ == "S":
            state_1 = State(topic_num, window_type, window_name, self._user, self._pass, question_id)
            state_1.question(subtopic, count)
        elif typ == "SH":
            short_1 = Short(topic_num, window_type, window_name, self._user, self._pass, question_id)
            short_1.question(subtopic, count)
        elif typ == "M":
            multiple_1 = Multiple(topic_num, window_type, window_name, self._user, self._pass, question_id)
            multiple_1.question(subtopic, count)
    def st_window(self, subtopic, topic_num, count, window):
        window.destroy()
        wn_mini = Toplevel(root)
        wn_mini.title(subtopic)
        wn_mini.geometry("500x200")
        Button(wn_mini, text = "Back", command = partial(back, wn_mini, root)).pack()
        question_1 = Question(topic_num, "T", wn_mini, self._user, self._pass)
        self.question_id = question_1.question(count)
        self.type = question_1.get_question_type(self.question_id)
        self.checking_question_type(self.type[0], topic_num, "T", wn_mini, subtopic, count, self.question_id)
    def r_window(self, count):
        root.withdraw()
        wn_random = Toplevel(root)
        wn_random.title("RANDOM QUESTIONS")
        Button(wn_random, text = "Back", command = partial(back, wn_random, root)).pack()
        question_2 = Question(" ", "R", wn_random, self._user, self._pass)
        self.question_id = question_2.question(count)
        self.type = question_2.get_question_type(self.question_id)
        self.checking_question_type(self.type[0], " ", "R", wn_random, " ", count, self.question_id)
    def p_window(self):
        root.withdraw()
        wn_progress = Toplevel(root)
        wn_progress.title("PROGRESS")
        wn_progress.geometry("300x400")
        progression_1 = Progression(self._user, self._pass)
        Button(wn_progress, text = "Back", command = partial(back, wn_progress, root)).pack()
        Button(wn_progress, text = "Topic", command = partial(progression_1.topic, wn_progress)).pack()
        Button(wn_progress, text = "Question", command = partial(progression_1.question, wn_progress)).pack()
        Button(wn_progress, text = "Activity", command = progression_1.activity_graph).pack()
        Button(wn_progress, text = "Progress graph", command = progression_1.progress_graph).pack()
    def _get_assigned(self):
        wn_assigned = Toplevel(root)
        wn_assigned.title("Questions")
        process_5 = Process(self._user, self._pass)
        cursor.execute("""SELECT QUESTIONID FROM ASSIGNED WHERE
                       STUDENTID = '%s'""" %(process_5.get_student()))
        c.commit()
        question_ids = cursor.fetchall()
        for i in question_ids:
            txt = "Question " + str(i[0])
            Button(wn_assigned, text = txt,
                   command = partial(self.get_assigned_question, i[0], 0)).pack()
        Button(self.window, text = "Close window", command = partial(close, wn_assigned)).pack()
    def get_assigned_question(self, question_id, count):
        wn_assigned_question = Toplevel(root)
        wn_assigned_question.title("Question")
        Button(wn_assigned_question, text = "Back",
               command = partial(back, wn_assigned_question, root)).pack()
        question_3 = Question(" ", " ", wn_assigned_question, self._user, self._pass)
        self.type = question_3.get_question_type(question_id)[0]
        self.answer = question_3.get_answer(question_id)
        self.checking_question_type(self.type, " ", " ", wn_assigned_question, " ", count, question_id)


class Mark:
    def __init__(self, answer, count, question_id, window_name, topic_num, subtopic_name, window_type, u, p):
        self.answer = answer # the actual answer
        self.question_id = question_id
        self.window = window_name
        self.topic_number = topic_num
        self.subtopic = subtopic_name
        self.type = window_type
        self.count = count
        self.date = datetime.datetime.now()
        self.count += 1
        self._user = u
        self._pass = p
        self.value = False
    def state(self, var):
        self.input = var.get()
        if not(self.input): # modify to while loop and keep regenerating same question
            # until they give an answer?
            Label(self.window, text = "Nothing was entered").pack()
        self.calculating(self.input, self.answer)
    def selected(self, options, variables):
        selected = []
        for o in range(len(variables)): # tried with o in variables
            # didnt work with fetching data
            if variables[o].get() == 1:
                selected.append((o, 1))
        return selected
    def multiple(self, opt, variables):
        selected = self.selected(opt, variables)
        cursor.execute("""SELECT OPTION1, OPTION2, OPTION3, OPTION4
                       FROM TYPE WHERE QUESTIONID = '%s'"""
                       %(self.question_id))
        c.commit()
        self.options = cursor.fetchall()[0]
        if len(selected) != 1:
            Label(self.window, text = "Error. Incorrect number of checkboxes selected. You may only select one.").pack()
            Label(self.window, text = self.answer).pack()
            user_answer = ""
            self.calculating(user_answer, self.answer)
        else:
            user_answer = self.options[selected[0][0]]
            self.calculating(user_answer, self.answer)
    def short(self, var):
        cursor.execute("SELECT OPTION1, OPTION2, OPTION3, OPTION4 FROM TYPE WHERE QUESTIONID = '%s'" %(self.question_id))
        c.commit()
        self.points = cursor.fetchall()[0]
        points = 0
        count = 0
        self.input = var.get().lower()
        if not(self.value):
            if not(self.input): # modify to while loop and keep regenerating same question
                # until they give an answer?
                Label(self.window, text = "Nothing was entered").pack()
            for i in self.points:
                if i:
                    points += 1
                    if i.lower() in self.input:
                        count += 1
            if points == count:
                Label(self.window, text = "Correct").pack()
                value = True
            else:
                Label(self.window, text = "Incorrect").pack()
                value = False
                queue_wrong.insert(self.question_id)
            Label(self.window, text = "Please mention: ").pack()
            for i in self.points:
                Label(self.window, text = i).pack()
            if self.type != " ":
                self._next_button(self.input, value)
        else:
            Label(self.window, text = "You have already submitted your answer for this question. Please click NEXT").pack()
    def calculating(self, user_input, answer):
##        cursor.execute("SELECT * FROM ANSWER WHERE DATE_DONE = '%s'" %(self.date))
##        temp = cursor.fetchone()
##        print(temp)
##        if temp is None:
        if not(self.value):
            if str(user_input).lower() == str(answer).lower():
                Label(self.window, text = "Correct").pack()
                value = True
            else:
                Label(self.window, text = "Incorrect").pack()
                Label(self.window, text = answer).pack()
                value = False
                queue_wrong.insert(self.question_id)
            if self.type != " ":
                self._next_button(user_input, value)
            else:
                self.add_to_database(user_input, value)
        else:
            print("A")
            Label(self.window, text = "You have already submitted your answer for this question. Please click NEXT").pack()
    def _next_button(self, user_input, value):
        Button(self.window, text = "NEXT",
               command = partial(clear, self.window, self.topic_number, self.subtopic, self.type, self.count, self._user, self._pass)).pack()
        self.add_to_database(user_input, value)
    def add_to_database(self, user_input, value):
        process_2 = Process(self._user, self._pass)
        self.student = process_2.get_student()[0]
        try:
            self.question_id = self.question_id[0]
        except TypeError:
            pass
        try:
            cursor.execute("SELECT * FROM ANSWER WHERE DATE_DONE = '%s'" %(self.date))
            temp = cursor.fetchone()
            print(temp)
            if temp is None:
                c.execute("INSERT INTO ANSWER(ANSWERS, STUDENTID, QUESTIONID, DATE_DONE, SCORE)\
                    VALUES(?, ?, ?, ?, ?)", (user_input, self.student, self.question_id, self.date, value))
                c.commit()
                self.value = True
            else:
                print("B")
                self.value = True
                Label(self.window, text = "You have already submitted your answer for this question. Please click NEXT").pack()
        except sqlite3.IntegrityError: # no longer an integrity error as answer is also a primary key
            if not(user_input):
                Label(self.window, text = "No answer was entered").pack()
            else:
                Label(self.window, text = "This question has already been answered. Please move on").pack()
        if self.type == " ":
            cursor.execute("DELETE FROM ASSIGNED WHERE QUESTIONID = '%s'" %(self.question_id))
            c.commit()
            Button(self.window, text = "Close window", command = partial(close, self.window)).pack()

class Teacher:
    def __init__(self, u, p):
        self._user = u.get()
        self._pass = p.get()
        self.process_4 = Process(self._user, self._pass)
    def tm_window(self, window): # used to display the main menu for the teacher
        window.destroy()
        root.deiconify()
        root.title("MAIN MENU")
        root.geometry("300x400")
        logging_3 = Logging()
        Button(root, text = "Log Out", command = partial(logging_3.logout, root)).pack()
        Button(root, text = "Students", command = self.classes).pack()
        Button(root, text = "Add Questions", command = self.add_questions).pack()
        Button(root, text = "Questions", command = self.questions).pack()
    def classes(self):
        root.withdraw()
        wn_teach_class = Toplevel(root)
        wn_teach_class.title("CLASS")
        wn_teach_class.geometry("300x400")
        Button(wn_teach_class, text = "Back", command = partial(back, wn_teach_class, root)).pack()
        initials = self.process_4.get_initials()
        cursor.execute("SELECT FIRSTNAME, STUDENTID FROM STUDENT WHERE CLASS = '%s'" %(initials))
        c.commit()
        students = cursor.fetchall()
        for i in students:
            Button(wn_teach_class, text = i[0], command = partial(self._student_menu, wn_teach_class, i)).pack()
    def _student_menu(self, window, student): # used to show what different things a teacher can do with a student account
        window.destroy()
        wn_student_menu = Toplevel(root)
        wn_student_menu.title(student[0])
        wn_student_menu.geometry("300x400")
        cursor.execute("SELECT USERNAME, PASSWORD FROM STUDENT WHERE STUDENTID = '%s'" %(student[1]))
        c.commit()
        u_and_p = cursor.fetchall()[0]
        user, pas = u_and_p[0], u_and_p[1]
        progression_3 = Progression(user, pas)
        Button(wn_student_menu, text = "Back", command = partial(back, wn_student_menu, root)).pack()
        Button(wn_student_menu, text = "Change difficulty", command = partial(self.difficulty, wn_student_menu, student[0], student[1])).pack()
        Button(wn_student_menu, text = "Assign question", command = partial(self.assign, student[1], wn_student_menu)).pack()
        Button(wn_student_menu, text = "Activity", command = progression_3.activity_graph).pack()
        Button(wn_student_menu, text = "Progress", command = progression_3.progress_graph).pack()

    def _difficulties(self, window):
        alist = {1, 2, 3}
        var_level = IntVar()
        Label(window, text = "1 is easiest, 3 is hardest").pack()
        OptionMenu(window, var_level, *alist).pack()
        return var_level
    def difficulty(self, window, student, student_id):
        window.destroy()
        wn_teach_diff = Toplevel(root)
        wn_teach_diff.title("Difficulty")
        wn_teach_diff.geometry("300x200")
        Button(wn_teach_diff, text = "Back", command = partial(back, wn_teach_diff, root)).pack()
        current = self.process_4.get_level(student_id)
        var_level = self._difficulties(wn_teach_diff)
        var_level.set(current)
        submit = Button(wn_teach_diff, text = "Submit", command = partial(self.process_4.change, student_id, var_level)).pack()
        c.commit()
    def assign(self, student_id, window):
        window.destroy()
        wn_assign = Toplevel(root)
        wn_assign.title("Assign")
        wn_assign.geometry("400x350")
        Button(wn_assign, text = "Back", command = partial(back, wn_assign, root)).pack()
        var_search = StringVar()
        Label(wn_assign, text = "Search by question number").pack()
        Entry(wn_assign, textvariable = var_search).pack()
        Button(wn_assign, text = "Search", command = partial(self.process_assign, wn_assign, var_search, student_id)).pack()
    def process_assign(self, window, var_search, student_id):
        question_info, type_info = self.search_questions(var_search, window)
        cursor.execute("SELECT QUESTION, ANSWERM, TOPIC FROM QUESTION WHERE QUESTIONID = '%s'" %(question_info[0]))
        c.commit()
        details = cursor.fetchall()[0]
        Label(window, text = "Question").pack()
        Label(window, text = details[0]).pack()
        Label(window, text = "Answer").pack()
        Label(window, text = details[1]).pack()
        Label(window, text = "Topic").pack()
        Label(window, text = str(details[2])).pack()
        Button(window, text = "Assign", command = partial(self.assign_to_database, student_id, question_info[0], window)).pack(side = BOTTOM)
    def assign_to_database(self, student_id, question_id, window):
        cursor.execute("SELECT * FROM ASSIGNED WHERE QUESTIONID = '%s' AND STUDENTID = '%s'" %(question_id, student_id))
        c.commit()
        try:
            initials = self.process_4.get_initials()
            cursor.execute("""INSERT INTO ASSIGNED(STUDENTID, QUESTIONID, INITIALS)
                           VALUES(?, ?, ?)""", (student_id, question_id, initials))
            c.commit()
            self.assign(student_id, window)
        except sqlite3.IntegrityError:
            Label(window, text = "This question has already been assigned to this student.").pack()
    def add_questions(self): # displays the window for the teacher to add questions
        root.withdraw()
        wn_teach_questions = Toplevel(root)
        wn_teach_questions.title("QUESTIONS")
        wn_teach_questions.geometry("300x400")
        Button(wn_teach_questions, text = "Back", command = partial(back, wn_teach_questions, root)).pack()
        Button(wn_teach_questions, text = "Multiple Choice", command = partial(self._add_multiple, wn_teach_questions)).pack()
        Button(wn_teach_questions, text = "State", command = partial(self._add_state, wn_teach_questions)).pack()
        Button(wn_teach_questions, text = "Short answer", command = partial(self._add_short, wn_teach_questions)).pack()
    def _teacher_input(self, window, text, variable): # used to generally allow teachers to enter details
        Label(window, text = text).pack()
        Entry(window, textvariable = variable).pack()
    def _topic_difficulty(self, window):
        topics = {1, 2, 3, 4, 5, 6, 7, 8}
        var_topic = IntVar()
        Label(window, text = "Topic").pack()
        OptionMenu(window, var_topic, *topics).pack()
        Label(window, text = "Difficulty").pack()
        var_level = self._difficulties(window)
        return var_level, var_topic
    def _add_options(self, window, word): # used to create the variables for options or marking points
        variables = []
        for i in range(4):
            self.variable_i = StringVar()
            variables.append(self.variable_i)
        for i in range(4):
            Label(window, text = (word, (i+1))).pack()
            Entry(window, textvariable = variables[i]).pack()
        return variables
    def _add_multiple(self, window): # used to add a multiple choice question to the database
        window.destroy()
        wn_add_multiple = Toplevel(root)
        wn_add_multiple.title("300x500")
        Button(wn_add_multiple, text = "Back", command = partial(back, wn_add_multiple, root)).pack()
        var_question = StringVar()
        self._teacher_input(wn_add_multiple, "Question", var_question)
        variables = self._add_options(wn_add_multiple, "Option")
        var_answer = StringVar()
        self._teacher_input(wn_add_multiple, "Answer", var_answer)
        var_level, var_topic = self._topic_difficulty(wn_add_multiple)
        Button(wn_add_multiple, text = "ADD", command = partial(self._to_database, "M", wn_add_multiple, var_question, var_answer, var_topic, var_level, variables)).pack()
    def _add_state(self, window): # used to add a state question to the database
        window.destroy()
        wn_add_state = Toplevel(root)
        wn_add_state.title("STATE")
        wn_add_state.geometry("300x500")
        Button(wn_add_state, text = "Back", command = partial(back, wn_add_state, root)).pack()
        var_question = StringVar()
        self._teacher_input(wn_add_state, "Question", var_question)
        var_answer = StringVar()
        self._teacher_input(wn_add_state, "Answer", var_answer)
        var_level, var_topic = self._topic_difficulty(wn_add_state)
        Button(wn_add_state, text = "ADD", command = partial(self._to_database, "S", wn_add_state, var_question, var_answer, var_topic, var_level, " ")).pack()
    def _add_short(self, window): # used to add short answer questions to the database
        window.destroy()
        wn_add_short = Toplevel(root)
        wn_add_short.title("Short")
        wn_add_short.geometry("300x500")
        Button(wn_add_short, text = "Back", command = partial(back, wn_add_short, root)).pack()
        var_question = StringVar()
        self._teacher_input(wn_add_short, "Question", var_question)
        variables = self._add_options(wn_add_short, "Marking point")
        var_level, var_topic = self._topic_difficulty(wn_add_short)
        Button(wn_add_short, text = "ADD", command = partial(self._to_database, "SH", wn_add_short, var_question, " ", var_topic, var_level, variables)).pack()
    def _to_database(self, question_type, window, var_question, var_answer, var_topic, var_level, variables):
        cursor.execute("SELECT MAX(QUESTIONID) FROM QUESTION")
        c.commit()
        question_id = cursor.fetchone()[0] + 1
        if question_type == "S":
            if (var_question.get() or var_answer.get()) == "":
                self.invalid_entry()
            else:
                cursor.execute("INSERT INTO QUESTION(QUESTIONID, QUESTION, ANSWERM, TOPIC, DIFFICULTY)\
                                VALUES(?, ?, ?, ?, ?)", (question_id, var_question.get(), var_answer.get(), var_topic.get(), var_level.get()))
                cursor.execute("INSERT INTO TYPE(QUESTIONID, QUESTION_TYPE)\
                                VALUES(?, ?)", (question_id, "S"))
        elif question_type == "M":
            if ((var_question.get() or var_answer.get()) == "") or (not(self.checking_presence(variables))):
                self.invalid_entry()
            else:
                cursor.execute("INSERT INTO QUESTION(QUESTIONID, QUESTION, ANSWERM, TOPIC, DIFFICULTY)\
                               VALUES(?, ?, ?, ?, ?)", (question_id, var_question.get(), var_answer.get(), var_topic.get(), var_level.get()))
                cursor.execute("INSERT INTO TYPE(QUESTIONID, QUESTION_TYPE, OPTION1, OPTION2, OPTION3, OPTION4)\
                                VALUES(?, ?, ?, ?, ?, ?)", (question_id, "M", variables[0].get(), variables[1].get(), variables[2].get(), variables[3].get()))
        elif question_type == "SH":
            if not(self.checking_presence(variables)):
                self.invalid_entry()
            else:
                cursor.execute("INSERT INTO QUESTION(QUESTIONID, QUESTION, TOPIC, DIFFICULTY)\
                                VALUES(?, ?, ?, ?)", (question_id, var_question.get(), var_topic.get(), var_level.get()))
                cursor.execute("INSERT INTO TYPE(QUESTIONID, QUESTION_TYPE, OPTION1, OPTION2, OPTION3, OPTION4)\
                                VALUES(?, ?, ?, ?, ?, ?)", (question_id, "SH", variables[0].get(), variables[1].get(), variables[2].get(), variables[3].get()))
        c.commit()
        Label(window, text = "Added").pack()
        if question_type == "S":
            self._add_state(window)
        elif question_type == "M":
            self._add_multiple(window)
        elif question_type == "SH":
            self._add_short(window)
    def invalid_entry(self):
        wn_temporary = Toplevel(root)
        wn_temporary.title("ERROR")
        Label(wn_temporary, text = "Error. One or more fields have not been filled. Please fix.").pack()
    def checking_presence(self, variables):
        for i in variables:
            if i.get() == "":
                pass
            else:
                return True
        return False
    def questions(self): # shows the questions to the user
        root.withdraw()
        wn_questions = Toplevel(root)
        wn_questions.geometry("400x300")
        Button(wn_questions, text = "Back", command = partial(back, wn_questions, root)).pack()
        Button(wn_questions, text = "Edit", command = partial(self.edit_questions, wn_questions)).pack()
        cursor.execute("SELECT QUESTION, QUESTIONID FROM QUESTION ORDER BY QUESTIONID ASC") # use bubble sort instead of ascending
        c.commit()
        questions = cursor.fetchall()
        scrollbar = Scrollbar(wn_questions)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar_2 = Scrollbar(wn_questions, orient = HORIZONTAL)
        scrollbar_2.pack(side=BOTTOM, fill = X)
        quest = Listbox(wn_questions, yscrollcommand = scrollbar.set, width = 40, xscrollcommand = scrollbar_2.set)
        for i in questions:
            text = str(i[1]) + ". " + i[0]
            quest.insert(END, text)
        quest.pack(side=LEFT, fill = BOTH)
        scrollbar.config(command = quest.yview)
        scrollbar_2.config(command = quest.xview)
    def edit_questions(self, window): # used to create a window to edit questions
        window.destroy()
        wn_edit = Toplevel(root)
        wn_edit.title("Edit")
        wn_edit.geometry("400x650")
        Button(wn_edit, text = "Back", command = partial(back, wn_edit, root)).pack()
        var_search = StringVar()
        Label(wn_edit, text = "Search question by question number").pack()
        Entry(wn_edit, textvariable = var_search).pack()
        Button(wn_edit, text = "Search", command = partial(self.get_questions, var_search, wn_edit)).pack()
    def search_questions(self, question_id, window): # used to search the table of questions by question id
        try:
            cursor.execute("SELECT * FROM QUESTION WHERE QUESTIONID = '%s'" %(int(question_id.get())))
            c.commit()
            information = cursor.fetchall()[0]
            cursor.execute("SELECT * FROM TYPE WHERE QUESTIONID = '%s'" %(int(question_id.get())))
            c.commit()
            typ = cursor.fetchall()[0]
            return information, typ
        except IndexError:
            Label(window, text = "That question number does not exist. Please try again").pack()
        except ValueError:
            Label(window, text = "You did not enter anything").pack()
        except TypeError:
            Label(window, text = "You did not enter an integer").pack()
    def get_questions(self, question_id, window): # used to get the questions to display
        question_info, type_info = self.search_questions(question_id, window)
        Label(window, text = "Question").pack()
        Label(window, text = question_info[1]).pack()
        var_question = StringVar()
        Entry(window, textvariable = var_question).pack(fill = X)
        variables = []
        if type_info[1] == "SH":
            for i in range(4):
                txt = "Marking point" + str(i+1)
                Label(window, text = txt).pack()
                Label(window, text = type_info[i+2]).pack()
                var_i = StringVar()
                variables.append(var_i)
                Entry(window, textvariable = var_i).pack()
        else:
            Label(window, text = "Answer").pack()
            var_answer = StringVar()
            Label(window, text = question_info[2]).pack()
            Entry(window, textvariable = var_answer).pack(fill = X)
            if type_info[1] == "M":
                for i in range(4):
                    txt = "Option" + str(i+1)
                    Label(window, text = txt).pack()
                    Label(window, text = type_info[i+2]).pack()
                    var_i = StringVar()
                    variables.append(var_i)
                    Entry(window, textvariable = var_i).pack()
        var_level, var_topic = self._topic_difficulty(window)
        var_topic.set(question_info[3])
        var_level.set(question_info[4])
        if type_info[1] == "SH":
            Button(window, text = "Change", command = partial(self._change, question_id.get(), var_question, " ", var_level, var_topic, variables, window)).pack(side = BOTTOM)
        elif type_info[1] == "M":
            Button(window, text = "Change", command = partial(self._change, question_id.get(), var_question, var_answer, var_level, var_topic, variables, window)).pack(side = BOTTOM)
        else:
            Button(window, text = "Change", command = partial(self._change, question_id.get(), var_question, var_answer, var_level, var_topic, " ", window)).pack(side = BOTTOM)
        Button(window, text = "Delete", command = partial(self.are_you_sure, question_id.get())).pack()
    def _change(self, question_id, var_question, var_answer, var_level, var_topic, variables, window): # used to change the question in the database
        value = False
        if var_answer == " ": # short answer question
            if not(self.checking_presence(variables)):
                self.invalid_entry()
                value = True
            else:
                sql = """UPDATE QUESTION
                    SET QUESTION = '%s',
                    DIFFICULTY = '%s',
                    TOPIC = '%s'
                    WHERE QUESTIONID = '%s'"""
                cursor.execute(sql %(var_question.get(), var_level.get(), var_topic.get(), question_id))
                c.commit()
                self.edit_questions(window)
        else:
            if ((var_question.get() or var_answer.get()) == ""):
                self.invalid_entry()
                value = True
            else:
                sql = """UPDATE QUESTION
                    SET QUESTION = '%s',
                    ANSWERM = '%s',
                    DIFFICULTY = '%s',
                    TOPIC = '%s'
                    WHERE QUESTIONID = '%s'"""
                cursor.execute(sql %(var_question.get(), var_answer.get(), var_level.get(), var_topic.get(), question_id))
                c.commit()
                self.edit_questions(window)
        if variables != " ":
            if (not(self.checking_presence(variables))) and not(value):
                self.invalid_entry()
            else:
                sql = """UPDATE TYPE
                    SET OPTION1 = '%s',
                    OPTION2 = '%s',
                    OPTION3= '%s',
                    OPTION4 = '%s'
                    WHERE QUESTIONID = '%s'"""
                cursor.execute(sql %(question_id, variables[0].get(), variables[1].get(), variables[2].get(), variables[3].get()))
                c.commit()
                
                #self.edit_questions(window)
    def are_you_sure(self, question_id): # used to check the user definitely wants to delete the question
        window = Toplevel(root)
        window.geometry("300x200")
        Label(window, text = "Are you sure you want to delete this question?").pack()
        Button(window, text = "Yes", command = partial(self.delete, question_id, window)).pack()
        Button(window, text = "No", command = window.destroy).pack()
    def delete(self, question_id, window): # used to let the user delete a question from the database
        window.destroy()
        cursor.execute("DELETE FROM QUESTION WHERE QUESTIONID = '%s'" %(question_id))
        c.commit() # combine these two sql statements
        cursor.execute("DELETE FROM TYPE WHERE QUESTIONID = '%s'" %(question_id))
        c.commit()
        self.edit_questions(window)

def back(old, new):
    old.destroy()
    if 'normal' != new.state():
        new.deiconify()

def clear(window, topic_num, subtopic, window_type, count, u, p): # clears a window and recreates it - used for answering questions
    window.destroy()
    student_1 = Student(u, p)
    if window_type == "R":
        student_1.r_window(count)
    elif window_type == "T":
        student_1.st_window(subtopic, topic_num, count, window)

def info_button(window, line): # gives the user some help on a topic
    Button(window, text = "INFO", command = partial(information, line)).pack()

def information(line): # fetches the data from a textfile
    info_page = Toplevel(root)
    root.geometry("100x100")
    file = open("Info.txt")
    topic_info = file.readlines()
    Label(info_page, text = "Chapter").pack()
    Label(info_page, text = topic_info[line]).pack()

def close(self, window):
    window.destroy()
    
if __name__ == '__main__':
    global root
    global queue_wrong
    root = Tk()
    root.withdraw()
    queue_wrong = Queue()
    c = sqlite3.connect("quiz.db")
    cursor = c.cursor()
    count_t = 0
    count_r = 0
    logging_1 = Logging()
    logging_1.l_window(" ")
    root.mainloop()

# No next button when multiple choice is wrong
# No nothing is entered when tailored
