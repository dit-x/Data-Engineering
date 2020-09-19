import pandas as pd
import re

df = pd.read_csv("covid19_Donors.csv")

def convert(x):
    if "B" in x:
        return round(float(x.replace("Billion",""))*1000000000, 2)
    elif  "M" in x:
        return round(float(x.replace("Million",""))*1000000, 2)
    else:
        return round(float(x), 2)

df["value_granted"] = df.value_granted.apply(lambda x: x.replace("$", "").replace(",",""))

df["value_granted"] = df["value_granted"].apply(convert)

df.to_csv("covid19_donors_data_cleaned.csv")