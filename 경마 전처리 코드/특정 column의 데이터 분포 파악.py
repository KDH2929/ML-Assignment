import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import missingno as msno


plt.rcParams["font.family"] = 'Malgun Gothic'
plt.rcParams["font.size"] = 15

df = pd.read_csv("horse_datas.csv", encoding='utf-8')

cnt = df['산지'].value_counts()

print(cnt)