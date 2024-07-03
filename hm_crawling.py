from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd

# 올바른 ChromeDriver 경로 설정
driver_path = 'D:/IDA/chromedriver-win64/chromedriver-win64/chromedriver.exe'  # chromedriver.exe의 정확한 경로로 변경
service = Service(driver_path)

# Chrome 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--allow-insecure-localhost')

# WebDriver 초기화
driver = webdriver.Chrome(service=service, options=options)

# 웹 페이지 열기
driver.get('https://www2.hm.com/ko_kr/productpage.1240205001.html')  # 대상 웹 페이지의 URL로 변경

try:
    # 버튼 클릭 (XPath로 찾기)
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'CTA-module--action__1qN9s CTA-module--medium__1uoRl CTA-module--reset__1G6AO CTA-module--inline__1rDLl CTA-module--iconPosition-start__1xBvp')]"))
    )
    button.click()

    # 테이블이 나타날 때까지 대기 (XPath 사용)
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'SizeRangeTabContent-module--sizeTable__1hkvr')]"))
    )

    # 테이블 크롤링
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        cols = [col.text for col in cols]
        data.append(cols)

    # 데이터프레임으로 변환
    df = pd.DataFrame(data)

    print(df)

    # 엑셀 파일로 저장
    df.to_excel('size_table.xlsx', index=False)

finally:
    # 드라이버 종료
    driver.quit()
