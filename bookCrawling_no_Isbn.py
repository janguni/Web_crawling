from pickle import FALSE
from selenium import webdriver
import urllib.request
import time
from openpyxl import Workbook
options = webdriver.ChromeOptions()
# 용량 초괍 방지
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')



# isbn없이 (책의 상세페이지로 가지 않고) 한 페이지에서 25개의 책의 이미지,책 제목, 저자, 출판사를 크롤링



ts = []
ts.append(["isbn","이미지","책 제목","저자","출판사"])
id=0


#알라딘 사이트로 이동
driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.aladin.co.kr/home/wbookmain.aspx?start=we_tab')


driver.find_element_by_xpath('//*[@id="browse1"]/a').click() # 가정/요리 카테고리 클릭
driver.find_element_by_class_name('bk5').click() # 도서 모두 보기 클릭


def select_book(id):
    
    books = driver.find_elements_by_class_name('ss_book_box')
    for book in books:
        time.sleep(1)

        # 책 Id
        id = id + 1

        # 표지
        img = book.find_element_by_css_selector('img').get_attribute('src')

        # 책 제목
        title = book.find_element_by_class_name('bo3').text  # 책 제목

        # 작가, 출판사
        li_count = len(book.find_element_by_xpath(
            './table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul').find_elements_by_tag_name("li"))

        if li_count == 5:  # 책 설명의 위에 특별한 선정이 있는 책
                # (작가)
                author = book.find_element_by_xpath(
                    './table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[3]/a[1]').text

                a_count = len(book.find_element_by_xpath(
                    './table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[3]').find_elements_by_tag_name("a"))
                # (출판사)
                publisher = book.find_element_by_xpath(
                    './table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[3]/a[' + str(a_count) + ']').text

        else:  # 책 설명의 위에 특별한 선정이 없는 책
                # (작가)
                author = book.find_element_by_xpath(
                    './table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[2]/a[1]').text

                a_count = len(book.find_element_by_xpath(
                    './table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[2]').find_elements_by_tag_name("a"))
                # (출판사)
                publisher = book.find_element_by_xpath(
                    './table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[2]/a[' + str(a_count) + ']').text

        #ts에 저장
        ts.append([id, img, title, author, publisher])


page_count=0

# main
while (1):

    page_num = len(driver.find_elements_by_class_name('numbox'))
    page_num = page_num // 2

    if driver.find_elements_by_class_name('numbox_pre'): # 11p 이후
        first_page = 3
    elif driver.find_elements_by_class_name('numbox_first'):  # 10p 이전
        first_page = 1
    else: # 1p
        page_num+=1
        first_page = 1

    for i in range(first_page,first_page + page_num):
        
        time.sleep(1)
        select_book(id)

        if driver.find_elements_by_class_name('numbox_first')==FALSE : # 1p인 경우
            driver.find_element_by_xpath('//*[@id="short"]/div[' + str(i) + ']/a').click()
            i = i + 1
            continue
 
        if page_count <= 100: # 100p 이하인 경우
            driver.find_element_by_xpath('//*[@id="short"]/div[' + str(i) + ']/a').click()
            #print(driver.find_element_by_xpath('//*[@id="short"]/div[' + str(i) + ']/a').text)
            print("page_count: ",page_count)
            page_count += 1
        else: # 101p 이상인 경우
            driver.find_element_by_xpath('//*[@id="middle"]/div[' + str(i) + ']/a').click()
            print(driver.find_element_by_xpath('//*[@id="middle"]/div[' + str(i) + ']/a').text)
            print("page_count: ", page_count)
            page_count += 1

    time.sleep(0.5)
    
    if driver.find_elements_by_class_name('numbox_next'): # 다음 페이지들이 있을 경우
        driver.find_element_by_class_name('numbox_next').click()

    else: #마지막 페이지 일 경우
        break


wb = Workbook()
ws = wb.active
for data in ts: # 엑셀 저장 1줄씩 생성
   ws.append(data)

wb.save('./ex1.xlsx')
        



#브라우저 뒤로 2번 가기 ->
#driver.forward()
#driver.forward()


#wb = Workbook()
#ws = wb.active
#for data in ts: # 엑셀 저장 1줄씩 생성
#    ws.append(data)

#wb.save('./ex3.xlsx')

#count=1
#for i in range(1,26):
    #driver.find_element_by_id('Myform')
    #imageURL = driver.find_elements_by_css_selector("Myform > div:nth-child(2) > div:nth-child(1) > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > div > a > img").get_attribute('src')
    #count += 1
    #print(image)

#Myform > div:nth-child(2) > div:nth-child(1) > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > div > a > img
#Myform > div:nth-child(2) > div:nth-child(2) > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > div > a > img
#Myform > div:nth-child(2) > div:nth-child(3) > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > div > a > img


# ------------pratice-------------#
# 이미지
#imgURL = driver.find_element_by_class_name('i_cover').get_attribute("src")

# 책 제목
#title = driver.find_element_by_class_name('bo3').find_element_by_tag_name('b').text

# 저자
#author = driver.find_elements_by_css_selector('Myform > div:nth-child(2) > div:nth-child(1) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(1)')
#Root_class = driver.find_elements_by_class_name('ss_book_list')
#Root_class.find_elements_by
#print(author)


#urllib.request.urlretrieve(imgURL, "jey"+ ".jpg")






