# plog
**plog** (**pl**ane l**og**) is a tracking tool for aviation enthusiasts. It can be used to track things like spotted aircraft, flown aircraft or aircraft that one has been onboard.

## App features

#### Feature states:
- Implemented: ✅
- Work in progress: 🚧
- Not implemented yet: ❌

#### App features:
- The user is able to create an account, log in and log out. ✅
- The user can add, modify and remove their own posts. ✅
- The user can see other users' posts in the app. ✅
- The user can search and filter the posts using keywords. ✅
- The user can see statistics about their app usage as well as the posts they have added on the profile page. ✅
- The user can select aircraft models and categories from predefined options. ✅
- The user has the option to lift (like) other users' aircraft. ✅

## Install & run
**Please note that the app is only guaranteed to work on Python 3.10 and newer versions. Older versions may not work and are not supported as of now.**

In different operating systems, Python can have different names. In most cases, it is either `python3` or simply `python`, please check this for your own system before proceeding if you are not sure which command should be used. It is also worth keeping in mind that at least in older versions of MacOS, `python` can refer to Python 2 so `python3` must be used even if both commands exist. The same rules also apply to PIP.

*Optional:*
Create a new Python virtual environment:
```
$ python3 -m venv venv
```

*Optional:*
Enter the virtual environment:
```
$ source venv/bin/activate
```

Install the flask library:
```
$ pip3 install flask
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