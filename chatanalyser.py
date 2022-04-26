# import pdb; pdb.set_trace()

import re
# from emoji import emojize

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

# import emoji
from collections import Counter
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import warnings
warnings.filterwarnings("ignore")


def get_chat(filepath):
    with open(filepath, mode='r',encoding='utf8')as f:
        data = f.readlines()
    dataset = data[1:]
    cleaned_data = []
    for line in dataset:
        date = line.split(',')[0]
        line2 = line[len(date):]
        time = line2.split('-')[0][2:]
        line3 = line2[len(time):].strip()
        name = line3.split(':')[0][4:]
        line4 = line3[len(name):]
        m1 = 6
        if len(name) > 6:
            m1 = len(name)
        message = line4[m1:]
        cleaned_data.append([date, time, name, message])
    df = pd.DataFrame(cleaned_data, columns=['Date', 'Time', 'Name', 'Message'])
    df['dtime'] = df.Date + " " + df.Time
    df['dtime'] = pd.to_datetime(df['dtime'], errors='coerce')
    df = df.dropna(subset = ['Date'])
    df.Time = df['dtime'].dt.time
    df.Date = df['dtime'].dt.date
    columns_to_drop = ['Mom Zah created group "The salt family..."', 'You were added','logging and free radicals.','Pepps (office) left','Lynne left','']
    for i in columns_to_drop:
        df.drop(df.loc[df['Name'] == i].index, inplace = True)        
    df.Name[df['Name'] == '🌸'] = 'Brenda'
    df.Name[df['Name'] == 'Sweet Bro'] = 'Rainer'
    df.Name[df['Name'] == 'Emmacs'] = 'Emma'
    df.Name[df['Name'] == 'Daa'] = 'Madhe'
    weeks = {0 : 'Monday',1 : 'Tuesday',2 : 'Wednesday',3 : 'Thursday',4 : 'Friday',5 : 'Saturday',6 : 'Sunday'}
    df['Day'] = df['dtime'].dt.weekday.map(weeks)
    df = df[['Date','Day','Time','Name','Message']]
    df['Day'] = df['Day'].astype('category')
    # Count no of letters in each message
    df['Letters'] = df['Message'].apply(lambda s : len(s))
    # Count number of words
    df['Words'] = df['Message'].apply(lambda x: len(x.split()))    
    URLPATTERN = r'(https?://S+)'
    df['Url_count'] = df['Message'].apply(lambda x: re.findall(URLPATTERN, x)).str.len()    
    MEDIAPATTERN = r'<media omitted>'
    df['Media_count'] = df['Message'].apply(lambda x: re.findall(MEDIAPATTERN, x)).str.len()
    return df

df = get_chat

def total_messages(df):
    total_messages = df.shape[0]
    return total_messages

def media_message(df):
    # Count media in chats
    # media = np.sum(df['Media_count'])
    media_messages = df[df['Message'] == '<Media omitted>'].shape[0]
    return media_messages


def links(df):
    links = np.sum(df['Url_count'])
    return links


def most_used_words(df):
    text = " ".join(review for review in df.Message)
    text = text.replace('Media omitted','')
    wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white').generate(text)

    plt.figure( figsize = (10,5))
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.axis('off')
    plt.savefig('static/images/wordcloud.png')
    return 'images/wordcloud.png'


# df.Time = [x.strip() for x in df.Time]
# Count links

# users =df.Name.unique()

# for i in range(len(users)):
#     req_df = df[df['Name'] == users[i]]
#     print(f'----> Stats of {users[i]} <----')
#     print('Total Messages Sent: ', req_df.shape[0])
#     words_per_message = (np.sum(req_df['Words']))/req_df.shape[0]
#     w_p_m = ("%.3f" % round(words_per_message,2))
#     print('Average words per message: ', w_p_m)
#     media = sum(req_df['Media_count'])
#     print('Total Media Messages sent: ', media)
#     links = sum(req_df['Url_count'])
#     print('Total Links sent: ', links)
#     print()
#     print('----------------------------------------------------------------------------------')


# day_unique = df.Day.unique()
# for i in range(len(day_unique)):
#     req_day = df[df['Day'] == day_unique[i]]
#     print(day_unique[i],' -> ', req_day.shape[0])
    
# plt.figure( figsize = (10,5))
# most_active = df['Name'].value_counts()
# m_a = most_active.head(13)
# bars = ['A', 'B', 'C', 'D', 'E', 'F', 'G','H', 'I','J','K','L']
# x_pos = np.arange(len(bars))
# m_a.plot.bar(rot = 80)
# plt.xlabel('Members', fontdict = {'fontsize': 14, 'fontweight': 10})
# plt.ylabel('No of Messages',fontdict = {'fontsize': 14, 'fontweight': 10})
# plt.title('Most Active Members of the group',fontdict = {'fontsize': 20, 'fontweight': 8})
# # plt.xticks(x_pos, bars)
# plt.show()
