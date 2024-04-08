import pandas as pd
import cv2
import urllib
import numpy as np
import urllib.request
from FarSideAR import FarSideAR
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# The image we need is inside of AR_MAP image, we need the min/max x/y to crop image out.
# The method is when white space is < 50%, that means it's the main image.
def getCropImageBoudary():
    start_image_y = 0
    end_image_y = 0
    start_image_x = 0
    end_image_x = 0

    # there are 3 URLs for each data point, 1 text file, 1 composite map and 1 strong active region map
    strongARImageURL = 'http://jsoc.stanford.edu/data/farside/AR_Maps_JPEG/2015/AR_MAP_2015.01.17_12:00:00.png'
    req = urllib.request.urlopen(strongARImageURL)

    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'
    # Convert to RGB format
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # extract main image form original image
    image_size = img2.shape

    height = image_size[0]
    width = image_size[1]

    # Find first y that less than half are white, then find the first one more than half is white
    white_color_boolean_matrix = np.zeros((height,width), dtype=int)

    for y in range(height):
        for x in range(width):
            col = img2[y,x]
            # get all white color's x, y in matrix
            if (col[0] == 255 and col[1] == 255 and col[2] == 255):
                white_color_boolean_matrix[y][x] = 1


    white_color_count1 = white_color_boolean_matrix.sum(axis=0)
    # print(white_color_count1)
    # if first time less than half are white, value < 1/2 * height, enter the main image
    start_image_flag = False
    for index1 in range(len(white_color_count1)):
        if white_color_count1[index1] <  height/2:
            if start_image_flag == False:
                start_image_x = index1
                start_image_flag = True

        else:
            if start_image_flag == True:
                # The index is the white space, so minus 1
                end_image_x = index1-1
                break


    white_color_count2 = white_color_boolean_matrix.sum(axis=1)
    # print(white_color_count2)
    start_image_flag = False
    for index2 in range(len(white_color_count2)):
        if white_color_count2[index2] <  width/2:
            if start_image_flag == False:
                start_image_y = index2
                start_image_flag = True

        else:
            if start_image_flag == True:
                #The index is the white space, so minus 1
                end_image_y = index2-1
                break
    print(start_image_y, ' is start image y', end_image_y, ' is end_image_y')
    print(start_image_x, ' is start image x', end_image_x, ' is end_image_x')
    return (start_image_x, end_image_x, start_image_y, end_image_y)

def SameColor (color1, color2):
    return (color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2])

def isFarSide(color):
    if color[0] == 0 and color[1] == 0 and color[2] == 102:
        return 1
    else:
        return 0

#Not working due to the grid color
def isInsideFarSideRegion(resized_map, lat, lon):
    if resized_map is not None:
        height = resized_map.shape[0]
        width = resized_map.shape[1]
        isInsidefarSideRegion = 0

    if lat < 178 and lat > 1 and lon < 356:

        rightside_color1 = resized_map[lat + 90, lon + 1]
        rightside_color2 = resized_map[lat + 90, lon + 2]
        rightside_color3 = resized_map[lat + 90, lon + 3]

        if isFarSide(rightside_color1) or isFarSide(rightside_color2) or isFarSide(rightside_color3):
            isInsidefarSideRegion = 1

        if isInsidefarSideRegion == 0:
            rightside_color4 = resized_map[lat + 90 -1 , lon + 1]
            rightside_color5 = resized_map[lat + 90,     lon + 1]
            rightside_color6 = resized_map[lat + 90 + 1, lon + 1]
            if isFarSide(rightside_color4) or isFarSide(rightside_color5) or isFarSide(rightside_color6):
                isInsidefarSideRegion = 1
    return isInsidefarSideRegion

