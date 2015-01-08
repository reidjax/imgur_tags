import requests
import json
import time

client_id = 'fdb6aa9e6ac6f76'

def get_top_gallery_tags():

	gallery = get_gallery()

	tags = {}
	for post in gallery:
		
		post_id = post['id']
		post_tags = get_post_tags(post_id)

		if post_tags not in (None, {}):
			tags[post_id] = post_tags

	grouped_tags = process_tags(tags)

	export_tags(grouped_tags)

def get_gallery():

	url = 'https://api.imgur.com/3/gallery/hot/viral/0.json'
	authentication = {'Authorization': 'Client-ID %s' % client_id}

	gallery = requests.get(url, headers = authentication)

	data = json.loads(gallery.text)

	gallery_items = data['data']

	return gallery_items

def get_post_tags(item_id):

	url = 'https://api.imgur.com/3/gallery/image/%s/tags' % item_id
	authentication = {'Authorization': 'Client-ID %s' % client_id}

	item_tags = requests.get(url, headers = authentication)

	data = json.loads(item_tags.text)
	
	try:
		tags = data['data']['tags']
		tag_storage = {}
		for tag in tags:
			tag_name = tag['name']
			tag_ups = tag['ups']
			tag_downs = tag['downs']
			tag_net = tag_ups - tag_downs
			tag_sum = tag_ups + tag_downs

			tag_storage[tag_name] = (tag_net, tag_sum, tag_ups, tag_downs)

		return tag_storage

	except KeyError:
		pass

def process_tags(gallery_tags):

	tags = {}

	for post_id in gallery_tags:
		for tag in gallery_tags[post_id]:
			if tag in tags:
				tags[tag] = tags[tag] + gallery_tags[post_id][tag][0]
			else:
				tags[tag] = gallery_tags[post_id][tag][0]

	return tags

def export_tags(processed_tags):
	name = 'tags_file'
	date = time.strftime('%m_%d_%Y')
	full_name = name + "_" + date

	tags_file = open(full_name, 'w')

	tags_file.write('tag \t')
	tags_file.write('net upvotes \n')

	for tag, upvote in processed_tags.items():
		tags_file.write(tag + '\t')
		tags_file.write(str(upvote) + '\n')

	tags_file.close()

### JFF
def get_profile(username):

	url = 'https://api.imgur.com/3/account/%s/gallery_profile.json' % username
	authentication = {'Authorization': 'Client-ID %s' % client_id}

	profile = requests.get(url, headers = authentication)

	data = json.loads(profile.text)

	return data

def get_account(username):
	url = 'https://api.imgur.com/3/account/%s' % username
	authentication = {'Authorization': 'Client-ID %s' % client_id}

	account = requests.get(url, headers = authentication)

	data = json.loads(account.text)

	return data

def get_image(image_id):

	url = 'https://api.imgur.com/3/image/%s' % image_id
	authentication = {'Authorization': 'Client-ID %s' % client_id}

	image = requests.get(url, headers = authentication)

	return image