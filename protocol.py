# server constants
PORT = 8888
SERVER_ID = 0
# client constants
#LOGGED_OUT = False
#LOGGED_IN = True
# message types
CREATE_USER = 0
DELETE_USER = 1
LOGIN       = 2
LOGOUT      = 3
FORWARD     = 4
EMPTY       = 8
INVALID     = 9
############################ MESSAGE FORMAT #############################
# AUTHOR                                                                #
# RECIPIENT                                                             #
# MESSAGE_TYPE                                                          #
# MESSAGE                                                               #
#                                                                       #
# Where                                                                 #
#     AUTHOR          is the source user id (or 0 for new user)         #
#     RECIPIENT       is the destination user id (0 for server)         #
#     MESSAGE_TYPE    is the message type. Possible values are:         #
#                         0 for CREATE_USER                             #
#                         1 for DELETE_USER                             #
#                         2 for LOGIN                                   #
#                         3 for LOGOUT                                  #
#                         4 for FORWARD                                 #
#     MESSAGE         is dependent on the type as follow:               #
#                         for 0,1,2:  PASSWORD                          #
#                         for 3:      OMMITED                           #
#                         for 4:      text                              #
#########################################################################
