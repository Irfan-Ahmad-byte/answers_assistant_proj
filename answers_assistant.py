'''
This is a GUI application that acts as answer assistant. 
It has two frames, to saving the question and the related
answer other to get answer of a question. It will not 
return an answer if it was not saved fot the respective question.

Developer: Irfan Ahmad
github: https://github.com/irfan-ahmad-byte/
fiverr: https://www.fiverr.com/irfanmlka
twitter: https://twitter.com/IrfanAhmad1707
date: July 3, 2022
'''


import tkinter
import tkinter.messagebox
import customtkinter

from tkinter import filedialog as fd
from tkinter import *
import pyttsx3
import datetime
import speech_recognition as sr #pip install speechRecognition

import database

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Alice, Sir. Please tell me how may I help you")       

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...") 
        #speak('Say that Again Please...') 
        return "None"
    return query

class App(customtkinter.CTk):

    WIDTH = 1020
    HEIGHT = 620

    def __init__(self):
        super().__init__()

        self.title("Questoins and Answers")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=300,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Questions and Answers feeder",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.entry_quest = customtkinter.CTkEntry(master=self.frame_left,
                                            width=120,
                                            placeholder_text="Enter question")
        self.entry_quest.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.entry_ans = customtkinter.CTkEntry(master=self.frame_left,
                                            width=120,
                                            placeholder_text="Enter answer")
        self.entry_ans.grid(row=4, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_save = customtkinter.CTkButton(master=self.frame_left,
                                                text="save", command=self.save_questions)
        self.button_save.grid(row=5, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Get your answers" ,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(row=0, column=0, pady=10, padx=10)
        
        self.label_info_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Your answer appears here" ,
                                                   height=100,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_2.grid(row=1, column=0, columnspan=1, pady=10, padx=4)


        # ============ frame_right ============

        self.entry_get_ans = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Enter question to get answer")
        self.entry_get_ans.grid(row=4, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_get = customtkinter.CTkButton(master=self.frame_right,
                                                text="get answer",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.get_ans)
        self.button_get.grid(row=5, column=0, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Dark")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def save_questions(self):
        '''
        function to save question and answer in the database
        '''

        # try:
        #     question = takeCommand()
        question = self.entry_quest.get()
        answer = self.entry_ans.get()
        speak(f'You saved an answer for the question')
        speak(question)
        conn = database.dbconnect('database/questions.db')
        save = database.save_ans(conn, (question, answer))
        conn.close()

        self.label_1.set_text(save)

    def get_ans(self):
        '''
        function to get question's answer from the database
        '''

        question = self.entry_get_ans.get()
        question = question.lower()
        conn = database.dbconnect('database/questions.db')
        ans = database.get_ans(conn, question)
        conn.close()

        speak('Sir, Here is your answer.')
        speak(ans)

        self.label_info_2.set_text(ans)


    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    wishMe()
    app.mainloop()

'''===================================================================='''