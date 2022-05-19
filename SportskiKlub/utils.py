from pymongo import MongoClient
from bson.objectid import ObjectId
from SportskiKlub.models import Location, Term

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://jope:jope@clusteris2022.aqpnv.mongodb.net/ISDatabase?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    #from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our
    return client['ISDatabase']

dbname = get_database()

collection_names = {
    'coaches': dbname["coaches"],
    'users': dbname["users"],
    'locations': dbname['locations'],
    'groups': dbname['groups'],
    'terms': dbname['terms']
}

def get_locations_for_coach(coachId):
    _locations = []
    groups = collection_names['groups'].find({"coachId": coachId})

    for group in groups:
        location = get_location_for_group(group['locationId'])
        if not location in _locations:
            _locations.append(location)

    return _locations

def get_location_for_group(locationId):
    location = collection_names['locations'].find_one({"_id": locationId})

    new_location = {
        "locationId": str(locationId),
        "name": location['name'],
        "adress": location['adress']
    }

    return new_location

def get_terms_for_group(id):
    term = collection_names['terms'].find_one({"_id": id})
    new_term = {
            "termId": str(id),
            "day": term['day'],
            "time": term['time']
        }

    return new_term

def get_groups_for_coach(coachId):
    _groups = []
    groups = collection_names['groups'].find({"coachId": coachId})

    for g in groups:
        location = get_location_for_group(g['locationId'])
        term = get_terms_for_group(g['termId'])
        _groups.append({"name": g['name'],
                        "groupId": str(g['_id']),
                        "location": location,
                        "term": term})

    return _groups


def get_all_coaches_from_db():
    _coaches = []
    coaches = collection_names['coaches'].find()
    for coach in coaches:
        user = collection_names['users'].find_one({"_id": coach['userId']})

        groups = get_groups_for_coach(coach['_id'])
        locations = get_locations_for_coach(coach['_id'])

        _coaches.append({"coachId": str(coach['_id']),
                         "name": user['name'],
                         "surname": user['surname'],
                         "username": coach['username'],
                         "groups": groups,
                         "locations": locations})

    return _coaches

def get_all_locations_from_db():
    _locations = []
    locations = collection_names['locations'].find()
    for location in locations:
        new_location = Location(locationId=str(location['_id']), name=location['name'], adress=location['adress'])
        _locations.append(new_location)

    return _locations

def get_all_terms_from_db():
    _terms = []
    terms = collection_names['terms'].find()
    for term in terms:
        new_term = Term(termId=str(term['_id']), day=term['day'], time=term['time'])
        _terms.append(new_term)

    return _terms

def create_group(coachId, termId, locationId, name):
    if collection_names['groups'].find_one({"coachId": ObjectId(coachId), "termId": ObjectId(termId)}):
        return None
    else:
        id = ObjectId()
        new_group = {
            "_id": id,
            "coachId": ObjectId(coachId),
            "termId": ObjectId(termId),
            "locationId": ObjectId(locationId),
            "name": name
        }
        collection_names['groups'].insert_one(new_group)
        return id

def update_group(groupId, termId, locationId, name):
    if collection_names['groups'].find_one({"_id": ObjectId(groupId)}):
        group = collection_names['groups'].find_one({"_id": ObjectId(groupId)})
        filter = {'_id': ObjectId(groupId)}
        if(group['termId'] == ObjectId(termId) and group['locationId'] == ObjectId(locationId)):
            newvalues = {"$set": {"name": name}}
            collection_names['groups'].update_one(filter, newvalues)
            return True
        if(group['termId'] == ObjectId(termId)):
            if collection_names['groups'].find_one({'locationId': ObjectId(locationId), 'termId': group['termId']}):
                return False
            if collection_names['groups'].find_one({'coachId': group['coachId'], 'termId': group['termId']}):
                return False
        if(group['locationId'] == ObjectId(locationId)):
            if collection_names['groups'].find_one({'locationId': group['locationId'], 'termId': ObjectId(termId)}):
                return False
            if collection_names['groups'].find_one({'coachId': group['coachId'], 'locationId': group['locationId']}):
                return False
        if collection_names['groups'].find_one({'locationId': ObjectId(locationId), 'termId': ObjectId(termId)}):
            return False
        newvalues = {"$set": {"name": name,
                              "locationId": ObjectId(locationId),
                              "termId": ObjectId(termId)}}
        collection_names['groups'].update_one(filter, newvalues)
        return True
    return False

def delete_group(groupId):
    if collection_names['groups'].find_one({"_id": ObjectId(groupId)}):
        if collection_names['groups'].delete_one({"_id": ObjectId(groupId)}):
            return True
    return False