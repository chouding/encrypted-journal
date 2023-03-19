# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.


import json, time
from collections import namedtuple
from Profile import Post, Profile


# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['typeError', 'error_message', 'token'])


def join(username:str, password:str, token:str = ''):
  """
  Converts username and password into specified join JSON format.
  """
  join_msg = {'join': {'username': username, 'password': password, 'token': token}}
  return json.dumps(join_msg)


def post(message:str, token:str):
  """
  Converts post into specified post JSON format.
  """
  post = Post(message)
  post_time = post.get_time()
  post_msg = {'token': token, 'post': {'entry': message, 'timestamp': str(post_time)}}
  return json.dumps(post_msg)


def bio(bio:str, token:str, time:str = None):
  """
  Converts bio into specified bio JSON format, if given.
  """
  if bio != None:
    bio_msg = {'token': token, 'bio': {'entry': bio, 'timestamp': time}}
    return json.dumps(bio_msg)
  return bio


def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object (ONLY for server responses).
  '''
  try:
    json_obj = json.loads(json_msg)
    typeError = json_obj['response']['type'] # grabs typeError from the json_obj
    error_message = json_obj['response']['message'] # grabs error_message from json_obj
    if 'token' in json_msg: 
      token = json_obj['response']['token'] # grabs token from json_obj
      return DataTuple(typeError, error_message, token) # returns DataTuple if of parameters typeError, error_message, and token
    return DataTuple(typeError, error_message, None)
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
