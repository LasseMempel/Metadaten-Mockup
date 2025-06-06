import requests
import pandas as pd

dataUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRb0tjnjkyjzReZ_--dYJOD4rbl1_iV8EdVTFXATh9ie6u3bRAeEYYrMNKZF0AcM_PQJkQbmZyGFfYe/pub?gid=0&single=true&output=csv"
# read csv from url
df = pd.read_csv(dataUrl)
print(df.head())
# delete column "note (source)"
df = df.drop(columns=["note (source)", "altLabel"])
# change name of column "scope note" to "mandatory"
df = df.rename(columns={"scope": "mandatory"})
# save pf as csv
df.to_csv("data.csv")