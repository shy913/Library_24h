from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import time
import schedule


def book(data: dict):
    time.sleep(0.5)
    try:
        with open('library_cookie.txt', 'r') as f:
            coo = f.read()
        current_time = datetime.now().strftime('%H:%M:%S.%f')
        print('sending request at:', current_time)
        text = requests.post(url="https://there.shu.edu.cn/api/v3/bookings", headers={'Cookie': str(coo)},
                             json=data).text
        print(text)
        if "同一用户10秒只能提交一次" in text or "15秒" in text:
            book(data)
        return text
    except:
        book(data)


def get_cookie(username: str, password: str):
    url = 'https://oauth.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE3MjcwODA4NTQ0NDg4NTA1OTksInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6ImVEcmQtTTBpMFdvU1dSeGs3U2hEQzFuLWZiUzdqUnZpIiwic2NvcGUiOiIxIiwicmVkaXJlY3RVcmkiOiJodHRwczovL3RoZXJlLnNodS5lZHUuY24vbG9naW4tb2F1dGgyIiwic3RhdGUiOiIifQ=='
    service = Service(service_args=['--log-level=OFF'], executable_path=r'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    # time.sleep(1)
    driver.find_element(By.XPATH, value='/html/body/div/div[3]/div/div/form/div[1]/input').send_keys(username)
    driver.find_element(By.XPATH, value='/html/body/div/div[3]/div/div/form/div[2]/input[2]').send_keys(password)
    driver.find_element(By.XPATH, value='/html/body/div/div[3]/div/div/form/button').click()
    time.sleep(1)
    driver.get('https://there.shu.edu.cn/mobile/seat2021#/pages/home/index')
    time.sleep(1)

    driver.find_element(By.XPATH,
                        value='/html/body/div/div/div/div/div/taro-view-core/taro-view-core[8]/taro-view-core[2]/taro-view-core/taro-view-core').click()
    coo = driver.get_cookies()
    cookie = (f'HYS_LANG={coo[2]["value"]}; '
              f'authenticityToken={coo[1]["value"]}; '
              f'SPHYS_SESSION={coo[0]["value"]}; ')
    # print(coo[0])
    # print(coo[1])
    # print(coo[2])
    with open('library_cookie.txt', 'w') as f:
        f.write(cookie)
    print('successfully wrote cookie')


if __name__ == '__main__':
    # t = '19:19:00'
    t = '20:00:00'

    data = {"rooms": [
       {"id": "？？？", "name": "？？？", "officeAreaId": "WyN53UzbmRsLjpR1t1ttWL", "disabled": False,
       "showOrder": 29, "isBusy": False, "isBooked": False, "abilities": ["booking"]}],
       "times": [{"startDate": tomorrow, "startTime": "14:30", "endDate": tomorrow, "endTime": "20:00"}],
       "subject": "？？？",
       "meetingMembers": ["？？？"]}

    while True:
        index = int(input(f'Enter index: \n[1]: get cookie\n[2]: book\n[3]: wait till {t}\n'))
        if index == 1:
            # get username & password
            info = {}
            with open('Info.txt', "r") as f:
                student_info = f.read()
            for item in student_info.split("\n"):
                info[item.split(":")[0]] = item.split(":")[1]

            # write cookie
            get_cookie(info['student_id'], info['password'])
        elif index == 2:

            book(data)
        elif index == 3:
            print('waiting from', datetime.now().strftime('%H:%M:%S.%f'))

            schedule.every().day.at(t).do(lambda: book(data))

            while True:
                schedule.run_pending()
                time.sleep(0.001)
