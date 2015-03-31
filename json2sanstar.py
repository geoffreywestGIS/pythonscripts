import json
import jsonpickle
import requests
import arcpy
import numpy as np    #NOTE THIS
import datetime
from email.mime.text import MIMEText
import sys
import traceback
import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from datetime import timedelta
import time
import logging
import logging.handlers
import unittest




#
# smtp_handler = logging.handlers.SMTPHandler(mailhost=("smtp.gmail.com", 587),
#                                             fromaddr="geoffreywestgis@gmail.com",
#                                             toaddrs="geoffreywestgis@gmail.com",
#                                             subject=u"AppName error!")
#
#
# logger = logging.getLogger()
# logger.addHandler(smtp_handler)
# try:
#     break
# except exception as e:
#   logger.exception('Unhandled Exception')



start = time.time()
Start = datetime.datetime.now()
msgFolder = "C:/logs/"
sender = "geoffreywestgis@gmail.com"
recipient = "geoffreywestgis@gmail.com"


fc = "C:\MYLATesting.gdb\MYLA311"
if arcpy.Exists(fc):
    arcpy.Delete_management(fc)

arcpy.SetLogHistory(True)

f2 = open('C:\Users\Administrator\Desktop\DetailView.json', 'r')
data2 = jsonpickle.encode( jsonpickle.decode(f2.read()) )

url2 = "https://myla311.lacity.org/myla311router/mylasrbe/1/QuerySR"


headers2 = {'Content-type': 'text/plain', 'Accept': '/'}

r2 = requests.post(url2, data=data2, headers=headers2)
decoded2 = json.loads(r2.text)

Start = datetime.datetime.now()

# print Start

items = []
for sr in decoded2['Response']['ListOfServiceRequest']['ServiceRequest']:
    SRAddress = sr['SRAddress']
    Latitude = sr['Latitude']
    Longitude = sr['Longitude']
    SRNumber = sr['SRNumber']
    FirstName = sr['FirstName']
    LastName = sr['LastName']
    HomePhone = sr['HomePhone']
    CreatedDate = sr['CreatedDate']
    CreatedDate = datetime.datetime.strptime(CreatedDate, "%m/%d/%Y %H:%M:%S")



ItemInfo = " "


for ew in sr["ListOfLa311ElectronicWaste"][u"La311ElectronicWaste"]:
        CommodityType = ew['Type']
        ItemType = ew['ElectronicWestType']
        DriverFirstName = ew ['DriverFirstName']
        DriverLastName = ew ['DriverLastName']
        ItemCount = ew['ItemCount']
        ItemInfo += '{0},  {1}, '.format(ItemType, ItemCount)
        DriverName = DriverFirstName + ' ' + DriverLastName
        ParentNumber = ew['Name']


for GIS in sr["ListOfLa311GisLayer"][u"La311GisLayer"]:
        Day = GIS['Day']
        DistrictName = GIS['DistrictName']
        ShortDay = GIS['ShortDay']
        A_Call_No = GIS['A_Call_No']
        Area = GIS['Area']
        DirectionSuffix = GIS['DirectionSuffix']
        DistrictAbbr = GIS['DistrictAbbr']
        DistrictNumber = GIS['DistrictNumber']
        DistrictOffice = GIS['DistrictOffice']
        Fraction = GIS['Fraction']
        R_Call_No = GIS['R_Call_No']
        SectionId = GIS['SectionId']
        StreetFrom = GIS ['StreetFrom']
        StreetTo = GIS ['StreetTo']
        StreetLightId = GIS ['StreetLightId']
        StreetLightStatus = GIS['StreetLightStatus']
        Y_Call_No = GIS ['Y_Call_No']
        CommunityPlanningArea = GIS['CommunityPlanningArea']
        LastUpdatedBy = GIS['LastUpdatedBy']
        BOSRadioHolderName = GIS['BOSRadioHolderName']


comments = [ cl['Comment'] for cl in sr["ListOfLa311ServiceRequestNotes"][u"La311ServiceRequestNotes"]]
Comment = ' '.join(comments)





dt = np.dtype([('Address', 'U40'),
            ('LatitudeShape', '<f8'),
            ('LongitudeShape', '<f8'),
            ('Latitude', '<f8'),
            ('Longitude', '<f8'),
            ('Type', 'U40'),
            ('SRNumber', 'U40'),
            ('FirstName', 'U40'),
           ('LastName', 'U40'),
           ('HomePhone', 'U40'),
            ('CreatedDate', 'U128'),
           ('Comment', 'U128'),
            ('ItemInfo', 'U128'),
            ('DayTest', 'U128'),
            ('DistrictName', 'U128'),
            ('ShortDay', 'U128'),
            ('DriverName','U128'),
            ('ParentNumber', 'U128'),
            ('A_Call_No','U128'),
            ('Area', 'U128'),
            ('DirectionSuffix','U128'),
            ('DistrictAbbr', 'U128'),
            ('DistrictNumber', 'U128'),
            ('DistrictOffice', 'U128'),
            ('Fraction', 'U128'),
            ('R_Call_No', 'U128'),
            ('SectionId', 'U128'),
            ('StreetTo', 'U128'),
            ('StreetFrom', 'U128'),
            ('StreetLightId', 'U128'),
            ('StreetLightStatus', 'U128'),
            ('Y_Call_No', 'U128'),
            ('CommunityPlanningArea', 'U128'),
            ('LastUpdatedBy', 'U128'),
            ('BOSRadioHolderName', 'U128'),
            ])


