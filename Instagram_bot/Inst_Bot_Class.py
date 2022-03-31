# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from DataUser import login, password
from selenium.common.exceptions import NoSuchElementException
import requests
import os

class InstagramBot:

    def __init__(self, log, passw):
        self.login = log
        self.password = passw
        self.driver = webdriver.Chrome('D:\chromedriver.exe')

    def close(self):
        self.driver.close()
        self.driver.quit()

    def login_acc(self):

        url = 'https://www.instagram.com'
        driver = self.driver
        driver.get(url)
        time.sleep(3)

        # находим на странице строку для ввода логина и вводим туда наш логин
        login_input = driver.find_element_by_name(name="username")
        login_input.clear()
        login_input.send_keys(self.login)

        time.sleep(random.randrange(1, 3))

        # находим на странице строчку для ввода пароля и вводим туда наш пароль
        password_input = driver.find_element_by_name(name="password")
        password_input.clear()
        password_input.send_keys(self.password)

        # Эмулируем нажатие кнопки ENTER
        password_input.send_keys(Keys.ENTER)
        time.sleep(120)

    def Like_Foto(self, hashtag):
        driver = self.driver

        driver.get(f'https://www.instagram.com/explore/tags/{hashtag}')
        time.sleep(3)

        for i in range(1, 4):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)

        # Соберем все ссылки по тегу
        hrefs = driver.find_elements_by_tag_name('a')

        # Создадим список для ссылок
        url_list = [items.get_attribute('href') for items in hrefs if '/p/' in items.get_attribute('href')]

        print(url_list)
        # url_page = []
        for adress in url_list[0:2]:
            try:
                driver.get(adress)
                time.sleep(2)

                like_button = driver.find_element_by_css_selector(
                    'div.ltEKP span.fr66n button.wpO6b').click()
                # Задержка на установку лайков, т.к есть ограничения по числу лайков
                time.sleep(random.randrange(8, 10))
            except Exception as ex:
                print(ex)
                self.close()
        # print(url_page)
        self.close()

    def css_exists(self, adress):
        driver = self.driver
        try:
            driver.find_element_by_css_selector(adress)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def xpath_exists(self, adress):
        driver = self.driver
        try:
            driver.find_element_by_xpath(adress)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # Ставим лайк на пост по ссылке
    def like(self, userpost):
        driver = self.driver
        driver.get(userpost)
        time.sleep(5)

        wrong_userpage = '/html/body/div[1]/section/main/div/div/h2'
        if self.xpath_exists(wrong_userpage):
            print('Такого поста не существует проверьте URL')
            self.close()
        else:
            print('Пост найден, ставим лайк!')
            time.sleep(2)
            like_button = 'div.ltEKP span.fr66n button.wpO6b'
            driver.find_element_by_css_selector(like_button).click()
            time.sleep(2)

            print(f'Лайк на пост: {userpost} поставлен')
            self.close()

    # МЕТОД СБОРА ПОСТОВ
    def post_url_all(self, userpage):
        driver = self.driver
        driver.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)

            posts_count = int(driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = driver.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    # Ставим лайки на страницу по ссылке
    def put_likes_in_page(self, userpage):
        driver = self.driver
        self.post_url_all(userpage)
        file_name = userpage.split('/')[-2]
        time.sleep(4)

        with open(f'{file_name}_set.txt', 'r') as file:
            urls_list = file.readlines()
            for post_url in urls_list[0:6]:
                try:
                    driver.get(post_url)
                    time.sleep(2)

                    like_button = 'div.ltEKP span.fr66n button.wpO6b'
                    driver.find_element_by_css_selector(like_button).click()
                    # Задержка на установку лайков, т.к есть ограничения по числу лайков
                    time.sleep(random.randrange(3, 4))
                    print(f'Лайк на пост {post_url} успешно установлен')
                except Exception as ex:
                    print(ex)
                    self.close()
        self.close()

    def download_userpage_content(self, userpage):

        driver = self.driver
        self.post_url_all(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        driver.get(userpage)
        time.sleep(4)

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует!")
        else:
            os.mkdir(file_name)

        img_and_video_src_urls = []
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list:
                try:
                    driver.get(post_url)
                    time.sleep(4)

                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = driver.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        video_src_url = driver.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        # print("Упс! Что-то пошло не так!")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки!")
                    print(f"Контент из поста {post_url} успешно скачан!")

                except Exception as ex:
                    print(ex)
                    self.close()

            self.close()

        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")


my_bot = InstagramBot(login, password)
my_bot.login_acc()
# my_bot.Like_Foto("serfing")
my_bot.download_userpage_content('https://www.instagram.com/juliette/')
