#!/usr/bin/python
# -*- coding: cp1251 -*-

# timeworker.py


import pymongo
# import datetime

def getRecords(host, port, dbname):
    connection = pymongo.Connection(host, port)
    # connect to database
    db = connection[dbname]
    records = db['days']
    worker = db['worker']
##    for post in worker.find():
##        print 'Worker: ' + post['Worker']
##        print 'Tabel number: ' + str(post['Tabel number'])
##    for record in records.find():
##        print record
    return worker, records
    
def whatAboutToday(timeinfo, host, port, dbname):
    connection = pymongo.Connection(host, port)
    db = connection[dbname]
    records = db['days']
    # timeinfo = datetime.datetime(yyyy, mm, dd, hh, mm, ss, ms)
    exists = 0
    for day in records.find():
        if day['income'].day == timeinfo.day and day['income'].month == timeinfo.month:
            exists = 1
            day_id = day['_id']
        else:
            pass
    
    if exists == 0:
        # new day!
        new_record = {'income': timeinfo}
        new_record_id = records.insert(new_record)
        #getRecords('localhost', 27017, 'timeworker')
        return generatePage('Check-out was made!')
    else:
        # income was made
        this_day = records.find_one({"_id": day_id})
        if this_day.has_key('outcome') == False:
            records.update(this_day, {'$set': {'outcome': timeinfo}})
        else:
            pass
            #print 'outcome was made\n\n'
        #getRecords('localhost', 27017, 'timeworker')
        return generatePage('Check-out was made!')
    
# whatAboutToday(datetime.datetime.today(), 'localhost', 27017, 'timeworker')

def generatePage(some_message):
    text_months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', \
                  6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sen', 10: 'Oct', \
                  11: 'Nov', 12: 'Dec'}
    
    top = '<html><body bgcolor="#8e8e95">'
    toptable = u'<table cellspacing="1" border="0" width="250"> \
<tr width="500" align="center"> \
<td bgcolor="#b9b9b9">&nbsp;&nbsp;<b>Дата</b></td> \
<td bgcolor="#888888">&nbsp;&nbsp;<b>Приход</b></td> \
<td bgcolor="#888888">&nbsp;&nbsp;<b>Уход</b></td> \
</tr>'
    bottom = '</table>'
    
    worker, records = getRecords('localhost', 27017, 'timeworker')
    for post in worker.find():
        worker_rec = u'Сотрудник: <b>' + post['Worker'] + '</b><br>'
        worker_rec += u'Табельный номер: <b>' + str(post['Tabel number']) + '</b><br>'

    page = top + worker_rec + toptable
        
    for record in records.find():
        if record.has_key('income'):
            income = str(record['income'].hour).rjust(2, '0')+':'+ \
                     str(record['income'].minute).rjust(2, '0')
        else:
            income = '--:--'
        if record.has_key('outcome'):
            outcome = str(record['outcome'].hour).rjust(2, '0')+':'+ \
                     str(record['outcome'].minute).rjust(2, '0')
        else:
            outcome = '--:--'
        
        base = u'<tr align="center"> \
<td bgcolor="#e7e7e7">&nbsp;&nbsp;{0} {1}</td> \
<td bgcolor="#aaaaaa">&nbsp;&nbsp;{2}</td> \
<td bgcolor="#aaaaaa">&nbsp;&nbsp;{3}</td> \
</tr> '.format(record['income'].day, \
               text_months[record['income'].month].encode('utf-8'), \
               income, outcome)
        page += base

    page += bottom

    page += u'<br><br><font color=#DA0000>'+some_message+u'</font></body></html>'
    return page
