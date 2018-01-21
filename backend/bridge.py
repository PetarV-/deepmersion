import numpy as np
from scipy.stats import entropy

# Linking functions to be accessed by the frontend

default_db = 'backend/db/'

def kl(pks, qk, msks=None):
    # we can 'safely?' ignore divide by zero errors here.
    with np.errstate(divide='ignore', invalid='ignore'):
        min_kl = None
        for i in range(pks.shape[0]):
            if msks is not None:
                curr_kl = entropy(pks[i][msks], qk)
            else:
                curr_kl = entropy(pks[i], qk)
            if min_kl is None or curr_kl < min_kl:
                min_kl = curr_kl
        return min_kl

class Bridge:
    def __init__(self, nb_sounds=10, path_to_db=default_db):
        self.objs = np.load(path_to_db + 'objs_db.npy')
        self.plcs = np.load(path_to_db + 'plcs_db.npy')
        self.msks = np.load(path_to_db + 'mask.npy').astype('int32')
        self.nb_sounds = nb_sounds

    # obj_dist: distribution of objects (shape: (1000,))
    # plc_dist: distribution of places (shape: (401,))
    # chatter_level: level of chatter (0 <= chatter_level <= 1.0)
    # use_obj: whether to use objects
    # use_plc: whether to use places
    # use_chatter: whether to use chatter or normal mode
    # Returns: a vector of shape (10,) containing volume levels
    def get_sound(self, obj_dist, plc_dist, chatter_level=0.0, use_obj=True, use_plc=True, use_chatter=False):
        out = np.zeros(self.nb_sounds)

        if use_chatter:
            entropies = np.zeros(self.nb_sounds)
            for i in range(self.nb_sounds):
                entropy_obj = kl(self.objs[1 << i], obj_dist, None)
                entropy_plc = kl(self.plcs[1 << i], plc_dist, self.msks)

                if use_obj:
                    entropies[i] += entropy_obj
                if use_plc:
                    entropies[i] += entropy_plc

            indices = np.argsort(entropies)

            # -4.6 = ln 0.01
            l = -4.6 * (chatter_level - 1.0)

            for i in range(self.nb_sounds):
                out[indices[i]] = np.exp(-l * i)

        else:
            # compute the closest obj/plc out of 1024 possible choices.
            # using kl distance

            min_kl = None
            best = None

            for i in range(1, 1 << self.nb_sounds):
                entropy_obj = kl(self.objs[i], obj_dist, None)
                entropy_plc = kl(self.plcs[i], plc_dist, self.msks)

                total_entropy = 0.0

                if use_obj:
                    total_entropy += entropy_obj
                if use_plc:
                    total_entropy += entropy_plc

                if best is None or total_entropy < min_kl:
                    min_kl = total_entropy
                    best = i

            for i in range(self.nb_sounds):
                if best & (1 << i):
                    out[i] = 1.0
                else:
                    out[i] = 0.0

        return out 

