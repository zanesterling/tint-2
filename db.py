from pymongo import MongoClient
import github

client = MongoClient()
db = client.tint

def hasUser(oauth_token=None, usern=None):
	if oauth_token:
		return db.users.find_one({'token': oauth_token}) is not None

	if usern:
		return db.users.find_one({'usern': usern}) is not None

	return False

# note: assumes user doesn't exist
def addUser(oauth_token):
	user = { 'token': oauth_token }

	# get user's usern from GitHub
	usern = github.Github(oauth_token).get_user().login
	user['usern'] = usern

	db.users.insert(user)
	return usern

def getUser(oauth_token):
	return db.users.find_one({'token': oauth_token})
