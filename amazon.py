from bs4 import BeautifulSoup
from selenium import webdriver
from pandas import DataFrame
import pandas as pd
import io
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re

chrome_options = Options()
chrome_options.set_headless(headless=False)
#browser = webdriver.Chrome(chrome_options=chrome_options)
browser = webdriver.Chrome(ChromeDriverManager().install())

comment_list = []
comment_title1 = []
au_list = []
comment_date = []
star_list = []
date_list = []
helpful_list = []
total_comments = 0
k = 0
i = 1
l=0
j=[]

while(True):
    temp_url = 'https://www.amazon.in/Mirah-Belle-Sanitizer-Approved-Children/product-reviews/B085NJSWPG/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent'
    url = temp_url + "&pageNumber=%d" % i
    i = i + 1
    print(i)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    comment_container = soup.findAll("span", {"class": "a-size-base review-text review-text-content"})
    comment_title = soup.findAll("a", {"class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"})
    author = soup.findAll("span", {"class": "a-profile-name"})
    date = soup.findAll("span", {"class": "a-size-base a-color-secondary review-date"})
    star = soup.findAll("i", {"data-hook": "review-star-rating"})
    helpful = soup.findAll("div", {"data-a-expander-name": "review_comment_expander"})

    if len(comment_container) == 0:
        break

    for help in helpful:
        help_d = help.get_text()
        if "found this helpful" in help_d:
            new = help_d.split(" ")
            helpful_list.append(new[0].strip())
            # help_d[:25]
            # re.findall(r'\d+', help_d)
        else:
            helpful_list.append('0')
        #print(help_d)

    for s in star:
        star_rating = s.get_text()
        star_list.append(star_rating)


    for comment in comment_container:
        k+=1
        j.append(k)
        note_comment = comment.get_text().replace('>', '')
        #print("%d "%k, note_comment)
        comment_list.append(note_comment.strip())

    for title in comment_title:
        t = title.get_text().replace('>', '')
        #print("%d "%k, note_comment)
        comment_title1.append(t.strip())

    for c in range(2,len(author)):
        l+=1
        note_author = author[c].get_text().replace('>', '')
        #print("%d "%l, note_author)
        au_list.append(note_author)
    for a in range(2, len(date)):
        date1 = date[a].get_text().replace('on ', '')
        #print(date1)
        date_list.append(date1)

    #browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[11]/span/div/ul/li[8]/a').click()
browser.quit()

df = pd.DataFrame({'Number':j,'Date':date_list, 'Author':au_list, 'Star':star_list, 'Title':comment_title1,'Comment':comment_list, 'helpful': helpful_list})
# print(df)
df.to_csv("mirah_sanitizer_1.csv", index=False)
