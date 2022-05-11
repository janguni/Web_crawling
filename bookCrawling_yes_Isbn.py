from pickle import FALSE
from selenium import webdriver
import urllib.request
import time
from openpyxl import Workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
options = webdriver.ChromeOptions()


# 책의 상세페이지로 이동하여 책의 isbn, 책 표지, 책 제목, 저자, 출판사 크롤링


ts = []
ts.append(["book_isbn", "book_img_url", "book_title","book_author", "book_publisher", "genre_name"])


#알라딘 사이트로 이동
def move_to_aladin_site():
    driver.get('https://www.aladin.co.kr/home/wbookmain.aspx?start=we_tab')
    driver.find_element_by_xpath('//*[@id="browse26"]/a').click()  # 카테고리 클릭 (browse뒤의 숫자를 바꿔 카테로리 별로 따로 크롤링 하였음)
    time.sleep(2)
    driver.find_element_by_class_name('bk5').click()  # 도서 모두 보기 클릭


# 페이지 별 책의 상세정보로 이동하여 책의 정보를 ts에 저장
def find_book_info_in_page(genre_name):
    books = driver.find_elements_by_class_name('ss_book_box')
    urls=[]
    for book in books: # 책의 url들을 얻어옴
        url = book.find_element_by_xpath(
            './table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/a').get_attribute('href')
        urls.append(url)

    for url in urls:
        print("-----------------------------------------")
        time.sleep(2)
        driver.get(url)
        time.sleep(5)

        try: # 19금 책의 상세정보에 들어갔을 경우 로그인하는 경고창을 무시하고 다음 책으로 넘어감
            Alert(driver)
            Alert(driver).dismiss()
            continue
        except:

            #책 isbn
            info_list = driver.find_element_by_class_name('conts_info_list1')
            ul = info_list.find_element_by_xpath('./ul')
            li_num = len(ul.find_elements_by_tag_name('li'))
            isbn = ul.find_element_by_xpath('./li['+ str(li_num) +']').text
            print(isbn)


            #책 표지
            img = driver.find_element_by_id('CoverMainImage').get_attribute('src')

            # 책 제목
            title = driver.find_element_by_class_name('Ere_bo_title').text

            # 작가 이름
            try:
                author = driver.find_element_by_xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[3]/a[1]').text
            except:  # 책들 중 바탕에 색깔이 들어간 책
                author = driver.find_element_by_xpath('//*[@id="Ere_prod_allwrap"]/div[1]/div[3]/div[2]/div[1]/div/ul/li[3]/a[1]').text
            print(author)

            # 출판사
            class_num = len(driver.find_elements_by_class_name('Ere_sub2_title'))-1
            try:
                driver.find_element_by_xpath("//a[contains(text(), '원제 :')]")
                class_num -= 1
            except:
                pass

            try:
                publisher = driver.find_element_by_xpath('//*[@id = "Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[3]/a[' + str(class_num) + ']').text
            except: # 책들 중 바탕에 색깔이 들어간 책
                publisher = driver.find_element_by_xpath('//*[@id = "Ere_prod_allwrap"]/div[1]/div[3]/div[2]/div[1]/div/ul/li[3]/a[' + str(class_num) + ']').text
            print(publisher)

            #ts에 저장
            ts.append([isbn, img, title, author, publisher, genre_name])


for i in range(1, 11):
    driver = webdriver.Chrome('./chromedriver')
    move_to_aladin_site()

    driver.find_element_by_xpath('//*[@id="short"]/div[' + str(i) + ']/a').click()
    time.sleep(1)

    genre_name = "컴퓨터/모바일"  # 카테고리 별로 이름을 달리 씀
    find_book_info_in_page(genre_name)

    driver.close()
    
    if i ==1: i += 2
    else: i += 1

    time.sleep(0.5)

wb = Workbook()
ws = wb.active
for data in ts:  # 엑셀 저장 1줄씩 생성
     ws.append(data)

wb.save('./bookList_20.xlsx') # 카테고리 별로 bookList_뒤의 숫자를 달리 씀
