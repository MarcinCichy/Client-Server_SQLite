# Client/Server application - PostgreSQL version.

![Main application interface](screenshots/CS_help_scr.png "Main interface")

It is a simple Client/Server application.
The app uses JSON to send commands and server responses.

   **Note:** In this version, only one user can connect to the server at a time.

## Overview
On the user side, a graphical user interface based on the Curses module was created, which simulates the behavior of old terminals.

The user must log in to use the connection. The server checks if the user exists in the database and if he is not locked out. 
If these conditions are met, the user is logged in. As you enter your password, it is masked with asterisks.


## User Functionality
From the GUI, a logged-in user can:
 * check the contents of his mailbox, 
 * read the message, 
 * delete the message,
 * send the message to another user.

**Message Rules:**

* There can be a maximum of 5 messages in the inbox. 
* If someone sends a message and it turns out that the recipient's inbox is full, 
    they will receive a message about it and the message will not be sent.

* When writing a message: 
  * the number of characters that have already been used is shown on the fly. 
  * The message cannot be longer than 250 characters. After reaching this value, it is not possible to continue writing messages.
    Then shorten the message to the required number of characters.
  * When editing a message, you can navigate through its content and use the LEFT/RIGHT cursor keys to use the BACKSPACE and DELETE keys.

**Administratrator Functionality:**

If the User has administrator rights, she/he can also:
* create a new account, 
* delete an existing one, 
* change the status of another user (active or blocked), 
* she/he can also change user rights (admin or user).

### Below is a complete list of commands that can be used depending on your permissions (admin/user).

**The command to us as an administrator:**

  *stop* - stops both the server and the client

  *user-add* - create an account

  *user-show* - shows the list of existing accounts

  *user-del [username]* - deletes the selected account

  *user-perm [username] [permission]* - change permissions [user] or [admin]

  *user-stat [username] [status]* - change user status [active] or [banned]

  *user-info [username]* - to show information about account of selected user

  *user-pass* - to change password




**Commands available to both users and administrators:**

  *uptime* - returns the server's live time

  *info* -  returns the version number of the server and the date it was created

  *help* - returns the list of available commands with short description

  *logout* - to log out the User

  *clear* - to clear the screen

  *msg-list* - to show content of inbox

  *msg-del [number of message]* - to delete selected message

  *msg-snd* - to create and send message

  *msg-show [number of message]* - to show details of message (from, date, content)


## Database Engine Options


Before starting, You should choose the database engine. 

In file database.ini you can choose between PostgreSQL and SQLite.
If you choose PostgreSQL, you must have a database and user created.

If you choose SQLite, you must have a database file created by build_SQLIite_db.py. 

After that, you can move data from PostgreSQL to SQLite, by using move_data_to_SQLite.py.
    
## Runing the application
**Start the server:**
  Run server.py 

**Start the Clent GUI:**
  Run main_gui.py.

**The Login Credentials:**  
  For testing only: 
* username = marcin
* password = 12345


## Version History
       

  - v 0.3.0 Added possibility to change database engine PostgreSQL to SQLite
  - v 0.2.2 Added possibility to change password
  - v 0.2.1 Added password hashing and salting
  - v 0.2.0 Added support for PostgreSQL databases. Bye, bye JSON format database ;)

  - v 0.1.8 Improved command handling after server connection is lost and re-established
            New functionality added - user-info, to show information 
            about account of selected user

  - v 0.1.7 Implementation of message management
             - show list of messages in box
             - deleting a message
             - writing a message
             - sending a message
             - show selected message

  - v 0.1.6 Implementation of user management
            - creating a new account (new user)
            - deleting account
            - change permissions
            - change user status, active or banned

  - v 0.1.5 Next GUI implementation:
          - added log out command to menu
          - added clear command to menu
          - some fixes in GUI after log out

  - v 0.1.4 Next GUI implementation:
          - added log out command to menu
          - added clear command to menu
          - some fixes in GUI after log out

  - v 0.1.3 Next GUI implementation:
          - added login window

  - v 0.1.2 Next GUI implementation:
          - added login window

  - v 0.1.1 First GUI implementation (Curses)

  - V 0.1.0 First init version with basic commends:
          - uptime - returns the server's live time,
          - info - returns the version number of the server and the date it was created,
          - help - returns the list of available commands with short description,
          - stop - stops both the server and the client


