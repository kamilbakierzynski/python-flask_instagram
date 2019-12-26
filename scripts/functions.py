import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scripts import selenium_browser
from scripts.file_management import append_to_statistics, write_to_last_run
from scripts.settings import WAIT_TIME_FOR_LIST_SCROLL, TIME_BETWEEN_FOLLOWS
import random
from collections import Counter



def unfollow_list(people_to_unfollow, FOLLOWS_TO_KEEP, skip_above):
    browser = selenium_browser.get_browser()
    people_skipped = []
    for acc in people_to_unfollow:
        if acc not in FOLLOWS_TO_KEEP:
            browser.get(f'https://www.instagram.com/{acc}/')
            follow_number = browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(',', '')
            try:
                int(follow_number)
            except:
                follow_number = 0
            if int(follow_number) < skip_above:
                follow_button = browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
                follow_button.click()
                confirm_button = browser.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]')
                confirm_button.click()
                time.sleep(TIME_BETWEEN_FOLLOWS)
            else:
                people_skipped.append(acc)
    return people_skipped


def instagram_login(username, password):
    browser = selenium_browser.get_browser()
    browser.get('https://www.instagram.com/accounts/login/')
    login_field = browser.find_element_by_name('username')
    login_field.send_keys(username)
    password_field = browser.find_element_by_name('password')
    password_field.send_keys(password)
    password_field.send_keys(u'\ue007')

    try:
        not_now = browser.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        not_now.click()
        return True
    except:
        selenium_browser.close_browser()
        return False


def scrape_popup(number):
    browser = selenium_browser.get_browser()
    fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
    scroll = 0
    while scroll < (int(number) // 6) + 2:
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        scroll += 1
        time.sleep(WAIT_TIME_FOR_LIST_SCROLL)

    list_scrape = browser.find_elements_by_xpath("//div[@class='isgrP']//li")
    output = []
    for acc in list_scrape:
        output.append(acc.text.split('\n')[0])
    return output

def scrape_popup_likes(number):
    browser = selenium_browser.get_browser()
    fBody = browser.find_element_by_xpath("/html/body/div[5]/div/div[2]/div")
    scroll = 0
    output = []
    while scroll < (int(number) // 6) + 2:
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        scroll += 1
        print(scroll_status_bar(scroll, (int(number) // 6) + 2))
        time.sleep(WAIT_TIME_FOR_LIST_SCROLL)
        list_scrape = browser.find_elements_by_css_selector("body > div.RnEpo.Yx5HN > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div > div > div:nth-child(2) > div > div > a")
        for acc in list_scrape:
            if acc.get_attribute('title') not in output:
                output.append(acc.get_attribute('title'))
    return output

def scroll_status_bar(step, full):
    return ('>'*step + '.'*(full-step))

def scrape_for_followers_and_following(username):
    browser = selenium_browser.get_browser()
    browser.get(f'https://www.instagram.com/{username}')

    follow_number = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text

    browser.find_element_by_css_selector('ul > li:nth-child(2) > a').click()

    follow_list = scrape_popup(follow_number)

    button_close = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button')
    button_close.click()

    following_number = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text

    browser.find_element_by_css_selector('ul > li:nth-child(3) > a').click()

    following_list = scrape_popup(following_number)

    append_to_statistics(len(follow_list), len(following_list))
    return follow_list, following_list

def save_account_stats():
    browser = selenium_browser.get_browser()
    follow_number = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text
    following_number = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text
    append_to_statistics(int(follow_number), int(following_number))

def compare_for_unfollow(follow_list, following_list):
    people_to_unfollow = []
    for follow in following_list:
        if follow not in follow_list:
            people_to_unfollow.append(follow)
    return people_to_unfollow


def compare_with_keep_following(people_to_unfollow, KEEP_FOLLOWING):
    people_not_in_list = []
    for acc in people_to_unfollow:
        if acc not in KEEP_FOLLOWING:
            people_not_in_list.append(acc)
    return people_not_in_list


def follow_or_like_on_hashtag(hashtag, number_to_follow, with_likes=False, with_follow=True):
    browser = selenium_browser.get_browser()
    wait = WebDriverWait(browser, 5)
    counter = 0
    browser.get(f'https://www.instagram.com/explore/tags/{hashtag}')
    for _ in range(1):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
    pics = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, '#react-root > section > main > article > div:nth-child(3) > div > div > div > a')))
    pics[0].click()
    acc_followed_list = []
    acc_like_list = []
    while counter < number_to_follow:
        print(f'Counter: {counter + 1}/{number_to_follow}')
        try:
            acc_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                  'body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.e1e1d > h2 > a')))
            if with_follow:
                follow_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                           'body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.bY2yH > button')))

                if follow_button.text == 'Follow':
                    time.sleep(TIME_BETWEEN_FOLLOWS)
                    counter += 1
                    acc_followed_list.append(acc_name.text)
                    follow_button.click()
            if with_likes:
                time.sleep(TIME_BETWEEN_FOLLOWS)
                like_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                         'body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button')))
                like_button.click()
                if not with_follow:
                    acc_like_list.append(acc_name.text)
                    counter += 1
        except:
            pass

        skips = random.randint(0, 5)
        counter_skips = 0
        while counter_skips < skips and counter != number_to_follow:
            time.sleep(TIME_BETWEEN_FOLLOWS)
            right_arrow = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    'body > div._2dDPU.vCf6V > div.EfHg9 > div > div > a.HBoOv.coreSpriteRightPaginationArrow')))
            right_arrow.click()
            counter_skips += 1

        time.sleep(TIME_BETWEEN_FOLLOWS)
        right_arrow = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                 'body > div._2dDPU.vCf6V > div.EfHg9 > div > div > a.HBoOv.coreSpriteRightPaginationArrow')))
        right_arrow.click()

    if len(acc_followed_list) != 0:
        write_to_last_run(acc_followed_list)
    return acc_followed_list if len(acc_followed_list) != 0 else acc_like_list

