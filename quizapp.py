import tkinter as tk

from tkinter import messagebox

from tkinter.ttk import Progressbar

import random

import json

import os

SESSION_FILE = "session.json"

DATA_FILE = "user_data.json"

---------------- QUIZ DATA ----------------

quiz_data = {

"Easy": [

{"q": "What is the extension of Python file?", "options": [".py", ".java",

".cpp", ".txt"], "ans": 0},

{"q": "Which keyword defines function?", "options": ["func", "def",

"function", "define"], "ans": 1},

{"q": "Which data type stores text?", "options": ["int", "float", "str",

"bool"], "ans": 2},

{"q": "Symbol for comment?", "options": ["//", "#", "/* */", "--"], "ans":

1},

{"q": "Output of print(2+3)?", "options": ["5", "23", "Error", "None"],

"ans": 0}

],

"Medium": [

{"q": "Which keyword is used for loop?", "options": ["loop", "iterate",

"for", "repeat"], "ans": 2},

{"q": "Which function takes input?", "options": ["get()", "input()",

"read()", "scan()"], "ans": 1},

{"q": "Mutable data type?", "options": ["tuple", "string", "list", "int"],

"ans": 2},

{"q": "type(10) returns?", "options": ["int", "<class 'int'>", "number",

"integer"], "ans": 1},

{"q": "Conditional keyword?", "options": ["if", "when", "check", "condition"], "ans": 0}

],

"Hard": [

{"q": "Which is not a Python data type?", "options": ["set", "map", "list",

"tuple"], "ans": 1},

{"q": "Output of len('Hello')?", "options": ["4", "5", "6", "Error"], "ans":

1},

{"q": "Which operator is used for exponent?", "options": ["^", "**", "//",

"%"], "ans": 1},

{"q": "Which keyword is used for exception handling?", "options": ["try",

"catch", "error", "handle"], "ans": 0},

{"q": "What does 'break' do?", "options": ["Stops loop", "Skips iteration",

"Ends program", "Restarts loop"], "ans": 0}

]

}

class QuizApp:

def init(self, root):

self.root = root

self.root.title("Quiz App")

self.root.geometry("550x650")

session = self.load_session()

if session:

self.name = session["name"]

self.roll = session["roll"]

self.dashboard_screen()

else:

self.login_screen()

---------------- UI ----------------

def set_background(self, level=None):

colors = {

"Easy": "#d4f7d4",

"Medium": "#fff4cc",

"Hard": "#ffd6d6"

}
bg = colors.get(level, "#f0f0f0")

self.root.configure(bg=bg)

---------------- SESSION ----------------

def save_session(self):

with open(SESSION_FILE, "w") as f:

json.dump({"name": self.name, "roll": self.roll}, f)

def load_session(self):

if os.path.exists(SESSION_FILE):

try:

with open(SESSION_FILE, "r") as f:

return json.load(f)

except:

return None

return None

def clear_session(self):

if os.path.exists(SESSION_FILE):

os.remove(SESSION_FILE)

---------------- DATA ----------------

def get_user_key(self):

return f"{self.name}_{self.roll}"

def load_data(self):

if os.path.exists(DATA_FILE):

try:

with open(DATA_FILE, "r") as f:

return json.load(f)

except:

return {}

return {}

def save_user_score(self):

data = self.load_data()

key = self.get_user_key()
if key not in data:

data[key] = {"Easy": [], "Medium": [], "Hard": []}

data[key][self.selected_level].append(self.score)

with open(DATA_FILE, "w") as f:

json.dump(data, f)

def get_history_text(self):

data = self.load_data()

history = data.get(self.get_user_key(), {"Easy": [], "Medium": [], "Hard":

[]})

text = ""

for level in ["Easy", "Medium", "Hard"]:

scores = history[level]

if scores:

text += f"{level} → Attempts: {len(scores)} | Scores: {scores} | Best:

{max(scores)}\n"

else:

text += f"{level} → No attempts\n"

return text

---------------- LOGIN ----------------

def login_screen(self):

self.clear_screen()

self.set_background()

tk.Label(self.root, text="Quiz App Login", font=("Arial", 16,

"bold")).pack(pady=20)

tk.Label(self.root, text="Name").pack()

self.name_entry = tk.Entry(self.root)

self.name_entry.pack()

tk.Label(self.root, text="Roll No").pack()
self.roll_entry = tk.Entry(self.root)

self.roll_entry.pack()

tk.Button(self.root, text="Login", command=self.login).pack(pady=15)

def login(self):

self.name = self.name_entry.get()

self.roll = self.roll_entry.get()

if not self.name or not self.roll:

messagebox.showwarning("Warning", "Enter all details")

return

self.save_session()

self.dashboard_screen()

---------------- DASHBOARD ----------------

def dashboard_screen(self):

self.stop_timer()

self.clear_screen()

self.set_background()

tk.Label(self.root, text="Dashboard", font=("Arial", 16,

"bold")).pack(pady=10)

tk.Label(self.root, text=f"Name: {self.name}").pack()

tk.Label(self.root, text=f"Roll No: {self.roll}").pack()

tk.Label(self.root, text="Select Difficulty").pack(pady=10)

self.level = tk.StringVar(value="Easy")

for lvl in ["Easy", "Medium", "Hard"]:

tk.Radiobutton(self.root, text=lvl, variable=self.level, value=lvl).pack()

tk.Button(self.root, text="Start Quiz",

command=self.start_quiz).pack(pady=10)

tk.Button(self.root, text=" View History",

command=self.show_history).pack(pady=5)
tk.Button(self.root, text=" Logout",

command=self.logout).pack(pady=5)

