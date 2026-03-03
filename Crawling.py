from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# 폴더 생성 확인
folder_path = "Horse_racing_datas"
os.makedirs(folder_path, exist_ok=True)


# WebDriver 설정
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)  # 10초 동안 요소를 기다릴 수 있도록 설정

driver.get("http://race.kra.co.kr/raceScore/scoretablePeriodScoreList.do")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']//span[contains(text(),'기간별검색')]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='arg_Year1']/option[text()='2024']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='arg_Mon1']/option[text()='01']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='arg_Day1']/option[text()='01']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']//span[contains(text(),'검색')]"))).click()

count = 0
try:
    while True:
        links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table//td[@class='alignL']//a")))
        total_links = len(links)

        for i in range(total_links):
            # 링크를 새로 찾아 매번 클릭
            current_link = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table//td[@class='alignL']//a")))[i]
            current_link.click()
            time.sleep(2)  # 페이지 전환 대기

            # 데이터 추출 로직

            # 공통 정보 추출
            common_info_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tableType1 table")))
            # 첫 번째 행 (날씨, 주로 상태, 습도, 시작시간)
            first_row = common_info_table.find_element(By.CSS_SELECTOR, "tbody tr:nth-of-type(1)")
            details = first_row.find_elements(By.CSS_SELECTOR, "td.bgnone")
            weather = details[2].text
            track_condition = details[3].text
            humidity = details[4].text
            start_time = details[5].text

            # 두 번째 행 (등급, 거리)
            second_row = common_info_table.find_element(By.CSS_SELECTOR, "tbody tr:nth-of-type(2)")
            grade = second_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(1)").text
            distance = second_row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2)").text

            # 경주 데이터 추출
            table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tableType2")))
            columns_name = [th.text for th in table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")]
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            race_details = []

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                row_data = [column.text.strip() for column in columns]
                row_data.extend([weather, track_condition, humidity, start_time, grade, distance])  # 공통 정보 추가
                race_details.append(row_data)

            # DataFrame 생성 및 저장
            columns_name.extend(['날씨', '주로 상태', '습도', '시작 시간', '등급', '거리'])
            df1 = pd.DataFrame(race_details, columns=columns_name)

            # 두 번째 경주 데이터 테이블 추출 (통과 누적기록, 펄롱타임)
            second_table = driver.find_elements(By.CSS_SELECTOR, "div.tableType2")[1]
            second_table_rows = second_table.find_elements(By.CSS_SELECTOR, "tbody tr")
            second_table_data = [[cell.text for cell in row.find_elements(By.TAG_NAME, "td")][-10:] for row in
                                 second_table_rows]  # 마지막 10개 열만 추출

            df2 = pd.DataFrame(second_table_data,
                               columns=['S1F지점', '1코너지점', '2코너지점', '3코너지점', 'G3F지점', '4코너지점', 'G1F지점', '3F-G', '1F-G', '경주기록'])

            df3 = pd.concat([df1, df2], axis=1)  # DataFrame 병합

            df3.to_csv(f"{folder_path}/race_data_{count}.csv", index=False, encoding='utf-8')


            driver.execute_script("window.history.go(-1)")  # 이전 페이지로 돌아가기
            time.sleep(2)  # 페이지 재로드 대기

            count += 1  # count 증가

        # 다음 페이지 이동
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button']//span[contains(text(),'다음')]")))
        next_button.click()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    print("Data collection completed.")