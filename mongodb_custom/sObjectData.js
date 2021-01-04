var user = {
    user: "sObjectDataAdmin",
    pwd: "Password01",
    roles: [
        {
            role: "dbOwner",
            db: "sObjectData"
        }
    ]
};
db.createUser(user);

//db.createCollection('Account');
//db.createCollection('Contact');
//db.createCollection('Event');
//db.createCollection('FeedComment');
//db.createCollection('FeedItem');
//db.createCollection('Lead');
//db.createCollection('LoginHistory');
//db.createCollection('Opportunity');
//db.createCollection('Task');
db.createCollection('sObjectColumns');