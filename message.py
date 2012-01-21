class MessageFormatInvalid(BaseException): pass
class MessageTypeInvalid(BaseException): pass

class Message(object):
    # define message types
    create,delete,login,logout,forward,ping,invalid = range(7)
    types = range(7)
    def __init__(self, src_id, dst_id, msg_type):
        self.__validate_header(src_id,dst_id,msg_type)
        self.src_id   = int(src_id)
        self.dst_id   = int(dst_id)
        self.msg_type = int(msg_type)
    def __validate_header(src_id,dst_id,msg_type):
        # validate UIDs
        try:
            int(src_id)
            int(dst_id)
        except ValueError:
            raise MessageFormatInvalid("Invalid UIDs")
        # validate message type
        try:
            msg_type = int(msg_type)
        except:
            raise MessageTypeInvalid("Invalid message type")
        if msg_type not in Message.types:
            raise MessageTypeInvalid("Invalid message type")

class CreateUserMessage(Message):
    def __init__(self):
        super(CreateUserMessage,self).__init__(0,0,Message.create)
