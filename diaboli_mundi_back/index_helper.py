import pymongo


def create_index(url, unique=True):
    """ create index for mongodb"""
    mongo = pymongo.MongoClient(url)
    db = mongo.get_database()

    coll = "users"
    db[coll].create_index([("phone", pymongo.ASCENDING)], unique=True, background=True)
    print(f"{coll} index created")

    coll = "permissions"
    db[coll].create_index([("permission_url", pymongo.ASCENDING)], unique=True, background=True)
    print(f"{coll} index created")

    coll = "roles"
    db[coll].create_index([("title", pymongo.ASCENDING)], unique=True, background=True)
    print(f"{coll} index created")

    coll = "role_to_permission"
    db[coll].create_index([("title", pymongo.ASCENDING), ("permission_id", pymongo.ASCENDING)], unique=unique,
                          background=unique)
    print(f"{coll} index created")

    coll = "role_to_permission"
    db[coll].create_index([("role_id", pymongo.ASCENDING), ("permission_id", pymongo.ASCENDING)], unique=unique,
                          background=unique)
    print(f"{coll} index created")

    coll = "user_to_role"
    db[coll].create_index([("user_id", pymongo.ASCENDING), ("role_id", pymongo.ASCENDING)], unique=unique,
                          background=True)
    print(f"{coll} index created")


if __name__ == "__main__":
    uri = 'mongodb://127.0.0.1:27017/diaboli_mundi_back?auth213213Source=admin'
    create_index(uri)