# Return the iamge we will process by cropping out the AR_MAP image
def cropImage(strongARImageURL, mainImageMinMaxXY):

    start_image_x = mainImageMinMaxXY[0]
    end_image_x = mainImageMinMaxXY[1]
    start_image_y = mainImageMinMaxXY[2]
    end_image_y = mainImageMinMaxXY[3]

    # old version, use urllib.request.urlopen(strongARImageURL)
    # not all txt file has png file
    try:
        req = urllib.request.urlopen(strongARImageURL)

        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        # Convert to RGB format
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Crop the image, remove added border
        map_image = img2[start_image_y+1: end_image_y-1, start_image_x+1: end_image_x-1]

        # resize image form (560, 280) to (360,180)
        resized_map = cv2.resize(map_image, (360,180))

        return resized_map
    except:
        print("An exception occurred when loading image: ", strongARImageURL)
        return None

# Main function to process all images and save into a csv file.
#
def procesImage(strongARImageURL, mainImageMinMaxXY, fs_name, cenLon, cenLat):

    # Store all active region data in a dictionary
    FS_Centroid = None

    resized_map = cropImage(strongARImageURL,mainImageMinMaxXY)

    if resized_map is not None:

        FS_Centroid = {}
        cenLon = int(float(cenLon))
        # The map longtitude starts form 180, so convert to current longtitude
        cenLat = 90 - int(float(cenLat))

        if cenLat >= 180:
            cenLat = 179
        if cenLon >= 360:
            cenLon = 359
        cenColor = resized_map[cenLat, cenLon]

        FS_Centroid[fs_name] = {'Centroid':(cenLat, cenLon), 'Color': cenColor, 'Location': [], 'Inside_Far_Side': 0}
        height = resized_map.shape[0]
        width = resized_map.shape[1]

        for y in range(height):
            for x in range(width):
                col = resized_map[y,x]
                # if col[0] == 255 or col[0] == 187 or col[0] == 242 :

                # Find color in resized_map
                for fs in FS_Centroid:
                    color = FS_Centroid[fs]['Color']

                    if SameColor(color, col):
                        FS_Centroid[fs]['Location'].append([y, x])

        # Crop the color block
        for fs in FS_Centroid:
            location = FS_Centroid[fs]['Location']
            insideFS = 0

            if len(location) > 0:
                minX = 360
                maxX = 0
                minY = 180
                maxY = 0

                for i in range(len(location)):
                    x = location[i][1]
                    y = location[i][0]

                    if x < minX:
                        minX = x

                    #sometimes, one active region can be divided into two by the far side line
                    if x > maxX and x < minX + 100:
                        maxX = x

                    if y < minY:
                        minY = y
                    if y > maxY:
                        maxY = y

            #check if it touches the east limb by compare color with far side background color [0,0,102]



            if maxX < 353 and cenLat < 172:

                newLat = cenLat
                newLon = maxX + 1

                #avoid the grid color [122, 0, 127]
                for i in range (3):
                    newcolor = resized_map[newLat, newLon]
                    if newcolor[0] == 122 and newcolor[1] == 0 and newcolor[1] == 127:
                        newLat = newLat + 1
                        newLon = newLon + 1

                rightside_color1 = resized_map[newLat, newLon]
                rightside_color2 = resized_map[newLat, newLon + 1]
                rightside_color3 = resized_map[newLat, newLon + 2]

                if isFarSide(rightside_color1) or isFarSide(rightside_color2) or isFarSide(rightside_color3):
                    insideFS = 1


         #       if maxX < 356:
         #           for index in range(maxY-minY):
         #               locationY = minY + index
         #               rightside_color1 = resized_map[locationY, maxX+1]
         #               rightside_color2 = resized_map[locationY, maxX+2]
         #               rightside_color3 = resized_map[locationY, maxX+3]

         #               if SameColor(rightside_color1, [0, 0, 102]) or SameColor(rightside_color2, [0, 0, 102]) or SameColor(rightside_color3, [0, 0, 102]):
         #                   FS_Centroid[fs]['Inside_Far_Side'].append(1)
         #               else:
         #                   FS_Centroid[fs]['Inside_Far_Side'].append(0)

                #convert back to -90 to 90 latitude
            newMinY = 90-(maxY+1)
            newMaxY = 90-(minY-1)
            #print(minX -1, 90 -(minY -1), maxX +1, maxY +1, newMinY, newMaxY)
            FS_Centroid[fs]['border'] = [minX -1, newMinY, maxX +1, newMaxY]
            print(FS_Centroid[fs]['border'], ', Inside Far Side: ', insideFS)
            FS_Centroid[fs]['Inside_Far_Side'] = insideFS
    return FS_Centroid

