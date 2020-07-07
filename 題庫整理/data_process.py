import csv
import pickle

class Question:
    def __init__(self, statement , option_A, option_B, option_C, option_D, ans, ans_time):
        self.statement = statement
        self.option_A = option_A
        self.option_B = option_B
        self.option_C = option_C
        self.option_D = option_D
        self.ans = ans
        self.ans_time = ans_time

# # # # # # # # # # # # # 將題目資料儲存成需要的格式 (可忽略不看) # # # # # # # # # # # # # 

# # 讀入檔案路徑，並開啟檔案
# data_path = 'G:\\我的雲端硬碟\\學習\\商研\\Python\\assignment\\Final Project\\題目.csv'
# data_file = open(data_path, 'r', encoding='utf-8')
# Q_data = csv.DictReader(data_file)  # 讀取CSV檔資料，並存進submit_data


# leve_Qs = dict()

# for per_row in Q_data:
#     statement = per_row["statement"]
#     option_A = per_row["option_A"]  
#     option_B = per_row["option_B"]
#     option_C = per_row["option_C"]
#     option_D = per_row["option_D"]
#     ans = per_row["answer"]
#     ans_time = per_row["time"]
#     level = per_row["level"]

#     per_Q = Question(statement , option_A, option_B, option_C, option_D, ans, ans_time)

#     if level not in leve_Qs:
#         leve_Qs[level] = (per_Q,)
#     else:
#         leve_Qs[level] += (per_Q,)

# data_file.close()

# # # 將分類好的dictionary 存成pickle格式
# with open('question_data.pickle', 'wb') as file:
#     pickle.dump(leve_Qs, file)




# # # # # # # # # # # # # 匯入處理好的題目data# # # # # # # # # # # # # 

with open('question_data.pickle', 'rb') as file:
    level_Qs = pickle.load(file)

# # # 說明 
# level_Qs 為一個dictionary
# keys = ['W>L (*3)', 'W>L (*1)', 'W=L (*2)', 'W>L (*2)', 'W=L (*3)', 'W=L (*1)', 'W<L (*3)', 'W<L (*2)', 'W<L (*1)']
# values 各level所對應的所有questions，並存成tuple
# tuple的每一個element即為一個question 並存成最上面定義的class Question物件

# 若還不懂，請執行下列code就會明白了

questions_WL3 = level_Qs['W>L (*3)']    # 叫出W>L (*3)這個level裡的所有questions (為一個tuple)
first_Q = questions_WL3[0]    # 挑出這個tuple中的第一題

# 叫出這題的各個attribute
print(first_Q.statement)
print(first_Q.option_A)
print(first_Q.option_B)    
print(first_Q.option_C)
print(first_Q.ans)
print(first_Q.ans_time)