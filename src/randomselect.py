import random
import pandas as pd

def select(quary):
    df = pd.read_csv(filepath_or_buffer="heritage_list.csv")
    if quary =="自然遺産" or "文化遺産" or "複合遺産" or "危機遺産":
        cand = df[df["class"] == quary]
    else:
        cand = df[df["country"] == quary]
         
    # heritage = random.choice(cand.values)[0]
    # # return csv_input
    return cand

print(select("自然遺産"))