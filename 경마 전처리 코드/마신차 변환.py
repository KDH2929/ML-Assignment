import pandas as pd

# 데이터 로드
df = pd.read_csv("horse_datas3-3.csv", encoding='utf-8')

# 변환 함수
def convert_distance(value):
    value = str(value).strip().lower()
    if '코' in value:
        return 0.006  # 코차 평균값
    elif '머리' in value:
        return 0.013  # 머리차 평균값
    elif '목' in value:
        return 0.032  # 목차 평균값
    elif '1/2 마신' in value or '½ 마신' in value:
        return 0.5    # 1/2 마신
    elif '1마신' in value:
        return 1.0    # 1 마신
    elif '출전취소' in value or '출전제외' in value or '주행중지' in value:
        return None   # 경주 미참가 처리
    else:
        try:
            # 분수를 십진수로 변환
            value = value.replace('¼', '.25').replace('½', '.5').replace('¾', '.75')
            return float(value)  # 숫자 변환
        except ValueError:
            return None  # 숫자로 변환할 수 없는 경우 None 처리

# 도착차 컬럼 변환
df['도착차'] = df['도착차'].apply(convert_distance)

# 변경된 데이터프레임을 새 파일로 저장
df.to_csv("horse_datas4-4.csv", index=False, encoding='ANSI')

print("변환 완료 및 파일 저장 완료")
