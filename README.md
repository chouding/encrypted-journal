# My Encrypted Journal

A Python program that enables users to write and store journal posts locally through a custom JSON file format.
Acts similarly to a messaging platform, with ability for users to publish encrypted journal entries to a class server.

## How It's Made:

**Tech used:** Python, Sockets, Tkinter, PyNaCl, PathLib

The graphical user interface was entirely constructed using the Tkinter module, including the entire frontend and all event handlers.
User profiles were created using OOP principles and stored with a custom JSON file format.
Server connection functionalities were accomplished with sockets and pathlibs. Journal entries were encrypted using PyNaCl.

## Optimizations

-> Added settings menu and interface that enables user to change their username and password

## Lessons Learned:

This class project taught me a lot about corroborating different modules together into a singular, big project. In particular,
separating different concerns into their own modules, such as the handling the network protocol in its own module or
the user interface in its own module. I also learned about unit testing, or ensuring that every part of your code is valid.
In general, I learned many common coding practices such as making clear/concise comments, using proper
variable naming conventions, and abstracting code to make it less redundant.

## Instructions

- **main.py**: Use this file as the main module for your program.

-> Simply go to this file and run the code.

-> Create and name a DSU file locally on the top left button labeled "File".

-> Create a username and password for your profile on the top left button labeled "Settings".

-> Type and save posts with the given text box.

-> See all your posts on the left text box.

---
