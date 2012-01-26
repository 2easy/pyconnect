class General(object):
    alias    = 'Alias'
    success  = 'Success'
    failure  = 'Failure'
    user_id  = 'User ID'
    password = 'Password'
    user     = 'User'
    error    = 'Error'
    db_error = 'Database error'
    yes      = 'Yes'
    no       = 'No'
class Menu(General):
    menu         = 'MENU'
    login        = 'Login'
    logout       = 'Logout'
    add_user     = 'Add user'
    add_buddy    = 'Add buddy'
    remove_buddy = 'Remove buddy'
    create_user  = 'Create user'
    send_msg     = 'Send message'
    exit         = 'Exit'
class Account(General):
    new             = 'New Account'
    q_save          = 'Save contact?'
    q_remember_pass = 'Remember password?'
    your_acc_id_is  = 'Your account ID is'
class Create(General):
    create = 'Create new user'
    succ   = 'Registration successful :)'
    failed = 'Registration failed, please do not try to break anything'
class Login(General):
    wrong_uid   = 'Wrong User ID'
    succ    = 'Login succesful :)'
    failed  = 'Login failed (user id or password invalid)'
    invalid_uid = 'Your User ID is invalid (must be integer)'
