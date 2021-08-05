import time
import re
import pandas
from selenium import webdriver
from datetime import date

driver = webdriver.Chrome()
# go to the website
driver.get("https://www.youtube.com/watch?v=7tmQSWuYwrI")

# write the part script with like, dislike and views (initial data) into the file, and search for it
p_id = driver.find_elements_by_tag_name("script")
for script in p_id:
    innerHTML= script.get_property('innerHTML')
    task=re.search('var ytInitialData = (.*)',innerHTML)
    if task is not None:
        # task_obj = json.loads(task.group(1)) #cannot work due to repeat {}
        with open("sample.json", "w", encoding = 'utf-8') as outfile:
            outfile.write(task.group(1))

with open('sample.json', "r", encoding = 'utf-8') as f:
    for line in f:
        like = re.findall('\d{2},\d{3} \u4eba\u559c\u6b61',line)[0]  #utf-8 code of 人喜歡
        dislike = re.findall('\d{3} \u4eba\u4e0d\u559c\u6b61',line)[0]  #utf-8 code of 人不喜歡
        view = re.findall('\u89c0\u770b\u6b21\u6578\uff1a\d{1},\d{3},\d{3}',line)[0]   # utf-8 code of 觀看次數:

#get the numeric part of the string
like = like[:6]
dislike = dislike[:3]
view = view[5:]

# scroll down the page to search for commentCounts(data rendered),
# 20000 may be not enough for some cases
js="var action=document.documentElement.scrollTop=20000"
driver.execute_script(js)
time.sleep(3)
c_id = driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string/span[1]')
comment = c_id.text
driver.close()

# write the data into the csv
today = date.today()
date =  today.strftime("%d/%m/%Y")
csv_file_name='data.csv'
current_df = pandas.read_csv(csv_file_name)

new_data = {'date':[date], 'views':view, 'likes':like, 'dislikes':dislike, 'comments':comment}
new_df = pandas.DataFrame(new_data)
# check the latest data (last row) to see if we need to update or add data
# ex: if shape is (4,5), then we need to check [3]['date']
is_today = current_df.iloc[current_df.shape[0]-1]['date'] == date
if is_today:
    # updating the column data, and save the new dataframe as new_df
    current_df.loc[current_df.shape[0]-1, 'views'] = view
    current_df.loc[current_df.shape[0]-1, 'likes'] = like
    current_df.loc[current_df.shape[0]-1, 'dislikes'] = dislike
    current_df.loc[current_df.shape[0]-1, 'comments'] = comment
    current_df.to_csv("data.csv", index=False)
    new_df = current_df
else:
    # adding the column data, and save the new dataframe as new_df
    new_df.to_csv(csv_file_name, mode = 'a', index = False, header = False)
    new_df = pandas.concat([current_df, new_df])











