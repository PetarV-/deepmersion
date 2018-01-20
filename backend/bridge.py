import numpy as np
# Linking functions to be accessed by the frontend

default_db = 'backend/db/'

class Bridge:
    def __init__(self, path_to_db=default_db):
        self.objs = np.load(path_to_db + 'objs_db.npy')
        self.plcs = np.load(path_to_db + 'plcs_db.npy')

    # obj_dist: distribution of objects (shape: (1000,))
    # plc_dist: distribution of places (shape: (401,))
    # chatter_level: level of chatter (0 <= chatter_level <= 1.0)
    # use_obj: whether to use objects
    # use_plc: whether to use places
    # use_chatter: whether to use chatter or normal mode
    # Returns: a vector of shape (10,) containing volume levels
    def get_sound(obj_dist, plc_dist, chatter_level=None, chause_obj=True, use_plc=True, use_chatter=True):
        return np.ones(10)

