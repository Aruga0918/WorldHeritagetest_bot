import random
import pandas as pd
df = pd.read_csv(filepath_or_buffer="heritage_list.csv")
def view(quary):
    target = df[df["name"] == quary]
    return random.choice(target.values)[5]

if __name__=="__main__":
    print(view("イエローストーン国立公園"))