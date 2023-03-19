# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin

import copy
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

from Profile import Post, Profile, DsuFileError, DsuProfileError
import json, time, os
from pathlib import Path
from NaClDSEncoder import NaClDSEncoder

class NaClProfile(Profile):
    def __init__(self):
        """
        From self.generate_keypair(self), generate these public class attributes:

        public_key:str
        private_key:str
        keypair:str
        """
        self_posts = []
        super().__init__()

    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

        :return: str    
        """
        encoder = NaClDSEncoder()
        encoder.generate()

        self.public_key = encoder.public_key
        self.private_key = encoder.private_key
        self.keypair = encoder.keypair

        return self.keypair

    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.
        """
        public_key, private_key, _ = keypair.split('=')
        self.public_key = public_key + '='
        self.private_key = private_key + '='

    def add_post(self, post_obj: Post) -> None:
        """
        Encrypts the entry of a post before adding it to a profile.
        """
        encoder = NaClDSEncoder()
        encoded_public_key = encoder.encode_public_key(self.public_key)
        encoded_private_key = encoder.encode_private_key(self.private_key)
        box = encoder.create_box(encoded_private_key, encoded_public_key)
        post_msg = post_obj.get_entry()
        encrypted_post_msg = encoder.encrypt_message(box, post_msg)
        post_obj.set_entry(encrypted_post_msg)

        super().add_post(post_obj)

    def get_posts(self) -> list[Post]:
        """
        Decrypts the entry of every post.
        """
        encoder = NaClDSEncoder()
        encoded_public_key = encoder.encode_public_key(self.public_key)
        encoded_private_key = encoder.encode_private_key(self.private_key)
        box = encoder.create_box(encoded_private_key, encoded_public_key)
        decrypted_posts = copy.deepcopy(self._posts)
        for idx, _post in enumerate(decrypted_posts):
            _post_msg = _post.get_entry()
            decrypted_post_msg = encoder.decrypt_message(box, _post_msg)
            _post.set_entry(decrypted_post_msg)
        return decrypted_posts
    
    def load_profile(self, path: str) -> None:
        """
        Loads a dsu file, taking into account the keys/keypairs and encrypting the entry of each post.
        """
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.public_key = obj['public_key']
                self.private_key = obj['private_key']
                self.keypair = obj['keypair']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.

        :return: bytes 
        """
        encoder = NaClDSEncoder()
        encoded_public_key = encoder.encode_public_key(public_key)
        encoded_private_key = encoder.encode_private_key(self.private_key)
        box = encoder.create_box(encoded_private_key, encoded_public_key)
        encrypted_entry = encoder.encrypt_message(box, entry)

        return encrypted_entry