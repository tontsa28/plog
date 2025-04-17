# plog
**plog** (**pl**ane l**og**) is a tracking tool for aviation enthusiasts. It can be used to track things like spotted aircraft, flown aircraft or aircraft that one has been onboard.

## App features

#### Feature states:
- Implemented: ✅
- Work in progress: 🚧
- Not implemented yet: ❌

#### App features:
- The user is able to create an account, log in and log out. ✅
- The user can add, modify and remove their own content. ✅
- The user can see user-added data in the app. ✅
- The user can sort, filter and search the aircraft in various ways (type, age, size etc.). ❌
- The user can see statistics about their app usage as well as the content they have added on the profile page. ❌
- The user can see the content they and others have added. ❌
- The user has the option to follow other users' aircraft lists. ❌

## Install & run
Install the flask library:
```
$ pip install flask
```

Create the database tables:
```
$ sqlite3 database.db < schema.sql
```

Insert predefined data into the database:
```
$ sqlite3 database.db < init.sql
```

Run the app:
```
$ flask run
```