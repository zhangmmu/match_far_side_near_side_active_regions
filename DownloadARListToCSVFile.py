# download each file with the specified extension
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from FarSideAR import FarSideAR


def processOneTxtURL(txt_url, starting_line_num=7):
    far_side_ar_list = []
    if txt_url.endswith('.txt'):
        try:
            response = requests.get(txt_url)
            soup = BeautifulSoup(response.content, "html.parser")
            text = response.text
            lines = text.splitlines() # convert text file to list

            # if there is strong active region, then lines should be greater than 8
            if len(lines) > starting_line_num:
                print('File: ',txt_url,'is processing')
                timestamp = lines[0].strip()
                for line in lines[starting_line_num:]:
                    far_side_ar = FarSideAR(line, timestamp, txt_url)
                    far_side_ar_list.append(far_side_ar)

        except:
            print("exception")
    return far_side_ar_list

def processAllTxtURL(url, starting_line_num=7):
    all_far_side_arlist = []
    # make a request to the webpage and get its content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # find all the links on the webpage
    links = soup.find_all("a")
    #there are duplicate files in the website, the same file is under
    # http://jsoc.stanford.edu/data/farside/AR_Lists/ direcoty
    # and under http://jsoc.stanford.edu/data/farside/AR_Lists/{year} directory
    # load all .txt files first and skip duplicate file under second directory.
    for link in links:
        hrefText = link.text
        #Get all files ends with .txt, such as AR_LIST_2013.04.27_00:00:00.txt
        if hrefText.endswith('.txt'):
            #add file name to list
            #file_names.append(hrefText)
            file_url = os.path.join(url, hrefText)
            ar_list = processOneTxtURL(file_url, starting_line_num)
            if len(ar_list) > 0:
                for ar in ar_list:
                    all_far_side_arlist.append(ar)

    # collect data between 2010 and 2021, the href ends with / which needs to be trimed first
    for link in links:
        #sample link <a href="2015/">2015/</a>, get rid of ending /
        href = link.get("href")
        hrefText = href[:-1]

        if (len(hrefText) == 4) and (str.isdigit(hrefText)) and (int(hrefText) in range(2010,2023)):
            try:
                sub_url = url+href
                sub_response = requests.get(sub_url)
                sub_soup = BeautifulSoup(sub_response.content, "html.parser")
                sub_links = sub_soup.find_all("a")

                for sub_link in sub_links:
                    sub_hrefText = sub_link.text

                    file_url = os.path.join(sub_url, sub_hrefText)
                    ar_list = processOneTxtURL(file_url, starting_line_num)
                    if len(ar_list) > 0:
                        for ar in ar_list:
                            all_far_side_arlist.append(ar)
            except:
                continue

    return all_far_side_arlist


def main ():
    all_dataArray = []
    url = 'http://jsoc.stanford.edu/data/farside/AR_Lists/'
    all_data = processAllTxtURL(url, 7)

    keyStringArray = []

    #get data into array
    for data in all_data:
        #remove duplicate row
        key = data.designation + data.timestamp
        if key in keyStringArray:
            print("Duplicate key: ",key)
        else :
            all_dataArray.append(data.getURLDataArray())
            keyStringArray.append(key)


    df = pd.DataFrame(all_dataArray, columns=['designation', 'longitude', 'latitude', 'strength', 'eta at east limb', 'days from east limb','Timestamp','URL'])
    df.to_csv('far_side_active_region_JSOC.csv', index = False)

# Using the special variable
# __name__
if __name__=="__main__":
    main()