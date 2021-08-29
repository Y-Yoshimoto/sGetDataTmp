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
//db.createCollection('sObjectColumns');