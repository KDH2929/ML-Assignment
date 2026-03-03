import pandas as pd
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


# 데이터 로드
data = pd.read_csv('cleaned_data2.csv')

# '순위' 컬럼을 범주형으로 변환 (필요시)
data['순위'] = data['순위'].astype('category')

# 결과를 저장할 데이터프레임 생성
results = pd.DataFrame(columns=['Column', 'Chi2 Stat', 'p-value', 'Degrees of Freedom'])

# '순위' 컬럼과 각 컬럼 간의 카이제곱 독립성 검정
for column in data.columns:
    if column != '순위':
        # 교차표 생성
        contingency_table = pd.crosstab(data['순위'], data[column])

        # 카이제곱 검정 수행
        chi2, p, dof, _ = chi2_contingency(contingency_table)

        # 결과 저장
        new_row = pd.DataFrame({'Column': [column], 'Chi2 Stat': [chi2], 'p-value': [p], 'Degrees of Freedom': [dof]})
        results = pd.concat([results, new_row], ignore_index=True)

# p-value 기준으로 정렬
results = results.sort_values(by='p-value')

# 결과 출력
print(results)

# 결과를 p-value 기준으로 정렬
results = results.sort_values(by='p-value')

# 막대 그래프 생성
plt.figure(figsize=(20, 20))  # 그래프 크기 조정
plt.barh(results['Column'], results['p-value'])
plt.xlabel('p-value', fontsize=14)
plt.ylabel('Column', fontsize=14)
plt.title('순위와 각 Column들의 카이제곱 검정에 따른 독립성검사', fontsize=16)
plt.axvline(0.05, color='red', linestyle='--', label='0.05 significance level')
plt.legend()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

# 그래프를 파일로 저장
plt.savefig('chi_square_test_results.png', dpi=300, bbox_inches='tight')
plt.close()