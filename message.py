class MessageFormatInvalid(BaseException): pass
class MessageTypeInvalid(BaseException): pass

class Message(object):
    # define message types
    create,delete,login,logout,ping,invalid,private = range(7)
    types = range(7)
    def __init__(self,msg_type,src_id=0,msg='',dst_id=0):
        self.__validate_header(msg_type,src_id,dst_id)
        self.msg_type = int(msg_type)
        self.src_id   = int(src_id)
        self.msg      = msg
        self.dst_id   = int(dst_id)
    def __validate_header(msg_type,src_id,dst_id):
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
    def __str__(self):
        return "{},{},{},{}\n".format(self.msg_type,self.src_id,
                                      self.msg,self.dst)
