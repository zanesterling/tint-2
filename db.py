from pymongo import MongoClient
import github

client = MongoClient()
db = client.tint

# returns user's usern if it exists
def hasUser(oauth_token=None, usern=None):
	if oauth_token:
		user = db.users.find_one({'token': oauth_token})
		if user is None:
			return False
		return user['usern']

	if usern:
		user = db.users.find_one({'usern': usern})
		if user is None:
			return False
		return user['usern']

	return False

# returns user's usern
# note: assumes user doesn't exist
def addUser(oauth_token):
	user = { 'token': oauth_token }

	# get user's usern from GitHub
	usern = github.Github(oauth_token).get_user().login
	user['usern'] = usern

	db.users.insert(user)
	return usern
