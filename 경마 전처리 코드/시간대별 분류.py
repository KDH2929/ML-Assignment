import pandas as pd

# 데이터 로드
df = pd.read_csv("horse_datas8.csv", encoding='ANSI')

# 시간 파싱 및 시간대 분류 함수
def classify_time(time_str):
    hour = int(time_str.split(':')[0])
    if 6 <= hour < 12:
        return '아침'
    elif 12 <= hour < 17:
        return '낮'
    elif 17 <= hour < 21:
        return '저녁'
    else:
        return '밤'

# 시간대 분류 적용
df['시작 시간 분류'] = df['시작 시간'].apply(classify_time)

# '시작 시간 분류' 컬럼을 '시작 시간' 컬럼 바로 뒤에 삽입
time_col_index = df.columns.get_loc('시작 시간') + 1
df.insert(loc=time_col_index, column='시작 시간 분류', value=df.pop('시작 시간 분류'))

# 변경된 데이터프레임을 새 파일로 저장
df.to_csv("horse_datas9.csv", index=False, encoding='ANSI')

print("변환 완료 및 파일 저장 완료")
