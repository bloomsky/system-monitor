import datetime
import time
from countActiveDevices import get_active_sky_devices


def check_abnormal_sky_devices(cur, session, date, ts):

    currSkyData = session.execute("""SELECT "Temperature", "Pressure", "Humidity", "UVIndex", "Voltage", "FWVersion1" FROM current_sky_data""")

    count_abnormal_temp = 0
    # abnormal_temp_list = []

    count_abnormal_press = 0
    # abnormal_press_list = []

    count_abnormal_humidity = 0
    # abnormal_humidity_list = []

    count_abnormal_uv = 0
    # abnormal_uv_list = []

    count_abnormal_volt = 0
    # abnormal_volt_list = []

    for data in currSkyData:
        if data['Temperature'] == 9999:
            count_abnormal_temp += 1
            # abnormal_temp_list.append(data['DeviceID'])
        if data['Pressure'] == 9999:
            count_abnormal_press += 1
            # abnormal_press_list.append(data['DeviceID'])
        if data['Humidity'] == 9999:
            count_abnormal_humidity += 1
            # abnormal_humidity_list.append(data['DeviceID'])
        if data['FWVersion1'] and not data['FWVersion1'].startswith('2') and data['UVIndex'] == 9999:
            count_abnormal_uv += 1
            # abnormal_uv_list.append(data['DeviceID'])
        if data['Voltage'] == 9999:
            count_abnormal_volt += 1
            # abnormal_volt_list.append(data['DeviceID'])

    # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ts = int(time.time())
    totalOnlineDevices = float(get_active_sky_devices(cur, session, date, ts))

    print "totalOnlineDevices : ", totalOnlineDevices

    abnormalRate_temperature = round(count_abnormal_temp/totalOnlineDevices,2)*100
    abnormalRate_pressure = round(count_abnormal_press/totalOnlineDevices,2)*100
    abnormalRate_humidity = round(count_abnormal_humidity/totalOnlineDevices,2)*100
    abnormalRate_uv = round(count_abnormal_uv/totalOnlineDevices,2)*100
    abnormalRate_volt = round(count_abnormal_volt/totalOnlineDevices,2)*100

    print "check abnormal sky device line 55 : ", abnormalRate_temperature, abnormalRate_pressure, abnormalRate_humidity, abnormalRate_uv, abnormalRate_volt

    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "Temperature", int(abnormalRate_temperature), count_abnormal_temp, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "Pressure", int(abnormalRate_pressure), count_abnormal_press, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "Humidity", int(abnormalRate_humidity), count_abnormal_humidity, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "Sky_UV", int(abnormalRate_uv), count_abnormal_uv, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "Sky_Voltage", int(abnormalRate_volt), count_abnormal_volt, ts))


def check_abnormal_storm_devices(cur, session, date, ts):

    currStormData = session.execute("""SELECT "RainDaily", "Rain", "UV", "Voltage", "WindDirection", "WindSpeed" FROM current_storm_data""")

    count_abnormal_raindaily = 0
    # abnormal_raindaily_list = []

    count_abnormal_windspeed = 0
    # abnormal_windspeed_list = []

    count_abnormal_rain = 0
    # abnormal_rain_list = []

    count_abnormal_uv = 0
    # abnormal_uv_list = []

    count_abnormal_volt = 0
    # abnormal_volt_list = []

    count_abnormal_direction = 0
    # abnormal_direction_list = []

    for data in currStormData:
        if data['RainDaily'] == 9999:
            count_abnormal_raindaily += 1
            # abnormal_raindaily_list.append(data['SkyDeviceID'])
        if data['WindSpeed'] == 9999:
            count_abnormal_windspeed += 1
            # abnormal_windspeed_list.append(data['SkyDeviceID'])
        if data['Rain'] == 9999:
            count_abnormal_rain += 1
            # abnormal_rain_list.append(data['SkyDeviceID'])
        if data['UV'] == 9999:
            count_abnormal_uv += 1
            # abnormal_uv_list.append(data['SkyDeviceID'])
        if data['Voltage'] == 9999:
            count_abnormal_volt += 1
            # abnormal_volt_list.append(data['SkyDeviceID'])
        if data['WindDirection'] == 9999:
            count_abnormal_direction += 1
            # abnormal_direction_list.append(data['SkyDeviceID'])

    # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ts = int(time.time())
    totalOnlineDevices = float(get_active_sky_devices(cur, session, date, ts))

    abnormalRate_raindaily = round(count_abnormal_raindaily/totalOnlineDevices,2)*100
    abnormalRate_rain = round(count_abnormal_rain/totalOnlineDevices,2)*100
    abnormalRate_windspeed = round(count_abnormal_windspeed/totalOnlineDevices,2)*100
    abnormalRate_uv = round(count_abnormal_uv/totalOnlineDevices,2)*100
    abnormalRate_volt = round(count_abnormal_volt/totalOnlineDevices,2)*100
    abnormalRate_direction = round(count_abnormal_direction/totalOnlineDevices,2)*100

    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "RainDaily", int(abnormalRate_raindaily), count_abnormal_raindaily, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "Rain", int(abnormalRate_rain), count_abnormal_rain, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "WindSpeed", int(abnormalRate_windspeed), count_abnormal_windspeed, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "Storm_UV", int(abnormalRate_uv), count_abnormal_uv, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "Storm_Voltage", int(abnormalRate_volt), count_abnormal_volt, ts))
    session.execute("""INSERT INTO abnormal_device_history ("Date","ErrorType","AbnormalRate","Count","TS") VALUES(%s,%s,%s,%s,%s)""", (date, "WindDirection", int(abnormalRate_direction), count_abnormal_direction, ts))
