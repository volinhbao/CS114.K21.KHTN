import pdb

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv
import time

from selenium.webdriver.support.wait import WebDriverWait


def write():
    with open('reviews.csv', mode='w') as csv_file:
        fieldnames = ['title', 'review', 'isPos']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows({'title': title, 'review': review, 'isPos': 1})

        reader = csv.DictReader(csv_file)
        row_count = sum(1 for row in reader)
        csv_file.close()
        return row_count


# 1.
# driver = webdriver.Chrome("./chromedriver")
#
# driver.get("https://www.imdb.com/title/tt7286456/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=10")

# # Enter username automatically
# txtUser = browser.find_element_by_id("email")
# txtUser.send_keys("tijolvep")
#
# # Enter password automatically
# txtPass = browser.find_element_by_id("pass")
# txtPass.send_keys("baovynehihi")
#
# # Submit form
# txtPass.send_keys(Keys.ENTER)
total_reviews = 0
# Click Load more to continue crawling
# browser.find_element_by_class_name("ipl-load-more__button").click()
# time.sleep(3)
# review_url = driver.current_url
# page = requests.get(review_url)
# soup = BeautifulSoup(page.content, "html.parser")
# all = soup.find(id="main")
#
# # Get the title of the movie
# all = soup.find(id="main")
# parent = all.find(class_="parent")
# name = parent.find(itemprop="name")
# url = name.find(itemprop="url")
# movie_title = url.get_text()
# print(movie_title)

# Get the review titles
# review_list = all.find(class_="lister-list")
# review_array = all.find(class_="lister-item mode-detail imdb-user-review collapsable")
# title_rev = review_array.select(".title")
# title = [t.get_text().replace("\n", "") for t in title_rev]
# # print(title)
# print(len(title))
# # Get the reviews
# # review_list = reviews.select(".lister-item mode-detail imdb-user-review collapsable")
# review_rev = review_array.select(".content .text")
# review = [r.get_text() for r in review_rev]
# # print(review)
# print(len(review))

# if (len(title) % 100 == 0):
#     total_reviews = write()
# if (total_reviews > 5356):
#     break
# Pause the browser in 5 seconds for display and close
# time.sleep(5)
titles = []
review = []
# while True:
#     try:
#         allReviewsDiv = driver.find_element_by_xpath("//div[@class='lister-list']")
#         allReviewsHTML = allReviewsDiv.get_attribute('innerHTML')
#         loadMoreButton = driver.find_element_by_xpath("//button[@class='ipl-load-more__button']")
#         for i in range(0,5):
#             loadMoreButton.click()
#             time.sleep(5)
#             continue
#         review_soup = BeautifulSoup(allReviewsHTML, 'html.parser')
#         review_containers = review_soup.find_all('div', class_='imdb-user-review')
#         # pdb.set_trace()
#         print('length: ', len(review_containers))
#         if(len(review_containers)>100):
#             break
#         for review_container in review_containers:
#             review_title = review_container.find('a', class_='title').text
#             review_rev = review_container.find('div', class_='content').text
#             # print(review_title)
#             titles.append(review_title)
#             review.append(review_rev)
#         time.sleep(2)
#
#     except Exception as e:
#         print(e)
#         break
# titles = wait(driver,5).until
# try:
#     allReviewsDiv = driver.find_element_by_xpath("//div[@class='lister-list']")
#     allReviewsHTML = allReviewsDiv.get_attribute('innerHTML')
#     loadMoreButton = driver.find_element_by_xpath("//button[@class='ipl-load-more__button']")
#     for i in range(0, 2):
#         loadMoreButton.click()
#         time.sleep(5)
#         continue
#     review_soup = BeautifulSoup(allReviewsHTML, 'html.parser')
#     review_containers = review_soup.find_all('div', class_='imdb-user-review')
#     print(review_containers)
#     # pdb.set_trace()
#     print('length: ', len(review_containers))
#     # if (len(review_containers) > 100):
#     #     break
#     for review_container in review_containers:
#         review_title = review_container.find('a', class_='title').text
#         review_rev = review_container.find('div', class_='content').text
#         # print(review_title)
#         titles.append(review_title)
#         review.append(review_rev)
#     time.sleep(2)
#
# except Exception as e:
#     print(e)

# driver.close()

URL = "https://www.imdb.com/title/tt7286456/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=10"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get(URL)
soup = BeautifulSoup(driver.page_source, 'html.parser')

while True:
    try:
        driver.find_element_by_css_selector("button#load-more-trigger").click()
        time.sleep(5)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ipl-load-more__load-indicator")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        containers = soup.find_all(class_='imdb-user-review')
        print("Reviews: ",len(containers))
    except Exception:
        break

for elem in soup.find_all(class_='imdb-user-review'):
    title = elem.find(class_='title').get_text(strip=True)
    rev = elem.find(class_='content').get_text(strip=True)
    titles.append(title)
    review.append(rev)

driver.quit()
print("title: ", len(titles))
print("review: ", len(review))
print(titles)
print(review)
# Make the dataframe
table_review = pd.DataFrame({
    "Title": titles,
    "Review": review,
})
print(table_review)
table_review.to_csv('imdb-reviews-dataset.csv',index=False)

# username = "tijolvep"
# *[ @ id = "main"] / section / div[2] / div[2] / div[1] / div[1] / div[1] / a
# //*[@id="main"]/section/div[2]/div[2]/div[50]/div[1]/div[1]/a
# //*[@id="main"]/section/div[2]/div[2]/div[49]/div[1]/div[1]
