#One far side active region
class FarSideAR:

    def __init__ (self, data_string, timestamp, txt_url, image_url):
         # default split by white spaces
        dataList = data_string.split()
        if len(dataList) >= 6:
             #'designation', 'longitude', 'latitude', 'strength', 'eta at east limb', 'days from east limb','Timestamp'

            self.designation = dataList[0]
            self.cen_long= dataList[1]
            self.cen_lat = dataList[2]
            self.strength = dataList[3]
            self.eta_at_east_limb = dataList[4]
            self.days_from_east_limb = dataList[5]
            self.timestamp = timestamp
            self.txt_url = txt_url
            self.image_url = image_url
            self.inside_far_side = 0

    def getURLDataArray(self):
        return [self.designation, self.cen_long, self.cen_lat, \
                self.strength, self.eta_at_east_limb, self.days_from_east_limb, self.timestamp, self.txt_url]


    def getDataArray (self):
        return [self.designation, self.timestamp, self.cen_long, self.cen_lat, \
                self.minX, self.minY, self.maxX, self.maxY, \
                self.strength, self.eta_at_east_limb,\
                self.days_from_east_limb, self.cen_blue, self.cen_green, self.cen_red, \
                self.inside_far_side,
                self.txt_url, self.image_url]


    def setDesignation (self, designation):
        self.designation = designation


    def setcen_long (self, cen_long):
        self.cen_long = cen_long


    def setcen_lat (self, cen_lat):
        self.cen_lat = cen_lat


    def setstrength (self, strength):
        self.strength = strength


    def seteta_at_east_limb (self, eta_at_east_limb):
        self.eta_at_east_limb = eta_at_east_limb


    def setdays_from_east_limb (self, days_from_east_limb):
        self.days_from_east_limb = days_from_east_limb


    def settimestamp (self, timestamp):
        self.timestamp = timestamp


    def settxt_url (self, txt_url):
        self.txt_url = txt_url

    def setimage_url (self, image_url):
        self.image_url = image_url

    def setCenColor (self, color):
        if len(color) > 2:
            self.cen_red = color[0]
            self.cen_green = color[1]
            self.cen_blue = color[2]


    def setMinMaxXY (self, points):
        if len(points) > 3:
            self.minX = points[0]
            self.minY = points[1]
            self.maxX = points[2]
            self.maxY = points[3]

    def setInsideFarSide (self, inside_fs):
         self.inside_far_side = inside_fs

    #toString functione for print
    def __str__(self):
        return f'designation: {self.designation}, cen_long: {self.cen_long}, cen_lat: {self.cen_lat}, \
                strength: {self.strength}, eta_at_east_limb: {self.eta_at_east_limb}, \
                days_from_east_limb:  {self.days_from_east_limb}, timestamp: {self.timestamp}, \
                inside_far_side: {self.inside_far_side}, \
                txt_url: {self.txt_url}, image_url: {self.image_url}'



