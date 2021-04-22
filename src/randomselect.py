import random
import pandas as pd
df = pd.read_csv(filepath_or_buffer="heritage_list.csv")

def select(quary):
    if quary.isnumeric():
        cand = df[df["chaputar"] == int(quary)]
    elif quary.endswith("遺産"):
        cand = df[df["class"] == quary]
    else:
        cand = df[df["country"] == quary]
    
    if len(cand) != 0:    
        heritage = random.choice(cand.values)[0]
    
    else:
        heritage = "no heritage"
    return heritage

def randomchoice():
    # df = pd.read_csv(filepath_or_buffer="heritage_list.csv")
    chosen = random.choice(df.values)[3]
    return chosen

def right(heritage):
    answer = random.choice(df[df["name"] == heritage].values)[3]
    return answer

print(select("ドイツ"))
print(randomchoice())
print(right("アーヘンの大聖堂"))