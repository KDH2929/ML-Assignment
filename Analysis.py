import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import f1_score, accuracy_score
import matplotlib.pyplot as plt

# 데이터 로드 및 전처리
df = pd.read_csv('horse_datas12.csv', encoding='ANSI')
df['Target'] = df['순위'].apply(lambda x: 1 if x <= 3 else 0)
df.drop(['순위'], axis=1, inplace=True)
df.dropna(inplace=True)

X = df.drop('Target', axis=1)
y = df['Target']

# 데이터 분할 및 스케일링
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
    'gamma': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
    'kernel': ['rbf']
}

# GridSearchCV
grid = GridSearchCV(SVC(), param_grid, scoring='f1', cv=5, return_train_score=True, verbose=1)
grid.fit(X_train_scaled, y_train)

# 결과 데이터 추출
res = grid.cv_results_

# Gamma별 결과 출력
print("Gamma\tC\tTrain F1\tVal F1")
for i in range(len(res['params'])):
    gamma = res['param_gamma'][i]
    c_val = res['param_C'][i]
    train_f1 = res['mean_train_score'][i]
    val_f1 = res['mean_test_score'][i]
    print(f"{gamma:.4f}\t{c_val}\t{train_f1:.4f}\t{val_f1:.4f}")

# 시각화
plt.figure(figsize=(10, 6))

# C값
for c in param_grid['C']:
    mask = (res['param_C'] == c)
    gammas = np.array(res['param_gamma'][mask], dtype=float)
    val_f1_scores = res['mean_test_score'][mask]
    
    plt.plot(gammas, val_f1_scores, marker='o', label=f'Val F1 (C={c})')

plt.xscale('log')
plt.xlabel('Gamma')
plt.ylabel('F1 Score (Class 1)')
plt.title('Grid Search F1 Score by Gamma')
plt.grid(True)
plt.legend()
plt.savefig('grid_search_result.png') # 이미지 저장 추가
plt.show()