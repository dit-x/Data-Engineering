#!/usr/bin/python3

# %%

"""
    This create plot the data fetched from twitter by 'get_live_tweets_and_sentiments.py'

"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background')
fig, axs = plt.subplots(1, 2)

#%%
# plt.subplots_adjust(hspace=0.3, wspace=0.3)

# path_data = os.getcwd() + '/data_T_B.csv'
# path_sentiment = os.getcwd() + '/sentiment.csv'

path_data = '/home/dit/Desktop/DiT/CS/Big-data-specialization/coursera-master/big-data-2/my_edition/twitter/data_T_B.csv'
path_sentiment = '/home/dit/Desktop/DiT/CS/Big-data-specialization/coursera-master/big-data-2/my_edition/twitter/sentiment.csv'

def animate(i):
    color = ['#3889f2','#e06d2b', 'black']
    fontsize = 10
    p1 = axs[0]
    p2 = axs[1]

    # get the file from it location
    data = pd.read_csv(path_data)
    x = data['x_value']
    y1 = data['trump']
    y2 = data['biden']

    p1.clear()
    p1.plot(x, y1, label='Trump', color=color[0])
    p1.plot(x, y2, label='Biden', color=color[1])
    p1.legend(loc='upper left')
    p1.set_title('Tweets frequency plot of Trump and Biden')


    sentiment = pd.read_csv(path_sentiment)
    sentiment = sentiment.T

    width = 0.25
    x = np.arange(len(sentiment))
    
    p2.clear()
    try:
        p2.bar(x - width/2, sentiment[0], label='Trump', width=width, edgecolor=color[2], color=color[0])
        p2.bar(x + width/2, sentiment[1], label='Biden', width=width, edgecolor=color[2], color=color[1])
        p2.set_title('Tweets sentiment for Trump and Biden')
        p2.set_xticks(x)
        p2.set_xticklabels(sentiment.index)
        
        for index, value in enumerate(sentiment[1]):
            p2.text(index, value, str(value), fontsize=fontsize)
        for index, value in enumerate(sentiment[0]):
            p2.text(index, value, str(value), fontsize=fontsize)
        p2.legend(loc='upper left')
    except:
        pass
   
ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()

#%%
# 