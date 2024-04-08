import pandas as pd
import cv2
import urllib
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from datetime import datetime, timedelta
import pandas as pd

def findNearSideAR(eta_at_east_limb, fs_cen_lon, fs_cen_lat, minX, minY, maxX, maxY):

    date_string = str(eta_at_east_limb)[0:10]
    fs_date = datetime.strptime(date_string, '%Y-%m-%d')

    for n in range(3):
        search_date = fs_date + timedelta(days=n)
        ns_date_rows = nearside_df[(nearside_df.year == search_date.year) & (nearside_df.month == search_date.month) & (nearside_df.day == search_date.day)]
        if len(ns_date_rows.index) > 0:
            for ns_index, ns_row in ns_date_rows.iterrows():

                ns_name = ns_row['noaa_ar_no']
                ns_lon = ns_row['carrington_longitude']
                ns_lat = ns_row['latitude']
                ns_fs_lon_diff = np.absolute(ns_lon - fs_cen_lon)
                ns_fs_lat_diff = np.absolute(ns_lat - fs_cen_lat)
                if ns_fs_lon_diff < 20 and ns_fs_lat_diff < 5 and \
                    ns_lon < maxX and ns_lon > minX and \
                    ns_lat < maxY and ns_lat > minY:
                    print('\n------------------- Match ------------',ns_name, ', [', ns_lon, ',', ns_lat, ']')
                    return ns_name, search_date, ns_lon, ns_lat
    return None, None, None, None

nearside_df = pd.read_csv ('Data/MU_noaa_ars_plages.csv');
farside_df = pd.read_csv ('Data/far_side_ar_all.csv');

#get the datasets that active regions are inside far side of the SUN
Three_days_farside_df = farside_df[((farside_df["days from east limb"] < 3.0) & (farside_df["days from east limb"] > 0.3))]

matched_data = []
not_matched_data = []

fs_diction = dict()
uniq_fs_ar = Three_days_farside_df.designation.unique()

for fs in uniq_fs_ar:
    fs_diction[fs] = dict()
    fs_diction[fs]['name'] = fs

    #get all rows in Three_days_farside_df
    one_fs_df = Three_days_farside_df[Three_days_farside_df['designation'] == fs]
    one_fs_df = one_fs_df.sort_values(by=['days from east limb'])
    one_fs_inside_fs_df = one_fs_df[one_fs_df['inside_far_side'] == 1]

    row = one_fs_df.iloc[0]
    if one_fs_inside_fs_df.empty is False:
        row = one_fs_inside_fs_df.iloc[0]

    timestamp_string = row['timestamp']
    cen_lon = row['cen_long']
    cen_lat = row['cen_lat']
    strength = row['strength']
    days_from_east_limb = row['days from east limb']
    eta_at_east_limb = row['eta at east limb']
    minX = row['minX']
    minY = row['minY']
    maxX = row['maxX']
    maxY = row['maxY']

    ns_name, search_date, ns_lon, ns_lat = findNearSideAR (eta_at_east_limb, cen_lon, cen_lat, minX, minY, maxX, maxY)
    if ns_name is not None:
        matched_data.append([fs, ns_name, timestamp_string, search_date, cen_lon, ns_lon, cen_lat, ns_lat, minX, minY, maxX, maxY, strength])
        print(fs,', ', eta_at_east_limb, ', ', days_from_east_limb, ', ', timestamp_string, ', ', strength, ', [',cen_lon, ', ', cen_lat, '],  [', minX, ', ', minY, ', ',  maxX, ', ', maxY, ']')


    else :
        not_matched_data.append([fs,timestamp_string, strength, cen_lon, cen_lat, minX, minY, maxX, maxY])

matched_df = pd.DataFrame(matched_data, columns=['fs_name', 'ns_name', 'fs_timestamp', 'ns_timestamp', 'fs_cen_lon', 'ns_cen_lon', 'fs_cen_lat', 'ns_cen_lat', 'minX', 'minY', 'maxX', 'maxY', 'strength'])
matched_df.to_csv('Data/matched_fs_ns_ar.csv', index = False)