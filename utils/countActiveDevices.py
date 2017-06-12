import time
import datetime

def get_active_sky_devices(cur, session, date, ts):

    print "count active sky devices: line 9"

    cur.execute("select DeviceID from appi_skydevice")
    devices = cur.fetchall()

    print "Registered Devices Amount: ", len(devices)

    countRegisteredDevices = len(devices)

    #  get all sky devices which has current data stored in cassandra
    currSkyData = session.execute("SELECT \"DeviceID\", \"TS\", \"FWVersion1\" FROM current_sky_data")

    devicesWithData = []
    countCurrSkyDevices = 0

    # get all online devices that sends the data within latest one hour
    max = time.time() - 3600
    countOnlineAllDevices = 0
    countOfflineAllDevices = 0

    # declare the variables to count the online devices and offline devices of difference firm versions
    countOnlineVersion1x = 0
    countOnlineVersion15 = 0
    countOnlineVersion2x = 0

    countOfflineVersion1x = 0
    countOfflineVersion15 = 0
    countOfflineVersion2x = 0

    for item in currSkyData:
        countCurrSkyDevices += 1
        if item['TS'] >= max:
            countOnlineAllDevices += 1
            if item['FWVersion1'] and item['FWVersion1'].startswith('1.5'):
                countOnlineVersion15 += 1
            elif item['FWVersion1'] and item['FWVersion1'].startswith('2'):
                countOnlineVersion2x += 1
            else:
                countOnlineVersion1x += 1
        else:
            countOfflineAllDevices += 1
            if item['FWVersion1'] and item['FWVersion1'].startswith('1.5'):
                countOfflineVersion15 += 1
            elif item['FWVersion1'] and item['FWVersion1'].startswith('2'):
                countOfflineVersion2x += 1
            else:
                countOfflineVersion1x += 1

    print "Sky Devices With Data: ", countCurrSkyDevices

    # get all online devices that sends the data within latest one hour
    max = time.time() - 3600

    # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ts = int(time.time())

    onlineRateVersion1x = round(countOnlineVersion1x/float(countRegisteredDevices),2)*100
    onlineRateVersion15 = round(countOnlineVersion15/float(countRegisteredDevices),2)*100
    onlineRateVersion2x = round(countOnlineVersion2x/float(countRegisteredDevices),2)*100

    session.execute("""INSERT INTO device_status_history ("Date","DeviceType","OfflineCount","OnlineCount","OnlineRate","TS") VALUES(%s,%s,%s,%s,%s,%s)""", (date, "Sky1",countOfflineVersion1x, countOnlineVersion1x, int(onlineRateVersion1x), ts))
    session.execute("""INSERT INTO device_status_history ("Date","DeviceType","OfflineCount","OnlineCount","OnlineRate","TS") VALUES(%s,%s,%s,%s,%s,%s)""", (date, "Sky15",countOfflineVersion15, countOnlineVersion15, int(onlineRateVersion15), ts))
    session.execute("""INSERT INTO device_status_history ("Date","DeviceType","OfflineCount","OnlineCount","OnlineRate","TS") VALUES(%s,%s,%s,%s,%s,%s)""", (date, "Sky2",countOfflineVersion2x, countOnlineVersion2x, int(onlineRateVersion2x), ts))

    return countOnlineAllDevices


def get_active_storm_devices(cur, session, date, ts):

    cur.execute("select DeviceID1 from appi_stormdevice")
    devices = cur.fetchall()

    #  get all registered devices from mysql
    countRegisteredDevices = len(devices)

    print "Registered Sky Devices: ", countRegisteredDevices

    #  get all sky devices which has current data stored in cassandra
    currStormData = session.execute("SELECT \"DeviceID1\", \"TS\", \"VERSION1\" FROM current_storm_data")

    countCurrStormDevices = 0

    # get all online devices that sends the data within latest one hour
    max = time.time() - 3600
    countOnlineAllDevices = 0
    countOfflineAllDevices = 0

    for item in currStormData:
        countCurrStormDevices += 1
        if item['TS'] >= max:
            countOnlineAllDevices += 1
        else:
            countOfflineAllDevices += 1

    print "Storm Devices With Data: ", countCurrStormDevices

    # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ts = int(time.time())

    onlineRate = round(countOnlineAllDevices/float(countRegisteredDevices),2)*100

    session.execute("""INSERT INTO device_status_history ("Date","DeviceType","OfflineCount","OnlineCount","OnlineRate","TS") VALUES(%s,%s,%s,%s,%s,%s)""", (date, "Storm",countOfflineAllDevices, countOnlineAllDevices, int(onlineRate), ts))

    return countOnlineAllDevices
