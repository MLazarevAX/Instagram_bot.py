# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from DataUser import login, password

'''
def autorization(login, password):
    url = 'https://www.instagram.com'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(random.randrange(4, 6))
    try:
        # находим на странице строку для ввода логина и вводим туда наш логин
        login_input = driver.find_element_by_name(name="username")
        login_input.clear()
        login_input.send_keys(login)

        time.sleep(random.randrange(1, 3))

        # находим на странице строчку для ввода пароля и вводим туда наш пароль
        password_input = driver.find_element_by_name(name="password")
        password_input.clear()
        password_input.send_keys(password)

        # Эмулируем нажатие кнопки ENTER
        password_input.send_keys(Keys.ENTER)
        time.sleep(12)

        driver.close()
        driver.quit()
    except Exception:
        driver.close()
        driver.quit()
        print(Exception)
'''





def like_post(login, password, hashtag):

    url = 'https://www.instagram.com'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(random.randrange(4, 6))
    try:
        # находим на странице строку для ввода логина и вводим туда наш логин
        login_input = driver.find_element_by_name(name="username")
        login_input.clear()
        login_input.send_keys(login)

        time.sleep(random.randrange(1, 3))

        # находим на странице строчку для ввода пароля и вводим туда наш пароль
        password_input = driver.find_element_by_name(name="password")
        password_input.clear()
        password_input.send_keys(password)

        # Эмулируем нажатие кнопки ENTER
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)
        try:
            driver.get(f'https://www.instagram.com/explore/tags/{hashtag}')
            time.sleep(3)

            #Иммитируем скрол страниц,для прогрузки постов
            for i in range(1,4):
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)

            # Соберем все ссылки по тегу
            hrefs = driver.find_elements_by_tag_name('a')

            # Создадим список для ссылок
            url_list = [items.get_attribute('href') for items in hrefs if '/p/' in items.get_attribute('href')]
            ''' Тоже самое только стандартно
            for items in hrefs:
                href = items.get_attribute('href')
                if '/p/' in href:
                    url_list.append(href)
            '''
            print(url_list)
            for adress in url_list[0:2]:
                try:
                    driver.get(adress)
                    time.sleep(2)
                    like_button = driver.find_element_by_css_selector('div.ltEKP span.fr66n button.wpO6b').click()
                    # Задержка на установку лайков, т.к есть ограничения по числу лайков
                    time.sleep(random.randrange(80, 100))
                except Exception as ex:
                    print(ex)
                    driver.close()
                    driver.quit()
            driver.close()
            driver.quit()
        except Exception as ex:
            driver.close()
            driver.quit()
            print(ex, "какая то хуита")

    except Exception:
        driver.close()
        driver.quit()
        print(Exception)

if __name__ == '__main__':
    like_post(login, password, 'surfing')
# autorization(login, password)
