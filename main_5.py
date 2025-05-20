import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import random

# --- Data Setup (10 Random Questions) ---
questions = [
    "Who won the men's singles title at the Australian Open 2024?",
    "What historic event was commemorated on its 80th anniversary in June 2024?",
    "At the end of September 2024, which country became the first major economy to shut down its last coal-fired power station?",
    "Which actor performed a stunt by jumping from the roof during the closing ceremony of the 2024 Paris Summer Games?",
    "Which Country won the Eurovision song contest held in Malmo, Sweden, in May 2024?",
    "In October 2024, who was announced as the world's wealthiest female singer with an estimated net worth of $1.6 billion?",
    "Which football team won the Championship League Final in June 2024?",
    "The spectacular 2024 Summer Games in Paris kicked off in July, but what disrupted the opening ceremony?",
    "In January 2024, Environmental protesters in Paris were arrested for trying to throw soup over which famous artwork?",
    "In August 2024, which British band announced a reunion tour of Britain and Ireland, 16 years after their acrimonious split?"
]

options = [
    ("A. Novak Djokovic", "B. Alexander Zverev", "C. Carlos Alcaraz", "D. Jannik Sinner"),
    ("A. Moon Landing", "B. D-Day (Normandy Invasion)", "C. Fall of the Berlin Wall", "D. End of World War I"),
    ("A. United Kingdom", "B. Germany", "C. Japan", "D. Switzerland"),
    ("A. Vin Diesel", "B. The Rock (Dwayne Johnson)", "C. Tom Cruise", "D. Ryan Reynolds"),
    ("A. Switzerland", "B. Croatia", "C. Turkey", "D. Australia"),
    ("A. Billie Eilish", "B. Katy Perry", "C. Miley Cyrus", "D. Taylor Swift"),
    ("A. Manchester City", "B. Bayern Munich", "C. Real Madrid", "D. Borussia Dortmund"),
    ("A. Some performers forgot their lines", "B. Flame was blown out", "C. Rain drenched the ceremony!", "D. Goats wandered on stage!"),
    ("A. The Persistence of Memory", "B. The Thinker", "C. The Mona Lisa", "D. Liberty Leading the People"),
    ("A. Blur", "B. Coldplay", "C. The Beatles", "D. Oasis")
]

answers = ["D", "B", "A", "C", "A", "D", "C", "C", "C", "D"]

# --- GUI Application ---
class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("2024 World Events Quiz")
        self.master.geometry("700x500")
        self.master.configure(bg="#2e2e2e")

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("TProgressbar", foreground='green', background='green')

        self.timer = 30
        self.timer_id = None
        self.q_index = 0
        self.score = 0
        self.user_answers = []

        self.question_label = tk.Label(master, text="", wraplength=650, font=('Arial', 14), fg="white", bg="#2e2e2e")
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(master, text="", variable=self.var, value=chr(65+i), font=('Arial', 12), fg="white",
                                 bg="#2e2e2e", selectcolor="#444444", activebackground="#2e2e2e", activeforeground="white")
            rb.pack(anchor='w', padx=30)
            self.radio_buttons.append(rb)

        self.progress = ttk.Progressbar(master, length=500, mode='determinate')
        self.progress.pack(pady=10)

        self.timer_label = tk.Label(master, text=f"Time left: {self.timer}s", font=('Arial', 12), fg="white", bg="#2e2e2e")
        self.timer_label.pack()

        self.submit_btn = tk.Button(master, text="Submit", command=self.submit_answer, font=('Arial', 12), bg="#444444",
                                     fg="white", activebackground="#666666")
        self.submit_btn.pack(pady=20)

        self.load_question()

    def load_question(self):
        if self.q_index < len(questions):
            self.var.set("")
            self.question_label.config(text=f"Q{self.q_index+1}: {questions[self.q_index]}")
            for i, option in enumerate(options[self.q_index]):
                self.radio_buttons[i].config(text=option)
            self.progress['value'] = (self.q_index / len(questions)) * 100
            self.reset_timer()
        else:
            self.show_results()

    def submit_answer(self):
        selected = self.var.get()
        if not selected:
            messagebox.showwarning("No selection", "Please choose an answer.")
            return

        self.master.after_cancel(self.timer_id)
        self.user_answers.append(selected)

        if selected == answers[self.q_index]:
            self.score += 1

        self.q_index += 1
        self.load_question()

    def reset_timer(self):
        self.timer = 30
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.timer}s")
        if self.timer > 0:
            self.timer -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.user_answers.append("No Answer")
            self.q_index += 1
            self.load_question()

    def show_results(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        percent = int((self.score / len(questions)) * 100)
        result_text = f"Quiz Complete!\n\nScore: {self.score}/{len(questions)}\nPercentage: {percent}%"
        tk.Label(self.master, text=result_text, font=('Arial', 16), fg="white", bg="#2e2e2e").pack(pady=20)

        self.save_results(percent)

        tk.Button(self.master, text="Restart Quiz", command=self.restart_quiz, font=('Arial', 12), bg="#444444", fg="white").pack(pady=10)
        tk.Button(self.master, text="Exit", command=self.master.quit, font=('Arial', 12), bg="#444444", fg="white").pack()

    def save_results(self, percent):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("quiz_results.txt", "a") as f:
            f.write(f"\n--- Quiz Attempt on {now} ---\n")
            f.write(f"Score: {self.score}/{len(questions)} ({percent}%)\n")
            for i, q in enumerate(questions):
                f.write(f"Q{i+1}: {q}\nYour Answer: {self.user_answers[i]}, Correct Answer: {answers[i]}\n")
            f.write("-"*40 + "\n")

    def restart_quiz(self):
        self.q_index = 0
        self.score = 0
        self.user_answers = []
        self.load_question()

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
