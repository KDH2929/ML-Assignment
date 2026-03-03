import pandas as pd

# 데이터 로드
df = pd.read_csv("horse_datas.csv", encoding='utf-8')

# 시간을 초로 변환하는 함수
def convert_time_to_seconds(t):
    if pd.isna(t) or t.strip() == "":
        return None
    minutes, seconds = t.split(':')
    return int(minutes) * 60 + float(seconds)

# 시간 데이터가 있는 컬럼 이름 지정
time_columns = ["S1F지점", "1코너지점", "2코너지점", "3코너지점", "G3F지점", "4코너지점", "G1F지점", "3F-G", "1F-G", "경주기록"]

# 각 시간 컬럼에 대해 시간 변환 적용
for column in time_columns:
    if column in df.columns:  # 컬럼이 실제로 데이터프레임에 있는지 확인
        df[column] = df[column].apply(convert_time_to_seconds)

# 변경된 데이터프레임을 새 파일로 저장
df.to_csv("horse_datas2.csv", index=False, encoding='utf-8')

print("변환 완료 및 파일 저장 완료")
