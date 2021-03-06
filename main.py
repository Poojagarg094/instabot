#HOW WE GENERATE ACCESS TOKEN FOLLW LINK => https://docs.google.com/document/d/1U0UQ79uMTLvM3e6CJmudhyyfrNYPsesbAWEKsbcWJpE/edit#
#client_id = d9fcbf571bda4f9995162dfafc5d2433
#ENDPOINTS = IT is another word of URL. website is same for all . it is just last word changing for everyone like www.acadview/students or /instructor

#matplotlib for graphs


import requests   #pip install requests
import urllib      #pip install urlib

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

BASE_URL= 'https://api.instagram.com/v1/'    #same for all url endpoints
APP_ACCESS_TOKEN = "3508609960.d9fcbf5.ce341ac62fab4e6d9cef7c9f943f5a03"

# def self_info:
#     own_info = requests.get(BASE_URL + '/users/self/?access_token'   + ACCESS_TOKEN)
#     print own_info.json()

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()   #for print URL
    print user_info #it display user detail   # JSON response is similar to a dictionary that we used earlier and hence we can read data from it in a similar way that we used for the dictionary.

    #for display value according to us
    if user_info['meta']['code'] == 200:     #200 mean request accepted or no issue in any request
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

def get_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          return user_info['data'][0]['id']
      else:
          return None
  else:
      print 'Status code other than 200 received!'

def get_user_info(insta_username):
  user_id = get_user_id(insta_username)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      print 'Username: %s' % (user_info['data']['username'])
      print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
      print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
      print 'There is no data for this user!'
  else:
    print 'Status code other than 200 received!'

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            #for downloading image
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
    return None

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            #for downloading image
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return user_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
    return None

def like_a_post():
  media_id = get_own_post(insta_username)
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": APP_ACCESS_TOKEN}
  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()

  if post_a_like['meta']['code'] == 200:
      print 'Like was successful!'
  else:
      print 'Your like was unsuccessful. Try again!'




def like_a_post(insta_username):
  media_id = get_user_post()
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": APP_ACCESS_TOKEN}
  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()

  if post_a_like['meta']['code'] == 200:
      print 'Like was successful!'
  else:
      print 'Your like was unsuccessful. Try again!'

def post_a_comment(insta_username):
  media_id = get_user_post(insta_username)
  comment_text = raw_input("Your comment: ")
  payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
  request_url = (BASE_URL + 'media/%s/comments') % (media_id)
  print 'POST request url : %s' % (request_url)

  make_comment = requests.post(request_url, payload).json()

  if make_comment['meta']['code'] == 200:
      print "Successfully added a new comment!"
  else:
      print "Unable to add comment. Try again!"

def delete_negative_comment(insta_username):
  media_id = get_user_post(insta_username)
  request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  comment_info = requests.get(request_url).json()

  if comment_info['meta']['code'] == 200:
    if len(comment_info['data']):
        comment_text = comment_info['data'][0]['text']
        blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
        print blob.sentiment
          # code to delete a comment
    else:
        print 'There are no existing comments on the post!'
  else:
        print 'Status code other than 200 received!'


# self_info()
#get_user_info('angel12ab')   #it will show detail of angel12ab
#get_own_post()
# get_user_info('angel12ab')
#get_user_post('angel12ab')

#get_own_post()
#like_a_post('angel12ab')
#post_a_comment('angel12ab')
delete_negative_comment('angel12ab')