var user = {
    user: "edituser",
    pwd: "Password01",
    roles: [
        {
            role: "dbOwner",
            db: "HistoryDB"
        }
    ]
};
db.createUser(user);
db.createCollection('sample');