# Defining main function
def main():
    # get the mainImage min/max x/y
    mainImageMinMaxXY = getCropImageBoudary()
    print(mainImageMinMaxXY)

    ## Load csv files to get all txt url first
    # There are way too many files
    df = pd.read_csv ('Data/far_side_active_region_JSOC.csv')
    all_txt_urls = df['URL'].unique()

    # Too many images to process, save one year to one file
    years = range(2010, 2024)
    for year in years:

        output_file_name = 'Data/far_side_ar_'+ str(year) + '.csv'
        # get all unique text URLs
        #resultdf = pd.DataFrame()
        year_array = []
        sub_string = 'AR_LIST_' + str(year)
        for txtURL in all_txt_urls:

            if sub_string in txtURL:
                #get all rows from dataframe with the same URL
                one_image_data = df.loc[df['URL'] == txtURL]

                strongARImageURL = txtURL.replace('AR_Lists', 'AR_Maps_JPEG').replace('AR_LIST', 'AR_MAP').replace('.txt', '.png')
                print(strongARImageURL)
                for index, row in one_image_data.iterrows():
                    fs_name = row['designation']
                    cen_lon = row['longitude']
                    cen_lat = row['latitude']

                    FS_Centroid = procesImage(strongARImageURL, mainImageMinMaxXY, fs_name, cen_lon, cen_lat)

                    if FS_Centroid is not None:
                        far_side_ar = FarSideAR('', row['Timestamp'], txtURL, strongARImageURL)
                        far_side_ar.setDesignation(fs_name)
                        far_side_ar.setcen_long(cen_lon)
                        far_side_ar.setcen_lat(cen_lat)
                        far_side_ar.setstrength(str(row['strength']))
                        far_side_ar.seteta_at_east_limb(row['eta at east limb'])
                        far_side_ar.setdays_from_east_limb(row['days from east limb'])
                        far_side_ar.settimestamp(row['Timestamp'])
                        far_side_ar.settxt_url(txtURL)
                        far_side_ar.setimage_url(strongARImageURL)

                        #set centroid color
                        far_side_ar.setInsideFarSide(FS_Centroid[fs_name]['Inside_Far_Side'])
                        far_side_ar.setCenColor(FS_Centroid[fs_name]['Color'])
                        far_side_ar.setMinMaxXY(FS_Centroid[fs_name]['border'])

                        year_array.append(far_side_ar.getDataArray())
                        print(far_side_ar)


        dataframe = pd.DataFrame(year_array, columns=['designation', 'timestamp', 'cen_long', 'cen_lat',
                                               'minX', 'minY', 'maxX', 'maxY', 'strength', 'eta at east limb',
                                               'days from east limb', 'cen_red','cen_green', 'cen_blue',
                                               'inside_far_side','txt_url', 'image_url'])
        dataframe.to_csv(output_file_name, index = False)

# Using the special variable
# __name__
if __name__=="__main__":

    #Process strong active region images and save to Data/far_side_ar_year.csv file
    main()

    #combine all csv files into one
    begin_year = 2010
    end_year = 2024
    years = range(begin_year, end_year)
    file_names = []

    for year in years:
        file_names.append('Data/far_side_ar_' + str(year) + '.csv')

    #combine all csv files into one csv file
    df = pd.concat((pd.read_csv(file_name) for file_name in file_names))
    df.to_csv('Data/far_side_ar_all.csv', index = False)







