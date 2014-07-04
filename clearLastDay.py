import pymongo
for each in pymongo.Connection('localhost', 27017)['timeworker']['days'].find():
    if each['income'].day == 27:
        day_id = each['_id']
pymongo.Connection('localhost', 27017)['timeworker']['days'].remove({'_id': day_id})

for each in pymongo.Connection('localhost', 27017)['timeworker']['days'].find():
    print each
