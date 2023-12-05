#One far side active region
class FarSideAR:

    def __init__ (self, data_string, timestamp, txt_url):
         # default split by white spaces
        dataList = data_string.split()
        if len(dataList) >= 6:
             #'designation', 'longitude', 'latitude', 'strength', 'eta at east limb', 'days from east limb','Timestamp'

            self.designation = dataList[0]
            self.center_long= dataList[1]
            self.center_lat = dataList[2]
            self.strength = dataList[3]
            self.eta_at_east_limb = dataList[4]
            self.days_from_east_limb = dataList[5]
            self.timestamp = timestamp
            self.txt_url = txt_url


    def getURLDataArray(self):
        return [self.designation, self.center_long, self.center_lat, \
                self.strength, self.eta_at_east_limb, self.days_from_east_limb, self.timestamp, self.txt_url]


    def getDataArray (self):
        return [self.designation, self.timestamp, self.center_long, self.center_lat, \
                self.minX, self.minY, self.maxX, self.maxY, \
                self.strength, self.eta_at_east_limb,\
                self.days_from_east_limb, self.center_blue, self.center_gree, self.center_red, self.txt_url]


    def setDesignation (self, designation):
        self.designation = designation


    def setcenter_long (self, center_long):
        self.center_long = center_long


    def setcenter_lat (self, center_lat):
        self.center_lat = center_lat


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


    def setCenterColor (self, color):
        if len(color) > 2:
            self.center_red = color[0]
            self.center_gree = color[1]
            self.center_blue = color[2]


    def setMinMaxXY (self, points):
        if len(points) > 3:
            self.minX = points[0]
            self.minY = points[1]
            self.maxX = points[2]
            self.maxY = points[3]


    #toString function for print
    def __str__(self):
        return f'designation: {self.designation}, center_long: {self.center_long}, center_lat: {self.center_lat}, \
                strength: {self.strength}, eta_at_east_limb: {self.eta_at_east_limb}, \
                days_from_east_limb:  {self.days_from_east_limb}, timestamp: {self.timestamp}, \
                txt_url: {self.txt_url}'