def get_likes_from_photos(username, details=True):
    browser = selenium_browser.get_browser()
    wait = WebDriverWait(browser, 5)
    browser.get(f'https://www.instagram.com/{username}/')
    save_account_stats()
    num_posts = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
    for _ in range(int(num_posts)//6):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
    pics = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, '#react-root > section > main > div > div._2z6nI > article:nth-child(2) > div > div > div > div > a')))
    pics[0].click()
    photos_list = []
    like_list = []
    for i in range(len(pics)):
        button_likes = browser.find_elements_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.EDfFK.ygqzn > div > div.Nm9Fw > button')
        if len(button_likes) != 0:
            num_likes = button_likes[0].text
            num_likes = num_likes.split(' ')[0]
        elif len(button_likes) == 0:
            button_video_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.EDfFK.ygqzn > div > span')))
            button_video_likes.click()
            text_video_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.EDfFK.ygqzn > div > div > div.vJRqr')))
            num_likes = text_video_likes.text
            num_likes = int(num_likes.split(' ')[0]) - 1
            close_small_popup = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/div[1]')
            close_small_popup.click()

        print(f'Photo {i + 1}/{len(pics)} Likes: {int(num_likes) + 1}')
        if details and len(button_likes) != 0:
            num_likes = int(num_likes) + 3
            button_likes[0].click()
            like_list = scrape_popup_likes(num_likes)
            button_close = browser.find_element_by_xpath('/html/body/div[5]/div/div[1]/div/div[2]/button')
            button_close.click()
            photos_list.append(like_list)
        else:
            like_list.append(int(num_likes) + 1)
        if i != len(pics)-1:
            time.sleep(0.5)
            right_arrow = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                            'body > div._2dDPU.vCf6V > div.EfHg9 > div > div > a.HBoOv.coreSpriteRightPaginationArrow')))
                                                                                                                              
            right_arrow.click()
    if details:
        counter_dict = count_people(photos_list)
        counter_obj = Counter(counter_dict)
        graph_data_labels = []
        graph_data_values = []
        for tuple_value in counter_obj.most_common(20):
            graph_data_labels.append(tuple_value[0])
            graph_data_values.append(tuple_value[1])
        graph_data = []
        graph_data.append(graph_data_labels)
        graph_data.append(graph_data_values)

        return photos_list, pics, graph_data
    else:
        return pics, like_list

def display_photo(username, photo_number):
    browser = selenium_browser.get_browser()
    wait = WebDriverWait(browser, 5)
    browser.get(f'https://www.instagram.com/{username}/')
    num_posts = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
    for _ in range(int(num_posts)//6):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
    pics = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, '#react-root > section > main > div > div._2z6nI > article:nth-child(2) > div > div > div > div > a')))
    pics[photo_number].click()

def count_people(photos_likes_list):
    output = {}
    for photo_list in photos_likes_list:
        for like in photo_list:
            output[like] = output.get(like, 0) + 1
    return output