def show_history(self):

messagebox.showinfo("History", self.get_history_text())

def logout(self):

self.clear_session()

self.login_screen()

---------------- QUIZ ----------------

def start_quiz(self):

self.selected_level = self.level.get()

self.quiz = random.sample(quiz_data[self.selected_level],

len(quiz_data[self.selected_level]))

self.index = 0

self.score = 0

self.user_answers = [None] * len(self.quiz)

self.time_left = {"Easy":120, "Medium":180,

"Hard":300}[self.selected_level]

self.quiz_screen()

def quiz_screen(self):

self.clear_screen()

self.set_background(self.selected_level)

self.timer_label = tk.Label(self.root, fg="red")

self.timer_label.pack()

self.progress_label = tk.Label(self.root)

self.progress_label.pack()

self.progress_bar = Progressbar(self.root, length=300)

self.progress_bar.pack()
self.question_label = tk.Label(self.root, wraplength=400)

self.question_label.pack(pady=10)

self.var = tk.IntVar(value=-1)

self.options = []

for i in range(4):

rb = tk.Radiobutton(self.root, text="", variable=self.var, value=i)

rb.pack(anchor='w')

self.options.append(rb)

btn = tk.Frame(self.root)

btn.pack(pady=10)

tk.Button(btn, text="Back", command=self.prev_question).grid(row=0,

column=0)

tk.Button(btn, text="Skip", command=self.skip_question).grid(row=0,

column=1)

tk.Button(btn, text="Next", command=self.next_question).grid(row=0,

column=2)

tk.Button(btn, text="Exit", command=self.exit_quiz).grid(row=0,

column=3)

self.load_question()

self.update_timer()

def exit_quiz(self):

self.stop_timer()

self.dashboard_screen()

def load_question(self):

q = self.quiz[self.index]

self.question_label.config(text=f"Q{self.index+1}. {q['q']}")

for i in range(4):

self.options[i].config(text=q["options"][i])
self.progress_label.config(text=f"Question

{self.index+1}/{len(self.quiz)}")

self.progress_bar['value'] = ((self.index+1)/len(self.quiz))*100

val = self.user_answers[self.index]

self.var.set(-1 if val is None else val)

def next_question(self):

if self.var.get() == -1:

messagebox.showwarning("Warning", "Select answer or skip")

return

self.user_answers[self.index] = self.var.get()

if self.index == len(self.quiz)-1:

self.show_result()

return

self.index += 1

self.load_question()

def prev_question(self):

if self.index > 0:

self.user_answers[self.index] = self.var.get()

self.index -= 1

self.load_question()

def skip_question(self):

self.user_answers[self.index] = self.var.get()

if self.index == len(self.quiz)-1:

self.show_result()

return

self.index += 1

self.load_question()

---------------- TIMER ----------------

def update_timer(self):

mins = self.time_left // 60

secs = self.time_left % 60

self.timer_label.config(text=f"Time Left: {mins:02d}:{secs:02d}")

if self.time_left > 0:

self.time_left -= 1

self.timer_id = self.root.after(1000, self.update_timer)

else:

messagebox.showinfo("Time Up", "Quiz submitted!")

self.show_result()

def stop_timer(self):

if hasattr(self, 'timer_id'):

self.root.after_cancel(self.timer_id)

---------------- RESULT (SCROLLABLE) ----------------

def show_result(self):

self.stop_timer()

self.clear_screen()

self.set_background(self.selected_level)

self.score = 0

canvas = tk.Canvas(self.root)

scrollbar = tk.Scrollbar(self.root, orient="vertical",

command=canvas.yview)

scroll_frame = tk.Frame(canvas)

scroll_frame.bind(

"<Configure>",

lambda e: canvas.configure(scrollregion=canvas.bbox("all"))

)
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)

scrollbar.pack(side="right", fill="y")

tk.Label(scroll_frame, text="Quiz Result", font=("Arial", 16,

"bold")).pack(pady=10)

for i, q in enumerate(self.quiz):

correct = q["ans"]

user = self.user_answers[i]

frame = tk.Frame(scroll_frame, bd=1, relief="solid", padx=5, pady=5)

frame.pack(fill="x", pady=5, padx=10)

tk.Label(frame, text=f"Q{i+1}. {q['q']}", font=("Arial", 10, "bold"),

wraplength=450).pack(anchor="w")

for idx, option in enumerate(q["options"]):

fg = "black"

text = option

if idx == correct:

text += " ✔ Correct"

fg = "green"

if user == idx and user != correct:

text += " ✖ Your Answer"

fg = "red"

tk.Label(frame, text=text, fg=fg).pack(anchor="w")

if user == correct:

self.score += 1

tk.Label(scroll_frame, text=f"Final Score: {self.score}/{len(self.quiz)}",

font=("Arial", 13, "bold")).pack(pady=15)
if self.score >= 4:

messagebox.showinfo("Result", "Excellent performance!")

else:

messagebox.showinfo("Result", "Good try! Keep practicing")

self.save_user_score()

btn_frame = tk.Frame(scroll_frame)

btn_frame.pack(pady=20)

tk.Button(btn_frame, text=" Restart Quiz", width=15,

command=self.start_quiz).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text=" Exit to Dashboard", width=18,

command=self.dashboard_screen).grid(row=0, column=1, padx=10)

def clear_screen(self):

for widget in self.root.winfo_children():

widget.destroy()

---------------- RUN ----------------

root = tk.Tk()

app = QuizApp(root)

root.mainloop()