import pandas as pd

# 데이터 로드
df = pd.read_csv("horse_datas7.csv", encoding='ANSI')


# 장구현황 정제 함수
def clean_gear(gear_str):
    if pd.isna(gear_str):
        return ""  # 결측치는 빈 문자열로 처리
    gear_str = str(gear_str)  # 모든 입력을 문자열로 변환
    current_gears = []
    gears = gear_str.split(',')
    for gear in gears:
        gear = gear.strip()
        if '-' in gear:  # 해지된 장구는 제외
            continue
        elif '+' in gear:  # 신규 추가된 장구에서 '+' 제거
            current_gears.append(gear.replace('+', ''))
        else:  # 기타 장구 (변경 없음)
            current_gears.append(gear)
    return ', '.join(current_gears)

# 정제된 장구현황 적용
df['장구현황'] = df['장구현황'].apply(clean_gear)


# 변경된 데이터프레임을 새 파일로 저장
df.to_csv("horse_datas8.csv", index=False, encoding='ANSI')

print("변환 완료 및 파일 저장 완료")
