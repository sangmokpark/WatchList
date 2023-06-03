import csv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 크롬 드라이버 경로 설정
driver_path = "C:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(driver_path)

# KOBISS 사이트 접속
driver.get("https://www.kobis.or.kr/kobis/business/stat/boxs/findFormerBoxOfficeList.do")

movie_list = driver.find_element_by_xpath('//*[@id="content"]/div[4]/table/tbody')
movies = movie_list.find_elements_by_tag_name("tr")

if not os.path.exists('movies.csv'):
    with open('movies.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'cast', 'genre', 'storyline'])

max_rows = 1000
file_name = 'movies.csv'

with open(file_name, 'a', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)

    for movie in movies:
        # 스크롤 한 칸 내리기
        driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")

        # 영화 정보 링크 클릭
        link = movie.find_element_by_class_name("tal")
        link.click()
        time.sleep(2)

        # 영화 정보 수집
        try:
            title = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div/strong')
            desc_info = driver.find_element_by_class_name("desc_info")
            staff = driver.find_element_by_xpath('//div[@class="info info2"]/div[@class="staffMore"]')
            genre = driver.find_element_by_css_selector('.ovf.cont dt:nth-of-type(4) + dd')
            print(title.text, staff.text, genre.text, desc_info.text)

            # 영화 정보 저장
            if sum(1 for _ in csv.reader(open(file_name, encoding='utf-8'))) >= max_rows:
                break
            writer.writerow([title.text, staff.text, genre.text, desc_info.text])
            close = driver.find_element_by_css_selector('a.close')
            close.click()
            time.sleep(2)
        except:
            print("영화 정보 수집 실패")
            time.sleep(2)

driver.quit()
