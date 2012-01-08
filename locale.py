class General(object):
    success  = "Success"
    failure  = "Failure"
    user_id  = "User ID"
    password = "Password"
    user     = "User"
    error    = "Error"
    db_error = "Database error"
class Menu(General):
    menu         = "MENU"
    login        = "Login"
    logout       = "Logout"
    add_user     = "Add user"
    add_buddy    = "Add buddy"
    remove_buddy = "Remove buddy"
    create_user  = "Create user"
    send_msg     = "Send message"
    exit         = "Exit"
class AddAcc(General):
    your_acc_id_is = "Your account ID is"
class Rgst(General):
    rgst   = "Registration"
    succ   = "Registration successful :)"
    failed = "Registration failed, please don't try to break anything"
class Login(General):
    wrong_uid   = "Wrong User ID"
    succ_msg    = "Login succesful :)"
    failed_msg  = "Login failed (user id or password invalid)"
    invalid_uid = "Your User ID is invalid (must be integer)"
