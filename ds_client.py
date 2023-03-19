import socket, ds_protocol, json
from Profile import Post, Profile
from NaClProfile import NaClProfile

PORT = 3021
SERVER = '168.235.86.101'


def checkWhiteSpace(message:str = None, bio:str = None):
  """
  Returns true if the post and/or bio are empty or have whitespace. Else, return false.
  """
  if message != None and len(message.split()) == 0:
    return True
  elif bio != None and len(bio.split()) == 0:
    return True
  return False


def connectServer(server: str, port:int):
  """
  Attempt to connect to ICS 32 Distributive server.
  """
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    return sock
  except:
    print("\nInvalid server and/or port, try again.")
    return None


def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''

  # Attempt to connect to server.
  connection = connectServer(server, port)
  if connection == None:
    return False

  # Checks if message/bio is empty or just has whitespace by returning false.
  if message != "" or message != '':
    if checkWhiteSpace(message=message) or checkWhiteSpace(bio=bio):
      return False

  # Send information to server and receive server response.
  try:
    send = connection.makefile('w')
    recv = connection.makefile('r')

    usr_profile = NaClProfile()
    usr_profile.generate_keypair()
    usr_public_key = usr_profile.public_key

    join_msg = ds_protocol.join(username, password, usr_public_key) # grabs username and password from ds_protocol
    send.write(join_msg + '\r\n') # attempts to join server
    send.flush()

    srv_msg = recv.readline()
    typeError, error_message, srv_token = ds_protocol.extract_json(srv_msg)
    print(error_message + '\n')

    if message != "": # check is message parameter is not None, else only pass in bio parameter 
      message = usr_profile.encrypt_entry(message, srv_token)
      post_msg = ds_protocol.post(message, usr_public_key)
      time = json.loads(post_msg)['post']['timestamp']
      bio_msg = ds_protocol.bio(bio, usr_public_key, time)
    elif message == "":
      bio_msg = ds_protocol.bio(bio, usr_public_key)

    joined = True
    while joined:
      if message != "": # writes message to server is message does not equal None
        send.write(post_msg + '\r\n') 
        send.flush()
      if bio != None: # writes bio to server if bio does not equal None
        send.write(bio_msg + '\r\n')
        send.flush()

      srv_msg = recv.readline()
      typeError, error_message, _ = ds_protocol.extract_json(srv_msg)
      print(error_message)
      joined = False

    connection.close() # closes connection
  except:
    connection.close()
    return False
  else:
    return True
