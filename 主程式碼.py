import tkinter as tk
import tkinter.font as tkFont
import pickle
from tkinter import messagebox  
from PIL import Image, ImageTk
import random
import csv
import pickle
import time
import datetime
import pygame
#import pkg_resources.py2_warn

# 決定要不要切換使用者
switch_usr = [1]   # 1代表要切換，起始葉面就會是login_page

present_ID_stored = ['']   # 用來暫存登入玩家的資料 


again = True
while again is True:
    pygame.mixer.init()                     # 初始化mixer，為每段程式必須輸入的code
    pygame.mixer.music.load('主要背景.mp3')   # 開啟音樂檔案
    pygame.mixer.music.play(-1)             # 音樂無限播放
    challenge_completed = []      # 已經完成的題目，最多為9個元素
    challenge_selected = []       # 每次只能選擇一個題目，以最後點擊的問題來當做須執行的題目  # 要重製
    challenge_successful = []     # 玩家成功的題目  # 範例: 'WBL3'
    game_payoff_rate = ['\n獲勝 x1\n失敗 x1', '\n獲勝 x2\n失敗 x2', '\n獲勝 x3\n失敗 x3', '\n獲勝 x1\n失敗 x2', '\n獲勝 x1\n失敗 x3', '\n獲勝 x3\n失敗 x1', '\n獲勝 x2\n失敗 x1', '\n獲勝 x1\n失敗 x0']
    payoff_rate_num = [(1, 1), (2, 2), (3, 3), (1, 2), (1, 3), (3, 1), (2, 1), (1, 0), (10, 10)]

    random.shuffle(game_payoff_rate)     # 隨機排列
    bingo_list = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]] # bingo的數字組合
    bonus_dict = {"0":0, "1":1000, "2":4000, "3":9000, "4":9000, "5":9000, "6":9000, "7":9000, "8":9000, "9":9000} # bonus金額

    question_my_selected_dict = {'\n獲勝 x1\n失敗 x1':"WEL1", '\n獲勝 x2\n失敗 x2':"WEL2", '\n獲勝 x3\n失敗 x3':"WEL3", '\n獲勝 x1\n失敗 x2':"WSL2", '\n獲勝 x1\n失敗 x3':"WSL3", '\n獲勝 x3\n失敗 x1':"WBL3", '\n獲勝 x2\n失敗 x1':"WBL2", '\n獲勝 x1\n失敗 x0':"WBL1"}

    def change_question(question_level):

        # level_list.append(question_level)
        # if question_level not in level_times.keys():
        #     level_times[question_level] = 0
        # else:
        #     level_times[question_level] += 1
        # questions_list = list(level_Qs['W>L (*3)'])
        answer_option = str()
        questions_list = list(level_Qs[question_level])
        questions_WL3 = questions_list    # 叫出W>L (*3)這個level裡的所有questions (為一個tuple)
        '''處理題目random'''
        random.shuffle(questions_WL3)  # 隨機排序後，照排序後的順序一個一個選
        # pick_question = level_times[question_level]
        first_Q = questions_WL3[0]  # 選第一個

        # 叫出這題的各個attribute
        # print("原始題目")
        # print(first_Q.statement)
        # print(first_Q.option_A)
        # print(first_Q.option_B)    
        # print(first_Q.option_C)
        # print(first_Q.option_D)
        # print(first_Q.ans)
        # print(first_Q.ans_time)

        question_text = first_Q.statement
        option1 = first_Q.option_A
        option2 = first_Q.option_B   
        option3 = first_Q.option_C
        option4 = first_Q.option_D
        answer = first_Q.ans
        # 在random選項排列前，先存下答案
        if answer == 'A':
            answer_option = option1
        elif answer == 'B':
            answer_option = option2
        elif answer == 'C':
            answer_option = option3
        elif answer == 'D':
            answer_option = option4

        ans_time = first_Q.ans_time

        '''處理選項random'''
        chioce_items = [option1, option2, option3, option4]
        random.shuffle(chioce_items)
        # print(chioce_items)

        option_A = chioce_items[0]
        option_B = chioce_items[1]
        option_C = chioce_items[2]
        option_D = chioce_items[3]

        for i in range(4):  # 換算答案的選項代碼
            if chioce_items[i] == answer_option:
                answer = chr(65 + i)

        # self.renew_question(self.question_text)
        
        Quesion_dict[question_level] = Question(question_text, option_A, option_B, option_C, option_D, answer, ans_time)

        # return(self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time)

    class Question:
        def __init__(self, statement , option_A, option_B, option_C, option_D, ans, ans_time):
            self.statement = statement
            self.option_A = option_A
            self.option_B = option_B
            self.option_C = option_C
            self.option_D = option_D
            self.ans = ans
            self.ans_time = ans_time

    with open('question_data.pickle', 'rb') as file:
        level_Qs = pickle.load(file)

    Quesion_dict = dict()  # 要放九個問題，之後用這個查詢難度去叫出問題頁面
    question_level_list = ["W>L (*3)", "W>L (*2)", "W>L (*1)", "W=L (*3)", "W=L (*2)", "W=L (*1)", "W<L (*3)", "W<L (*2)", "W<L (*1)"]
    for level in question_level_list:
        change_question(level)
    # enter = input("輸入難度")
    # print(Quesion_dict[enter])

    initial_parameters = [0, 10000, ' ', 0, 0, False]      # 連線數量、初始資金、目前切換的格子(給計時器用的)、賭金、選取第幾格
    RRR = [False]  # 初始還是題目、有做還是沒做(呼叫initial_parameters[2])
    trigger_list = []                                     # 啟動鎖定按鈕的條件

    present_ID = ['']   
    login_time = ['']



    # 在玩一次的參數
    play = [0]    # 0代表不玩了，1代表再玩一次 

    #============================== 控制切換頁面的主程式 ==============================#
    class main_program(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            #===============創建一個視窗，用來盛裝所有page (命名為container)===================#
            container = tk.Frame(self)
            container.master.title("百萬大學堂")
            container.master.geometry('1000x563')
            container.master.resizable(width=0, height=0)   # 固定視窗大小(使用者不可調整)
            container.pack()


            self.frames = {}   # 宣告一個set(其實就是空的dictionary)
            for F in [login_page, intro_page,fund_page, Page_4, break_page, final_page, monster_page, WBL3_page, WBL2_page, WBL1_page, WSL2_page, WSL3_page, WEL3_page, WEL2_page, WEL1_page]: 
                page_name = F.__name__  # login_page.__name__ 就會回傳 "login_page"
                frame = F(parent=container, controller=self) 
                self.frames[page_name] = frame

                # 將每一個page都放到container理，並且完全重疊在一起
                # 只有最上面page的會顯現出來
                frame.grid(self.master, row=0, column=0)   # sticky="nsew" 表示完全填滿

            # # 如果把下面這行拿掉，一開始顯現的就會是intro_page，因為迴圈最後面是停在intro_page
            if switch_usr[0] == 1:
                self.show_frame("login_page")
            else:
                present_ID[0] = present_ID_stored[0]
                login_time[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                self.show_frame("fund_page")

        #==============把指定的page放到最上層=================#
        def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()
            RRR[0] = True
            self.frames[Page_4.__name__].amount_have_box(initial_parameters[1])
            self.frames[Page_4.__name__].line_connected_box(initial_parameters[0])
            self.frames[Page_4.__name__].draw_box_in_different_color(initial_parameters[5])
            self.frames[Page_4.__name__].amount_entry_box()

            if page_name == 'break_page':
                self.frames[break_page.__name__].music()

            if page_name == 'final_page':
                self.frames[final_page.__name__].music()
                self.frames[final_page.__name__].show_rank(login_time[0], present_ID[0], initial_parameters[1])


            if initial_parameters[2] == 'monster':
                self.frames[monster_page.__name__].countdown(Quesion_dict["W=L (*3)"].ans_time, initial_parameters[2])
            if initial_parameters[2] == 'WBL3':
                self.frames[WBL3_page.__name__].countdown(Quesion_dict["W>L (*3)"].ans_time, initial_parameters[2])
            if initial_parameters[2] == 'WBL2':
                self.frames[WBL2_page.__name__].countdown(Quesion_dict["W>L (*2)"].ans_time, initial_parameters[2])
            if initial_parameters[2] == 'WBL1':
                self.frames[WBL1_page.__name__].countdown(Quesion_dict["W>L (*1)"].ans_time, initial_parameters[2])
            if initial_parameters[2] == 'WSL3':
                self.frames[WSL3_page.__name__].countdown(Quesion_dict["W<L (*3)"].ans_time, initial_parameters[2])
            if initial_parameters[2] == 'WSL2':
                self.frames[WSL2_page.__name__].countdown(Quesion_dict["W<L (*2)"].ans_time, initial_parameters[2])
            if initial_parameters[2] == 'WEL3':
                self.frames[WEL3_page.__name__].countdown(Quesion_dict["W=L (*3)"].ans_time, initial_parameters[2])
            if initial_parameters[2] == 'WEL2':
                self.frames[WEL2_page.__name__].countdown(Quesion_dict["W=L (*2)"].ans_time, initial_parameters[2])
            if initial_parameters[2] == 'WEL1':
                self.frames[WEL1_page.__name__].countdown(Quesion_dict["W=L (*1)"].ans_time, initial_parameters[2])
        
        def change_player(self):
            play[0] = 1
            switch_usr[0] = 1
            self.destroy()
        
        def play_again(self):
            play[0] = 1
            switch_usr[0] = 0
            self.destroy()
        
        def page_detroy(self):
            self.destroy()

    class login_page(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            #=========================插入背景========================#
            self.BG_img = ImageTk.PhotoImage(Image.open("rsz_login_page_bg.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)

            #=========================設定字形========================#
            f1 = tkFont.Font(size = 12, family = "Courier New")
            f2 = tkFont.Font(size = 16, family = "Courier New")

            #=========================創建Entry========================#
            self.ID_input = tk.StringVar()
            self.pswd_input = tk.StringVar()

            self.ID_entry = tk.Entry(self.BG_label, textvariable = self.ID_input, width = 15, font = f2)
            self.ID_entry.place(relx=0.4, rely=0.56)

            self.pswd_entry = tk.Entry(self.BG_label, textvariable = self.pswd_input, width = 15, font = f2, show = '*')
            self.pswd_entry.place(relx=0.4, rely=0.64)

            #=========================創建Button========================#
            self.start_button = tk.Button(self.BG_label, text = '進入遊戲', font = f1, width = 8, relief = 'flat', bg = 'white', command = self.usr_login)
            self.start_button.place(relx=0.367, rely = 0.717)

            self.signup_button = tk.Button(self.BG_label, text = '先去註冊', font = f1, width = 8, relief = 'flat', bg = 'white', command = self.usr_sign_up)
            self.signup_button.place(relx=0.534, rely = 0.717)


        def usr_login(self):
            self.user_ID = self.ID_entry.get()
            self.user_pswd = self.pswd_input.get()

            try:   # 開啟usrs_info.pickle的資料檔案 (裡面存著user_name: pswd的dictionary)
                with open('usrs_info.pickle', 'rb') as usr_file:
                    usrs_info = pickle.load(usr_file)
            except FileNotFoundError:    # 如果這個檔案不在，就創建一個，並先增加第一筆使用者帳密(admin)
                with open('usrs_info.pickle', 'wb') as usr_file:
                    usrs_info = {'admin': 'admin'}
                    pickle.dump(usrs_info, usr_file)

            if self.user_ID == str() or self.user_pswd == str():
                tk.messagebox.showerror('不行喔!', "帳號或密碼不能空白!")
            elif self.user_ID in usrs_info:
                if self.user_pswd == usrs_info[self.user_ID]:
                    
                    # 紀錄目前玩家及登入時間
                    present_ID[0] = self.user_ID
                    present_ID_stored[0] = self.user_ID

                    login_time[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # print(present_ID[0])
                    # print(login_time[0])

                    tk.messagebox.showinfo(title='Welcome', message='歡迎! ' + self.user_ID)
                    self.controller.show_frame("intro_page")    # 進入遊戲介紹葉面
                else:
                    tk.messagebox.showerror(message='密碼錯誤，再試一次!')
            else:
                is_sign_up = tk.messagebox.askyesno('Welcome','您尚未註冊，是否要註冊呢?')
                                # 按下"是" → 回傳True，按下否 → 回傳False
                if is_sign_up is True:
                    self.usr_sign_up()

        def usr_sign_up(self):

            #=======================創建Sign up window====================# 
            self.window_sign_up = tk.Toplevel(self)
            self.window_sign_up.geometry('350x200')
            self.window_sign_up.title('歡迎註冊')

            # ID輸入欄位
            self.new_ID_input = tk.StringVar()
            tk.Label(self.window_sign_up, text='User name: ').place(x = 10, y = 10)
            entry_new_name = tk.Entry(self.window_sign_up, textvariable = self.new_ID_input)
            entry_new_name.place(x = 150, y = 10)

            # 密碼輸入欄位
            self.new_pswd_input = tk.StringVar()
            tk.Label(self.window_sign_up, text = 'Password: ').place(x=10, y=50)
            entry_usr_pwd = tk.Entry(self.window_sign_up, textvariable = self.new_pswd_input, show = '*')
            entry_usr_pwd.place(x = 150, y = 50)

            # # 確認密碼欄位
            self.new_pwd_confirm_input = tk.StringVar()
            tk.Label(self.window_sign_up, text = 'Confirm password: ').place(x=10, y= 90)
            entry_usr_pwd_confirm = tk.Entry(self.window_sign_up, textvariable = self.new_pwd_confirm_input, show = '*')
            entry_usr_pwd_confirm.place(x=150, y=90)

            self.btn_comfirm_sign_up = tk.Button(self.window_sign_up, text = "註冊", command = self.process_signup_info)
            self.btn_comfirm_sign_up.place(x=150, y=130)
        
        def process_signup_info(self):
            self.new_ID = self.new_ID_input.get()
            self.new_pswd = self.new_pswd_input.get()
            self.new_pwd_confirm = self.new_pwd_confirm_input.get()

            try:   # 開啟usrs_info.pickle的資料檔案 (裡面存著user_name: pswd的dictionary)
                with open('usrs_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
            except FileNotFoundError:    # 如果這個檔案不在，就創建一個，並先增加第一筆使用者帳密(admin)
                with open('usrs_info.pickle', 'wb') as usr_file:
                    usrs_info = {'admin': 'admin'}
                    pickle.dump(usrs_info, usr_file)
            
                with open('usrs_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
            
            if self.new_ID == str() or self.new_pswd == str():
                self.window_sign_up.destroy()
                tk.messagebox.showerror('不行喔!', "帳號或密碼不能空白")
                self.usr_sign_up()        
            elif self.new_pswd != self.new_pwd_confirm:
                self.window_sign_up.destroy()
                tk.messagebox.showerror('糟糕!', "兩次密碼輸入不一樣喔!")
                self.usr_sign_up()
            elif self.new_ID in exist_usr_info:
                self.window_sign_up.destroy()
                tk.messagebox.showerror('糟糕!', '這個ID已經有人使用了!')
                self.usr_sign_up()
            else:
                exist_usr_info[self.new_ID] = self.new_pswd
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo('Welcome', '歡迎 ' + self.new_ID+" !" + ' 恭喜你註冊成功 !')

                # 紀錄目前玩家及登入時間
                present_ID[0] = self.new_ID
                present_ID_stored[0] = self.new_ID

                login_time[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                self.window_sign_up.destroy()
                self.controller.show_frame("intro_page")   # 進入下一個頁面

    class intro_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            #=========================插入背景========================#
            self.BG_img = ImageTk.PhotoImage(Image.open("rule.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)

            #=========================設定字形========================#
            f1 = tkFont.Font(size = 16, family = "Courier New")

            #=========================創建Button======================#
            self.start_button = tk.Button(self.BG_label, text = 'Next', font = f1, width = 9, relief = 'flat', bg = 'white', command=lambda: controller.show_frame("fund_page"))
            self.start_button.place(relx=0.435, rely=0.911)

    class fund_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            #=========================插入背景========================#
            self.BG_img = ImageTk.PhotoImage(Image.open("第一筆資金.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)

            #=========================設定字形========================#
            f1 = tkFont.Font(size = 14, family = "Courier New")

            #=========================創建Button======================#
            self.start_button = tk.Button(self.BG_label, text = 'Get Started', font = f1, width = 10, relief = 'flat', bg = 'white', command=lambda: controller.show_frame("Page_4"))
            self.start_button.place(relx=0.44, rely=0.91)

    class Page_4(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #=========================插入背景========================#
            self.BG_img = ImageTk.PhotoImage(Image.open("0004.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)
            # ====================基本參數===================#
            self.myfont = tkFont.Font(size=20, family="Courier New")  # 統一字型
            self.x1, self.x2, self.x3 = 0.3, 0.44, 0.58  # 九宮格位置
            self.y1, self.y2, self.y3 = 0.2, 0.4, 0.6    # 九宮格位置
            self.nine_buttons()           # 九個buttons的格式與位置
            self.amount_have_box()        # 擁有金額的格式與位置
            self.amount_entry_box()       # 輸入賭金的格式與位置
            self.line_connected_box()     # 連線數量的格子
            self.confirm_button_page_4()  # 確認按鈕的格式與位置

        def nine_buttons(self):
            self.button_1 = tk.Button(self.BG_label, text = game_payoff_rate[0], width = 8, height = 3, command = self.activate_button_1, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_1.place(relx = self.x1, rely = self.y1)

            self.button_2 = tk.Button(self.BG_label, text = game_payoff_rate[1], width = 8, height = 3, command = self.activate_button_2, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_2.place(relx = self.x2, rely = self.y1)

            self.button_3 = tk.Button(self.BG_label, text = game_payoff_rate[2], width = 8, height = 3, command = self.activate_button_3, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_3.place(relx = self.x3, rely = self.y1)

            self.button_4 = tk.Button(self.BG_label, text = game_payoff_rate[3], width = 8, height = 3, command = self.activate_button_4, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_4.place(relx = self.x1, rely = self.y2)

            self.button_5 = tk.Button(self.BG_label, text = '大魔王\n獲勝 x10\n失敗 x10', width = 8, height = 3, command = self.activate_button_5, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_5.place(relx = self.x2, rely = self.y2)
            
            self.button_6 = tk.Button(self.BG_label, text = game_payoff_rate[4], width = 8, height = 3, command = self.activate_button_6, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_6.place(relx = self.x3, rely = self.y2)

            self.button_7 = tk.Button(self.BG_label, text = game_payoff_rate[5], width = 8, height = 3, command = self.activate_button_7, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_7.place(relx = self.x1, rely = self.y3)

            self.button_8 = tk.Button(self.BG_label, text = game_payoff_rate[6], width = 8, height = 3, command = self.activate_button_8, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_8.place(relx = self.x2, rely = self.y3)

            self.button_9 = tk.Button(self.BG_label, text = game_payoff_rate[7], width = 8, height = 3, command = self.activate_button_9, bd = 4, activebackground = '#AFEEEE', bg = '#FFEBCD', font = self.myfont)
            self.button_9.place(relx = self.x3, rely = self.y3)

        # 選擇哪個按鈕
        def activate_button_1(self):
            initial_parameters[4] = 1
            if len(challenge_selected) == 0:
                self.button_1.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_1)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_1:
                self.button_1.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_1)
        
        def activate_button_2(self):
            initial_parameters[4] = 2
            if len(challenge_selected) == 0:
                self.button_2.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_2)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_2:
                self.button_2.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_2)

        def activate_button_3(self):
            initial_parameters[4] = 3
            if len(challenge_selected) == 0:
                self.button_3.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_3)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_3:
                self.button_3.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_3)

        def activate_button_4(self):
            initial_parameters[4] = 4
            if len(challenge_selected) == 0:
                self.button_4.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_4)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_4:
                self.button_4.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_4)

        def activate_button_5(self):
            initial_parameters[4] = 5
            if len(challenge_selected) == 0:
                self.button_5.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_5)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_5:
                self.button_5.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_5)

        def activate_button_6(self):
            initial_parameters[4] = 6
            if len(challenge_selected) == 0:
                self.button_6.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_6)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_6:
                self.button_6.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_6)

        def activate_button_7(self):
            initial_parameters[4] = 7
            if len(challenge_selected) == 0:
                self.button_7.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_7)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_7:
                self.button_7.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_7)

        def activate_button_8(self):
            initial_parameters[4] = 8
            if len(challenge_selected) == 0:
                self.button_8.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_8)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_8:
                self.button_8.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_8)

        def activate_button_9(self):
            initial_parameters[4] = 9
            if len(challenge_selected) == 0:
                self.button_9.configure(bg = '#AFEEEE')
                challenge_selected.append(self.button_9)
            elif len(challenge_selected) != 0 and challenge_selected[0] != self.button_9:
                self.button_9.configure(bg = '#AFEEEE')
                challenge_selected[0].configure(bg = '#FFEBCD')
                challenge_selected.pop()
                challenge_selected.append(self.button_9)

        def Wrong_disabled_button(self):
            challenge_selected[0].configure(state = 'disabled', bg = '#F08080')
            challenge_selected.clear()
        
        def Correct_disabled_button(self):
            challenge_selected[0].configure(state = 'disabled', bg = '#66CDAA')
            challenge_selected.clear()
                
        def draw_box_in_different_color(self, initial_parameters_bool):
            if len(challenge_completed)!= 0 and len(trigger_list) != 0:
                if initial_parameters_bool == True:
                    self.Correct_disabled_button()
                elif initial_parameters_bool == False:
                    self.Wrong_disabled_button()
                trigger_list.clear()
        # 現有$$
        def amount_have_box(self, moneymoney = 10000):
            self.amount_have = tk.Label(self.BG_label, text = str(moneymoney), width = 10, font = self.myfont)
            self.amount_have.place(relx=0.758, rely=0.27)
        ######這邊要加入判定$$增加或減少  ##跟換頁有關#################

        # 連線數量
        def line_connected_box(self, lineline = 0):
            self.line_connected = tk.Label(self.BG_label, text = str(lineline), width = 10, font = self.myfont)
            self.line_connected.place(relx=0.758, rely=0.44)

        # 輸入賭金鈕
        def amount_entry_box(self):
            self.amount_input = tk.StringVar()
            self.amount_entry = tk.Entry(self.BG_label, textvariable = self.amount_input, width = 8, font = self.myfont)
            self.amount_entry.place(relx=0.758, rely=0.65)

        # 確認鈕
        def confirm_button_page_4(self):
            self.confirm = tk.Button(self.BG_label, text = "確認", bd = 2, command =self.Click_Confirm, font = self.myfont, activebackground = 'cyan')    
            self.confirm.place(relx = 0.758, rely = 0.77)
            
        def Click_Confirm(self):
            if len(challenge_selected) == 0:  # 沒有選擇題目
                tk.messagebox.showerror('黑人問號','不會選題目嗎?')
            #####增加防呆機制，輸入不屬於數字的字元

            elif self.amount_entry.get().isdigit() == False:
                tk.messagebox.showerror('小提示','請輸入確切數字') # 輸入的字串必須為一整數

            else:
                if int(self.amount_entry.get()) * 100 > initial_parameters[1]:   # 擁有金額不夠支付賭金
                    tk.messagebox.showerror('要不要考慮小額貸款','沒錢仔還想賭博啊?')

                else: # 進入下一頁的題目
                    initial_parameters[3] = int(self.amount_entry.get()) * 100  # 存取賭金
                    self.amount_input = ''   # 清空輸入值，方便之後再次輸入
                    temp = initial_parameters[4]
                    challenge_completed.append(initial_parameters[4])
                    if temp == 5:
                        initial_parameters[2] = 'monster'
                    elif temp < 5:
                        initial_parameters[2] = question_my_selected_dict[game_payoff_rate[temp - 1]]
                    elif temp > 5:
                        initial_parameters[2] = question_my_selected_dict[game_payoff_rate[temp - 2]]
                    self.controller.show_frame(initial_parameters[2] + "_page")

    class monster_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W<L (*1)"
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型
            self.time_upup = ''

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0
        
        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'monster' or ' ':   # 呼叫或是初始
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'monster':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)
                self.time_upup = time_up

                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')
                    else:
                        self.controller.show_frame('Page_4')

        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[8][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[8][0] + now_bingo
            elif self.time_upup  == 'monster':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[8][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[8][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[8][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[8][1]

    class WBL3_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W>L (*3)"
            self.time_upup = ''
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0
        
        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'WBL3' or ' ':
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        # self.submit_chioce(self.var.get(), start_or_not)
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'WBL3':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)
                self.time_upup = time_up

                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')
                    else:
                        self.controller.show_frame('Page_4')

        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now > 3:
                money = bonus_dict[str(3)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return max(money, 0)
            elif line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[5][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[5][0] + now_bingo
            elif self.time_upup  == 'WBL3':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[5][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[5][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[5][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[5][1]

    class WBL2_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W>L (*2)"
            self.time_upup = ''
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0
        
        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'WBL2' or ' ':
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        # self.submit_chioce(self.var.get(), start_or_not)
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                        start_or_not = False
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        # print("現在到數到幾秒", "%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'WBL2':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)


                self.time_upup = time_up
                # print("*****correct_or_not", correct_or_not)
                # print("*****challenge_completed", challenge_completed)
                # 印出來長這樣  *****correct_or_not False
                # 印出來長這樣  *****challenge_completed [8, 8, 9, 9, 5, 5, 6, 7] 發現是pag4那邊重複append>>已改
                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')

                    else:
                        self.controller.show_frame('Page_4')

        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now > 3:
                money = bonus_dict[str(3)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return max(money, 0)
            elif line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[6][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[6][0] + now_bingo
            elif self.time_upup  == 'WBL2':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[6][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[6][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[6][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[6][1]

    class WBL1_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W>L (*1)"
            self.time_upup = ''
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0
        
        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'WBL1' or ' ':
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        # self.submit_chioce(self.var.get(), start_or_not)
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'WBL1':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)
                self.time_upup = time_up

                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')
                    else:
                        self.controller.show_frame('Page_4')

        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now > 3:
                money = bonus_dict[str(3)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return max(money, 0)
            elif line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[7][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[7][0] + now_bingo
            elif self.time_upup  == 'WBL1':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[7][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[7][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[7][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[7][1]

    class WSL2_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W<L (*2)"
            self.time_upup = ''
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0
        
        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'WSL2' or ' ':
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        # self.submit_chioce(self.var.get(), start_or_not)
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'WSL2':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)
                self.time_upup = time_up

                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')
                    else:
                        self.controller.show_frame('Page_4')

        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now > 3:
                money = bonus_dict[str(3)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return max(money, 0)
            elif line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[3][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[3][0] + now_bingo
            elif self.time_upup  == 'WSL2':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[3][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[3][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[3][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[3][1]

    class WSL3_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W<L (*3)"
            self.time_upup = ''
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0

        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'WSL3' or ' ':
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        # self.submit_chioce(self.var.get(), start_or_not)
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        # # 魔王關的倒數計時
        # def countdown(self, remaining = None, start_or_not = ' '):
        #     if start_or_not == 'monster' or ' ':   # 呼叫或是初始
        #         if remaining is not None:
        #             self.remaining = remaining
        #         # 變紅字
        #         if int(self.remaining) <= 5:
        #             self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
        #         if int(self.remaining) <= 0:
        #             self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
        #             self.submit_chioce(self.var.get(), initial_parameters[2])
        #         else:
        #             self.label.configure(text="%d" % int(self.remaining))
        #             self.remaining = int(self.remaining) - 1
        #             self.after(1000, self.countdown)


        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'WSL3':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)
                self.time_upup = time_up

                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')
                    else:
                        self.controller.show_frame('Page_4')

        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now > 3:
                money = bonus_dict[str(3)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return max(money, 0)
            elif line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[4][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[4][0] + now_bingo
            elif self.time_upup  == 'WSL3':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[4][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[4][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[4][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[4][1]

    class WEL3_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W=L (*3)"
            self.time_upup = ''
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0

        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'WEL3' or ' ':
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        # self.submit_chioce(self.var.get(), start_or_not)
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'WEL3':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)
                self.time_upup = time_up

                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')
                    else:
                        self.controller.show_frame('Page_4')

        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now > 3:
                money = bonus_dict[str(3)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return max(money, 0)
            elif line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[2][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[2][0] + now_bingo
            elif self.time_upup  == 'WEL3':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[2][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[2][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[2][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[2][1]

    class WEL2_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W=L (*2)"
            self.time_upup = ''
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0

        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'WEL2' or ' ':
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        # self.submit_chioce(self.var.get(), start_or_not)
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'WEL2':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)
                self.time_upup = time_up

                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')
                    elif time_up  == 'WEL2':
                        self.controller.show_frame('Page_4')
                    else:
                        self.controller.show_frame('Page_4')
        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now > 3:
                money = bonus_dict[str(3)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return max(money, 0)
            elif line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[1][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[1][0] + now_bingo
            elif self.time_upup  == 'WEL2':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[1][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[1][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[1][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[1][1]

    class WEL1_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            self.question_level = "W=L (*1)"
            self.time_upup = ''
            # (self.question_text, self.optionA, self.optionB, self.optionC, self.optionD, self.answer, self.ans_time) = self.change_question(question_level)
            #====================基本參數===================#
            self.myfont = tkFont.Font(size=32, family="Courier New")  # 統一字型

            #==============設定這個頁面要由哪些函數來控制===============# 
            self.BG_img = ImageTk.PhotoImage(Image.open("題目畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)


            # l = tk.Label(window, text='empty', font = ('Arial', 12), width = 20, height = 2)
            # global l
            self.l = tk.Label(self.BG_label, text='請選擇下方選項', width = 15, height = 1, bg = 'white', fg = '#4097AA')  # 顯示選擇的答案區域
            # label.config(bg='systemTransparent')
            # l.pack()
            self.l.place(x=690, y=236)
            Q = Quesion_dict[self.question_level].statement
            if len(Q) <= 35:
                self.question = tk.Label(self.BG_label, 
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            else:
                self.question = tk.Label(self.BG_label,
                        highlightthickness=0, borderwidth=0, padx=0, pady=0,  # 修改这里查看按钮边缘大小
                        compound='center', font=('Courier New', 17, 'bold'), bg = '#FAF1EA', fg = '#2E4058', # 修改字体和大小
                        text = Q, wraplength = 800, justify = 'left').place(relx=0.1, rely=0.3)  # x、y和左位置、上位置一致即可
            # self.renew_question(Quesion_dict[question_level].statement)

            # global var
            self.var = tk.StringVar()
            self.var.set(" ")

            """ 選項A """
            # r1 = tk.Radiobutton(self, variable = var, value = 'A', command = self.print_selection, bg = 'white')
            self.r1 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'A', command = self.print_selection, bg = 'white',
                            text = '選項 A', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10, activebackground = "yellow")
            self.r1.place(x=123, y=279)  # 位置
            self.text_r1 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_A), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r1.place(x=150, y=340)

            # 答對情況改顏色
            # r1.Radiobutton.configure(command = self.change_color(r1))
            # if (correct_or_not == True) and (choice == 'A'):
            #     r1.Radiobutton.configure(bg = 'green')
            #     text_r1.Label.configure(bg = 'green')

            
            """ 選項B """
            # r2 = tk.Radiobutton(self, variable = var, value = 'B', command = self.print_selection, bg = 'white')
            self.r2 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'B', command = self.print_selection, bg = 'white',
                            text = '選項 B', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r2.place(x=323, y=279)  # 位置
            self.text_r2 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_B), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r2.place(x=350, y=340)

            """ 選項C """
            # r3 = tk.Radiobutton(self, variable = var, value = 'C', command = self.print_selection, bg = 'white')
            self.r3 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'C', command = self.print_selection, bg = 'white',
                            text = '選項 C', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r3.place(x=523, y=279)  # 位置
            self.text_r3 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_C), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r3.place(x=550, y=340)

            """ 選項D """
            # r4 = tk.Radiobutton(self, variable = var, value = 'D', command = self.print_selection, bg = 'white')
            self.r4 = tk.Radiobutton(self.BG_label, variable = self.var, value = 'D', command = self.print_selection, bg = 'white',
                            text = '選項 D', font = 'Courier 16 bold', width = 10, height = 6, fg = '#2E4058',
                            anchor = 'nw', padx = 10, pady = 10)
            self.r4.place(x=723, y=279)  # 位置
            self.text_r4 = tk.Label(self.BG_label, bg = 'white', text = (Quesion_dict[self.question_level].option_D), font = 'Courier 12', fg = '#2E4058',
                                height = 3, wraplength = 130, justify = 'left')
            self.text_r4.place(x=750, y=340)

            """ 確認鍵 """
            self.confirm = tk.Button(self.BG_label, text = '確定', width = 5, height = 1, command = lambda:self.submit_chioce(self.question_level, RRR[0]),
                                bg = 'white', relief = 'flat', activebackground = 'white', fg = '#4097AA')
            self.confirm.place(x=850, y=234, anchor="nw")


            """ 倒數計時 """
            self.label = tk.Label(self.BG_label, text="", width=10, font = 'Courier 12', height = 1,
                            justify = 'center', bg = 'white', fg = '#4097AA')
            self.label.place(x=445, y=506)
            self.remaining = 0

        # 倒數計時
        def countdown(self, remaining = None, start_or_not = ' '):
            if self.label.winfo_exists() == 1:
                if start_or_not == 'WEL1' or ' ':
                    if remaining is not None:
                        self.remaining = remaining
                    # 變紅字
                    if int(self.remaining) <= 5:
                        self.label.configure(fg = 'red', font=('Courier New', 12, 'bold'))
                    if int(self.remaining) <= -1:
                        self.label.configure(text=" Time's up!", fg = 'red', font=('Courier New', 12, 'bold'))
                        # self.submit_chioce(self.var.get(), start_or_not)
                        self.submit_chioce(self.var.get(), initial_parameters[2])
                    else:
                        self.label.configure(text="%d" % int(self.remaining))
                        self.remaining = int(self.remaining) - 1
                        self.after(1000, self.countdown)

        def submit_chioce(self, question_level_list, time_up):
            if RRR[0] is True:
                if time_up is True:
                    choice = self.var.get()
                    choice = choice.strip()
                    if choice != "":  # 按進確認鍵
                        correct_or_not = self.match_answer(choice, Quesion_dict[self.question_level].ans)
                        initial_parameters[2] = ''
                        del self.label
                elif time_up  == 'WEL1':
                    correct_or_not = False
                    trigger_list.append(1)
                    initial_parameters[2] = "未選擇題目"  # 為了不讓他再次呼叫同一頁面的計時器
                    pygame.mixer.music.stop()
                    pygame.mixer.init()
                    pygame.mixer.music.load('Fail.mp3')
                    pygame.mixer.music.play(0)
                    
                self.time_upup = time_up

                if correct_or_not is not None:
                    initial_parameters[1] = int(self.my_count(correct_or_not))
                    if initial_parameters[1] <= 0:
                        self.controller.show_frame('break_page')
                    elif len(challenge_completed) == 9:
                        self.controller.show_frame('final_page')
                    elif time_up  == 'WEL1':
                        self.controller.show_frame('Page_4')
                    else:
                        self.controller.show_frame('Page_4')
        def match_answer(self, choice, answer):
            if choice == answer:
                correct_or_not = True
                challenge_successful.append(initial_parameters[4])     # 玩家成功的題目
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Victory.mp3')
                pygame.mixer.music.play(0)
            else:
                correct_or_not = False
                initial_parameters[5] = correct_or_not
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('Fail.mp3')
                pygame.mixer.music.play(0)
            trigger_list.append(1)
            # challenge_completed.append(initial_parameters[4])
            return(correct_or_not)

        def print_selection(self):
            self.l.config(text = "您的選擇：" + self.var.get(), fg = '#4097AA')

        def check_bingo(self):
            line_now = 0
            for i in bingo_list:
                if (i[0] in challenge_successful) and (i[1] in challenge_successful) and (i[2] in challenge_successful):
                    line_now += 1
            if line_now > 3:
                money = bonus_dict[str(3)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return max(money, 0)
            elif line_now == 0:
                return (0)
            else:
                money = bonus_dict[str(line_now)] - bonus_dict[str(initial_parameters[0])]
                initial_parameters[0] = line_now
                return money

        def my_count(self, answer):   # 要傳入有沒有答對的bool
            now_bingo = self.check_bingo()
            if answer is True:
                tk.messagebox.showinfo('答對了','恭喜你！贏得' + str(initial_parameters[3] * payoff_rate_num[0][0]))
                if now_bingo != 0:
                    tk.messagebox.showinfo('恭喜你','獲得連線獎金' + str(now_bingo))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] + initial_parameters[3] * payoff_rate_num[0][0] + now_bingo
            elif self.time_upup  == 'WEL1':
                tk.messagebox.showinfo("Time's up!",'時間到囉!')
                tk.messagebox.showinfo('超過時間未答題','損失' + str(initial_parameters[3] * payoff_rate_num[0][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[0][1]
            else:
                tk.messagebox.showinfo('答錯了','損失' + str(initial_parameters[3] * payoff_rate_num[0][1]))
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load('主要背景.mp3')
                pygame.mixer.music.play(-1)
                return initial_parameters[1] - initial_parameters[3] * payoff_rate_num[0][1]

    class break_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            #=========================插入背景========================#
            self.BG_img = ImageTk.PhotoImage(Image.open("破產畫面.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)

            #=========================設定字形========================#
            f1 = tkFont.Font(size = 14, family = "Courier New")

            #=========================創建Button======================#
            self.play_again_button = tk.Button(self.BG_label, text = '再玩一次', font = f1, width = 9, relief = 'flat', bg = 'white', command=lambda: controller.play_again())
            self.play_again_button.place(relx=0.266, rely=0.698)

            self.change_player_button = tk.Button(self.BG_label, text = '換人玩玩看', font = f1, width = 9, relief = 'flat', bg = 'white', command=lambda: controller.change_player())
            self.change_player_button.place(relx=0.448, rely=0.698)

            self.exit_button = tk.Button(self.BG_label, text = '退出遊戲', font = f1, width = 9, relief = 'flat', bg = 'white', command=lambda: controller.page_detroy())
            self.exit_button.place(relx=0.629, rely=0.698)

        def music(self):
            pygame.mixer.music.stop()
            pygame.mixer.init()
            pygame.mixer.music.load('失敗音效.mp3')
            pygame.mixer.music.play(0)  

    class final_page(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)  
            self.controller = controller

            #=========================插入背景========================#
            self.BG_img = ImageTk.PhotoImage(Image.open("最終獎金.gif"))
            self.BG_label = tk.Label(self, image = self.BG_img)
            self.BG_label.pack(fill='both', expand=True)

            #=========================設定字形========================#
            f1 = tkFont.Font(size = 14, family = "Courier New")
            # f2 = tkFont.Font(size = 45, family = "Courier New")

            #=========================創建Button======================#
            self.play_again_button = tk.Button(self.BG_label, text = '再玩一次', font = f1, width = 9, relief = 'flat', bg = 'white', command=lambda: controller.play_again())
            self.play_again_button.place(relx=0.266, rely=0.885)

            self.change_player_button = tk.Button(self.BG_label, text = '換人玩玩看', font = f1, width = 9, relief = 'flat', bg = 'white', command=lambda: controller.change_player())
            self.change_player_button.place(relx=0.445, rely=0.885)

            self.exit_button = tk.Button(self.BG_label, text = '退出遊戲', font = f1, width = 9, relief = 'flat', bg = 'white', command=lambda: controller.page_detroy())
            self.exit_button.place(relx=0.628, rely=0.885)

            # #=========================顯示最後金額=====================#

            # self.final_money = tk.Label(self.BG_label, text = str(initial_parameters[1]), font = f2, bg = '#FAF1EA', height = 0, fg = '#2E4058')
            # self.final_money.place(relx=0.18, rely=0.34)

        #=========================排行榜===============================#
        def show_rank(self, login_time, present_ID, score):
            # f1 = tkFont.Font(size = 10, family = "Courier New")
            f2 = tkFont.Font(size = 45, family = "Courier New")

            # print('fuck')
            try:   # 開啟usrs_info.pickle的資料檔案 (裡面存著user_name: pswd的dictionary)
                with open('rank_info.pickle', 'rb') as rank_info_file:
                    rank_info = pickle.load(rank_info_file)
                    if login_time not in rank_info:
                        # print('1234')
                        rank_info[login_time] = (present_ID, score)   
                
                with open('rank_info.pickle', 'wb') as rank_info_file:
                    pickle.dump(rank_info, rank_info_file)
                    
                    # pickle.dump(rank_info, rank_info_file)
                    # print(list(rank_info.items()))
                
            except FileNotFoundError:    # 如果這個檔案不在，就創建一個，並增加第一筆資料
                with open('rank_info.pickle', 'wb') as rank_info_file:
                    print(login_time, present_ID, score)
                    rank_info = {login_time: (present_ID, score) }      # 登入時間: (ID, score)
                    pickle.dump(rank_info, rank_info_file)


            rank_info = list(rank_info.items())
            rank_info = sorted(rank_info, key = lambda elem: elem[1][1], reverse=True)   # 按分數由大排到小

            # print(rank_info)
            # 本次排行
            total_num = len(rank_info)
            present_rank = rank_info.index((login_time, (present_ID, score)))
            # print(str(present_rank+1)+' /'+ str(total_num))

            # # # # 本次排名
            self.present_rank = tk.Label(self.BG_label, text = str(present_rank+1)+'/'+ str(total_num), font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
            self.present_rank.place(relx=0.5, rely=0.76)
            self.present_id = tk.Label(self.BG_label, text = present_ID, font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
            self.present_id.place(relx=0.6, rely=0.76)
            self.present_money = tk.Label(self.BG_label, text = score, font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
            self.present_money.place(relx=0.78, rely=0.76)

            # # # # 排行榜

            if total_num == 1:
                self.rank_1 = tk.Label(self.BG_label, text = '1', font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1.place(relx=0.5, rely=0.41)
                self.rank_1_id = tk.Label(self.BG_label, text = rank_info[0][1][0], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1_id.place(relx=0.6, rely=0.41)
                self.rank_1_money = tk.Label(self.BG_label, text = rank_info[0][1][1], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1_money.place(relx=0.78, rely=0.41)
            
            elif total_num == 2:
                self.rank_1 = tk.Label(self.BG_label, text = '1', font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1.place(relx=0.5, rely=0.41)
                self.rank_1_id = tk.Label(self.BG_label, text = rank_info[0][1][0], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1_id.place(relx=0.6, rely=0.41)
                self.rank_1_money = tk.Label(self.BG_label, text = rank_info[0][1][1], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1_money.place(relx=0.78, rely=0.41)

                self.rank_2 = tk.Label(self.BG_label, text = '2', font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_2.place(relx=0.5, rely=0.49)
                self.rank_2_id = tk.Label(self.BG_label, text = rank_info[1][1][0], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_2_id.place(relx=0.6, rely=0.49)
                self.rank_2_money = tk.Label(self.BG_label, text = rank_info[1][1][1], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_2_money.place(relx=0.78, rely=0.49)
            
            else:
                self.rank_1 = tk.Label(self.BG_label, text = '1', font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1.place(relx=0.5, rely=0.41)
                self.rank_1_id = tk.Label(self.BG_label, text = rank_info[0][1][0], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1_id.place(relx=0.6, rely=0.41)
                self.rank_1_money = tk.Label(self.BG_label, text = rank_info[0][1][1], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_1_money.place(relx=0.78, rely=0.41)

                self.rank_2 = tk.Label(self.BG_label, text = '2', font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_2.place(relx=0.5, rely=0.49)
                self.rank_2_id = tk.Label(self.BG_label, text = rank_info[1][1][0], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_2_id.place(relx=0.6, rely=0.49)
                self.rank_2_money = tk.Label(self.BG_label, text = rank_info[1][1][1], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_2_money.place(relx=0.78, rely=0.49)

                self.rank_3 = tk.Label(self.BG_label, text = '3', font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_3.place(relx=0.5, rely=0.57)
                self.rank_3_id = tk.Label(self.BG_label, text = rank_info[2][1][0], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_3_id.place(relx=0.6, rely=0.57)
                self.rank_3_money = tk.Label(self.BG_label, text = rank_info[2][1][1], font = "Courier", bg = 'white', height = 0, fg = '#2E4058')
                self.rank_3_money.place(relx=0.78, rely=0.57)
       
            #=========================顯示最後金額=====================#

            self.final_money = tk.Label(self.BG_label, text = str(score), font = f2, bg = '#FAF1EA', height = 0, fg = '#2E4058')
            self.final_money.place(relx=0.15, rely=0.32)
        
        def music(self):
            pygame.mixer.music.stop()
            pygame.mixer.init()
            pygame.mixer.music.load('排行榜影片.mp3')
            pygame.mixer.music.play(0)  


    if __name__ == "__main__":
        main_prgram = main_program()
        main_prgram.mainloop()

    if play[0] == 0:
        again = False