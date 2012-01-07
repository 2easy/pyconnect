from proto_consts import INVALID

class Request():
    def __init__(self, src_id=0, dst_id=0, req_type=INVALID, msg=''):
        self.src_id   = int(src_id)
        self.dst_id   = int(dst_id)
        self.req_type = int(req_type)
        self.msg = msg
    def not_valid(self):
        if self.req_type == INVALID: return True
        else: return False
    def to_s(self):
        return "{},{},{},{}\n".format(self.src_id,self.dst_id,
                                      self.req_type,self.msg)