items.append((SRAddress,
                      Latitude,
                     Longitude,
                      Latitude,
                      Longitude,
                      CommodityType,
                      SRNumber,
                     FirstName,
                      LastName,
                      HomePhone,
                      CreatedDate,
                      Comment,
                      ItemInfo,
                      Day,
                      DistrictName,
                      ShortDay,
                      DriverName,
                      ParentNumber,
                     A_Call_No,
                    Area,
                    DirectionSuffix,
                    DistrictAbbr,
                    DistrictNumber,
                    DistrictOffice,
                    Fraction,
                    R_Call_No,
                    SectionId,
                    StreetFrom,
                    StreetTo,
                    StreetLightId,
                    StreetLightStatus,
                    Y_Call_No,
                    CommunityPlanningArea,
                    LastUpdatedBy,
                    BOSRadioHolderName
))


arr = np.array(items,dtype=dt)
sr = arcpy.SpatialReference(4326)




NumPyArray = arcpy.da.NumPyArrayToFeatureClass(arr, fc, ['longitudeshape', 'latitudeshape'], sr)

i = 5
i2= 10

now_minus_5 = Start - datetime.timedelta(minutes =i)
now_plus_10 = Start + datetime.timedelta(minutes =i2)


def servicequery(CreatedDate, now_plus_10):
    if CreatedDate > now_plus_10:
        NumPyArray
    elif CreatedDate < now_plus_10:
          return "Blissful Intersection"
    else:
      print "X is now LESS than five!"

servicequery(CreatedDate, now_plus_10)

def servicequery2(CreatedDate, now_plus_10):
    if servicequery(CreatedDate, now_plus_10) == str("Blissful Intersection"):
         NumPyArray
    else:
        print "X is now LESS than five!"

servicequery2(CreatedDate, now_plus_10)

arcpy.AddField_management(fc, "Date", "DATE", '', 255)

field1 = "Date"

cursor = arcpy.UpdateCursor(fc)
for row in cursor:
    row.setValue(field1, row.getValue("CreatedDate"))
    cursor.updateRow(row)






while True:
        try:

            msgTxt = msgFolder+"resultMSG.txt"
            writeFile = open(msgTxt,"a")
            writeFile.write("service update is successful.\n" + str(Start))
            writeFile.write("\n")
            writeFile.write("service update is successful.\n")
            writeFile.write("\n")
            writeFile.close()
            del msgTxt

            ### Send Email Status Message
            txt = msgFolder+"resultMSG.txt"
            fp = open(txt,'rb')
            msg = MIMEText(fp.read())
            fp.close()

            msg['Subject'] = "3Di2SANSTAR Service Error"
            msg['From'] = "geoffreywestgis@gmail.com"
            msg['To'] = "geoffreywestgis@gmail.com"

            del txt

        except Exception:

            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n     " + str(sys.exc_type) + ": " + str(sys.exc_value) + "\n"
            msgs = "ARCPY ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            print msgs
            print pymsg
            print arcpy.GetMessages(1)


            msgTxt = msgFolder+"errorArcMSG.txt"
            writeFile = open(msgTxt,"w")
            writeFile.write("3Di2SANSTAR Service Error\n")
            writeFile.write("\n")
            writeFile.write("3Di2SANSTAR Service Error\n")
            writeFile.write(msgs+"\n")
            writeFile.write("\n")
            writeFile.write(pymsg+"\n")
            writeFile.write("\n")
            writeFile.write(arcpy.GetMessages(1))
            writeFile.close()


            fp = open(msgTxt,'rb')
            msg = MIMEText(fp.read())
            fp.close()

            msg['Subject'] = "claimsMap Script Error"
            msg['From'] = sender
            msg['To'] = recipient

            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login('geoffreywestgis@gmail.com', 'pythonheat1')
            server.sendmail(sender,recipient,msg.as_string())
            server.quit()

            print "Preparing to restart script due to processing error..."
            pass

        else:
            break
#
# print json.dumps(decoded2, sort_keys=True, indent=4)



print 'It took', time.time()-start, 'seconds.'
