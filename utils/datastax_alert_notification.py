import urllib2, urllib,json, time
from email_cron_job import send_email
import requests

import ssl

def getUrl(path):

    # req = requests.post("https://54.193.105.210:8443/login",data={'username':'admin', 'password':'il0veweather'},verify=False)
    # print req.json()

    url = 'https://54.193.105.210:8443/%s' % path

    username = 'admin'
    password = 'il0veweather'
    p = urllib2.HTTPBasicAuthHandler()

    p.add_password(realm='RESTRICTED ACCESS',
                   uri='httpss://54.193.105.210:8443/%s' %path,
                   user='admin',
                   passwd='il0veweather')

    opener = urllib2.build_opener(p)
    urllib2.install_opener(opener)
    context = ssl._create_unverified_context()
    page = urllib2.urlopen(url,context=context).read()

    print json.loads(page)

    try:
        print "DataStax Alert Url: ", url
        # contents = urllib2.urlopen(url).read()
        context = ssl._create_unverified_context()
        contents = urllib2.urlopen(url,context=context).read()
        print "DataStax Alert Contents: ", contents
        return json.loads(contents)
    except Exception as e:
        print "Exception : ", str(e)
        return None

def getAlertInfo(alert, rule):
    if alert['node'] == '172.31.14.162':
        node = 'Cassandra 1'
    elif alert['node'] == '172.31.13.134':
        node = 'Solr'
    elif alert['node'] == '172.31.0.39':
        node = 'Cassandra 3'
    elif alert['node'] == '172.31.10.182':
        node = 'Cassandra 2'

    msg = "<h2>DataStax Alert Reporting......<h2>"
    if rule['type'] == 'rolling-avg' or rule['type'] == 'percentile':
        msg += "<h3>Alert Reason: %s on node %s exceeds the threshold(%.2f%%), current value is at %.2f%%</h3>" %\
                        (rule['metric'], node, rule['threshold'], alert['current_value'])
    elif rule['type'] == 'node-down':
        msg += "<h3>Alert Reason:Node %s is down</h3>" % alert['node']
    elif rule['type'] == 'agent-issue':
        msg += "<h3>Alert Reason: Agent Issue</h3>"


    datetime_str = time.strftime("%m/%d/%Y %H:%M:%S %Z",
                                 time.localtime(alert['first_fired']))
    msg += "Date: since %s" % datetime_str

    print msg

    receivers = ['sunwei@bloomsky.com']
    subject = 'DataStax Reports Alerts'
    for receiver in receivers:
        send_email(msg, receiver, subject)

def notification():
    fired_alerts = getUrl('BloomSky_Cluster/alerts/fired')
    print "fired_alerts : ", fired_alerts

    alert_rules = getUrl('BloomSky_Cluster/alert-rules')
    rules_map = dict((rule['id'], rule) for rule in alert_rules)

    for alert in fired_alerts:
        rule = rules_map.get(alert['alert_rule_id'])
        getAlertInfo(alert, rule)
