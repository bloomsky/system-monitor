import time
from email.MIMEBase import MIMEBase
from email import Encoders
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.MIMEText import MIMEText
import email
import email.mime.application
import smtplib

def send_email(message, receiver, subject):
    sender = 'yangl@bloomsky.com'
    password = 'il0veweather'
    receivers = [receiver]
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receivers)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.add_header('Content-Type','text/html')
    msg.attach(MIMEText(message, 'html'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())
        server.quit()
        print "Successfully sent email"
    except:
        print "Error: unable to send email"



def send_alarm_email_to_staff(message):
    print message

    alarmName = ''
    if 'BloomskyEnvCPUUtilization' in message['AlarmName']:
        alarmName = 'Bloomsky-env CPU Utilization'
    elif 'DashboardCPUPercentageAlarm' in message['AlarmName']:
        alarmName = 'Dashboard CPU Utilization'
    elif 'BloomskyWorkerCPUUtilization' in message['AlarmName']:
        alarmName = 'Bloomsky-worker CPU Utilization'
    elif 'WUNCPUUtilization' in message['AlarmName']:
        alarmName = 'WUN CPU Utilization'
    elif 'MySQLCPUUtilization' in message['AlarmName']:
        alarmName = 'MySQL CPU Utilization'
    elif 'DashboardEnvironmentHealth' in message['AlarmName']:
        alarmName = 'Dashboard Environment Health'
    elif 'BloomskyWorkerEnvironmentHealth' in message['AlarmName']:
        alarmName = 'Bloomsky-worker Environment Health'
    elif 'BloomskyEnvEnvironmentHealth' in message['AlarmName']:
        alarmName = 'Bloomsky-env Environment Health'
    elif 'WUNEnvEnvironmentHealth' in message['AlarmName']:
        alarmName = 'WUN Environment Health'
    elif 'VideoWorkerEnvironmentHealth' in message['AlarmName']:
        alarmName = 'Video Worker Environment Health'
    elif 'MySQLStorageUsage' in message['AlarmName']:
        alarmName = 'MySQL Storage Usage'
    elif 'MySQLFreeableMemory' in message['AlarmName']:
        alarmName = 'MySQL Freeable Memory'


    alarmDescription = message['AlarmDescription']
    newStateReason   = message['NewStateReason']
    stateChangeTime  = message['StateChangeTime']
    newStateValue    = message['NewStateValue']
    oldStateValue    = message['OldStateValue']

    if alarmName is 'Dashboard Environment Health':
        newStateReason = 'Dashboard Environment health becomes Severe.'
    elif alarmName is 'Bloomsky-worker Environment Health':
        newStateReason = 'Bloomsky-worker Environment health becomes Severe.'
    elif alarmName is 'Bloomsky-env Environment Health':
        newStateReason = 'Bloomsky-env Environment health becomes Severe.'
    elif alarmName is 'WUN Environment Health':
        newStateReason = 'WUN Environment health becomes Severe.'

    print alarmName, type(alarmName)
    print alarmDescription, type(alarmDescription)
    print newStateReason, type(newStateReason)
    print stateChangeTime, type(stateChangeTime)

    content = """
        <html>
          <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                table, tr, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                tr, td {
                    text-align: left;
                    padding: 8px;
                }
            </style>
          </head>
          <body>
                <table>
                    <tr>
                        <td> Subject : </td>
                        <td> %s </td>
                    </tr>
                    <tr>
                        <td> Description : </td>
                        <td> %s </td>
                    </tr>
                    <tr>
                        <td> Reason : </td>
                        <td> %s </td>
                    </tr>
                    <tr>
                        <td> Date : </td>
                        <td> %s </td>
                    </tr>
                    <tr>
                        <td> Status Change: </td>
                        <td> %s  &nbsp ---->   &nbsp %s</td>
                    </tr>
                </table>
          </body>
        </html>
    """ % (alarmName, alarmDescription, newStateReason, stateChangeTime, oldStateValue, newStateValue)
    receivers = ['sunwei@bloomsky.com', 'yangl@bloomsky.com']
    subject = 'Server Monitor Alarm'
    for receiver in receivers:
        send_email(content, receiver, subject)




#Server disk and memory monitoring
import os
from collections import namedtuple
import psutil


def disk_partitions(disk_ntuple, all=False):
    """Return all mountd partitions as a nameduple.
    If all == False return phyisical partitions only.
    """
    phydevs = []
    f = open("/proc/filesystems", "r")
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())

    retlist = []
    f = open('/etc/mtab', "r")
    for line in f:
        if not all and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if device == 'none':
            device = ''
        ntuple = disk_ntuple(device, mountpoint, fstype)
        retlist.append(ntuple)
    return retlist


def disk_usage(usage_ntuple, path):
    """Return disk usage associated with path."""
    st = os.statvfs(path)
    free = (st.f_bavail * st.f_frsize)
    total = (st.f_blocks * st.f_frsize)
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    try:
        percent = ret = (float(used) / total) * 100
    except ZeroDivisionError:
        percent = 0
    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # http://goo.gl/sWGbH
    return usage_ntuple(total, used, free, round(percent, 1))


def memory_usage():
    s = psutil.virtual_memory()
    return s.percent


def server_disk_alert():
    disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
    usage_ntuple = namedtuple('usage',  'total used free percent')
    used_memory_percent = memory_usage()
    print "used_memory_percent : ", used_memory_percent
    for part in disk_partitions(disk_ntuple):
        usage = disk_usage(usage_ntuple, part.mountpoint)
        used_disk_percentage = usage.percent
        print "used_disk_percentage : ", used_disk_percentage
        if used_disk_percentage >= 80 or used_memory_percent >= 80:
            print "display usage"
            message = """
            <html>
              <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
              </head>
              <body>
                <p>
                   The used disk for worker server is %d percent<br><br>
                   The used memory for worker server is %d percent
                </p>
              </body>
            </html>
            """ % (used_disk_percentage, used_memory_percent)
            print "Here"
            receivers = ['sunwei@bloomsky.com', 'yangl@bloomsky.com']
            subject = 'Monitor Server status'
            for receiver in receivers:
                send_email(message, receiver, subject)
