import pandas as pd
import urllib
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from datetime import datetime
from datetime import timedelta

def get_year(timeStamp_string):
    return int(timeStamp_string[0:4])

def getIndex (strength):
    if strength < 500:
        return 0
    elif strength >= 500 and  strength < 1000:
        return 1
    elif strength >= 1000 and  strength < 1500:
        return 2
    elif strength >= 1500 and  strength < 2000:
        return 3
    elif strength >= 2000 and  strength < 2500:
        return 4
    elif strength >= 2500 and  strength < 3000:
        return 5
    elif strength >= 3000 and  strength < 4000:
        return 6
    elif strength >= 4000 and  strength < 5000:
        return 7
    elif strength >= 5000:
        return 8

matched_farside_df = pd.read_csv ('Data/matched_fs_ns_ar.csv')
farside_df = pd.read_csv ('Data/far_side_active_region_JSOC.csv')
nearside_df = pd.read_csv('Data/MU_noaa_ars_plages.csv')

matched_farside_df['year'] = matched_farside_df['fs_timestamp'].apply(get_year)
farside_df['year'] = farside_df['Timestamp'].apply(get_year)

yearArray = []
yearMatchedFSCount = []
yearFSCount = []
yearNSCount = []

#find every year's unique active region count
for y in range (2010, 2024):
    yearArray.append(y)
    yearMatchedFSCount.append(matched_farside_df[matched_farside_df['year'] == y].shape[0])
    yearFSCount.append(len(farside_df[farside_df['year'] == y].designation.unique()))
    yearNSCount.append(len(nearside_df[nearside_df['year'] == y].noaa_ar_no.unique()))
print(yearNSCount)

#bar chart of active region counts by year
yeardf = pd.DataFrame({'Year':yearArray, 'Matched Far-Side AR Counts':yearMatchedFSCount, 'Far-Side AR Counts':yearFSCount, 'Near-Side AR Counts':yearNSCount })
yeardf.set_index('Year', inplace=True)
yeardf[['Matched Far-Side AR Counts', 'Far-Side AR Counts', 'Near-Side AR Counts']].plot.bar()


#pie chart of how many active regions reaching east limb
less_than_one_day = 0
more_than_one_day = 0
more_than_two_days = 0
more_than_three_days = 0

minvalue_fs_ar = farside_df.groupby("designation").min()
maxvalue_fs_ar = farside_df.groupby("designation").max().reset_index()

#Check min days from east limn to see how many far-side active regions reach east limb
#Anyalize how many didn't reach the east lime

more_than_three_days = minvalue_fs_ar[minvalue_fs_ar['days from east limb'] > 3.0].shape[0]
more_than_two_days = minvalue_fs_ar[(minvalue_fs_ar['days from east limb'] > 2.0) & (minvalue_fs_ar['days from east limb'] < 3.0)].shape[0]
more_than_one_day = minvalue_fs_ar[(minvalue_fs_ar['days from east limb'] > 1.0) & (minvalue_fs_ar['days from east limb'] < 2.0)].shape[0]
less_than_one_day = minvalue_fs_ar[minvalue_fs_ar['days from east limb'] < 1.0].shape[0]
total_ar = minvalue_fs_ar.shape[0]

labels = ['Died More Than 3 Days Before Reaching East Limb', 'Died 2 Days Before Reaching East Limb',
          'Died 3 Days Before Reaching East Limb', 'Reaching East Limb']

sizes = [more_than_three_days, more_than_two_days, more_than_one_day, less_than_one_day]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()

import matplotlib.pyplot as plt

#Check if only large max strength active regions can find match
matched_farside_name = matched_farside_df.fs_name.unique()
matched_strength_array = []
not_matched_strength_array = []

labels = ['<500', '500-1000', '1000-1500', '1500-2000', '2000-2500', '2500-3000', '3000-4000', '4000-5000', '>5000']
matched_max_str_counts = [0,0,0,0,0,0,0,0,0]
not_matched_strength_array = [0,0,0,0,0,0,0,0,0]

for fs_index, fs_row in maxvalue_fs_ar.iterrows():
    fs_name = fs_row['designation']
    strength = fs_row['strength']

    index = getIndex(strength)
    print(strength, ', ', index)
    if fs_name in matched_farside_name:
        matched_max_str_counts[index] = matched_max_str_counts[index] + 1
    else:
        not_matched_strength_array[index] = not_matched_strength_array[index] + 1

strengthdf = pd.DataFrame({'Strength':labels, 'Matched Far-Side AR Max Strength':matched_max_str_counts, 'Not Matched Far-Side Max Strength':not_matched_strength_array})
strengthdf.set_index('Strength', inplace=True)
strengthdf[['Matched Far-Side AR Max Strength', 'Not Matched Far-Side Max Strength']].plot.bar()
plt.show()

