import pandas as pd
from scipy.stats import chi2_contingency

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

# p-value가 0.05 이하인 컬럼 선택
significant_columns = results[results['p-value'] <= 0.05]['Column']

# p-value가 0.05 이하인 컬럼들 제거
columns_to_remove = significant_columns.tolist()
data_cleaned = data.drop(columns=columns_to_remove)

# 결과를 cleaned_data3.csv로 저장
data_cleaned.to_csv('cleaned_data3.csv', index=False)
