class Request():
    def __init__(self, src_id=0, dst_id=0, msg_type='',msg=''):
        self.src_id = src_id
        self.dst_id = dst_id
        self.msg_type = msg_type
        self.msg = msg
    def to_s(self):
        return "{},{},{},{}\n".format(self.src_id,self.dst_id,
                                         self.msg_type,self.msg)
