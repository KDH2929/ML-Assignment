import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import missingno as msno


plt.rcParams["font.family"] = 'Malgun Gothic'
plt.rcParams["font.size"] = 15

# 데이터 로드
df = pd.read_csv("horse_datas.csv", encoding='utf-8')

# '산지' 컬럼의 값 개수를 세고, 시각화
cnts = df['산지'].value_counts()

# Seaborn을 사용한 바 차트
sns.barplot(x=cnts.index, y=cnts.values)
plt.title('산지 별 말의 개수')
plt.xlabel('산지')
plt.ylabel('개수')
plt.xticks(rotation=45)  # x 축 라벨을 45도 회전하여 표시
plt.show()