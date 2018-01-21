import numpy as np

# Linking functions to be accessed by the frontend

default_db = 'backend/db/'

def entropy(pk, qk):
    # we can 'safely?' ignore divide by zero errors here.
    with np.errstate(divide='ignore', invalid='ignore'):
        return -np.sum(np.sum(pk * np.log(pk/qk) - pk + qk, axis=1), axis=1)

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
    def get_sound(self, obj_dist, plc_dist, chatter_level=0.0, use_obj=True, use_plc=True, use_chatter=False):
        out = np.zeros(10)

        if use_chatter:
            entropies = np.zeros(10)
            for i in range(10):
                entropy_obj = entropy(self.objs[1 << i], obj_dist)
                entropy_plc = entropy(self.plcs[1 << i], plc_dist)

                if use_obj:
                    entropies[i] += entropy_obj
                if use_plc:
                    entropies[i] += entropy_plc

            indices = np.argsort(entropies)

            # -4.6 = ln 0.01
            l = -4.6 * (chatter_level - 1.0)

            for i in range(10):
                out[indices[i]] = exp(-l * i)

        else:
            # compute the closest obj/plc out of 1024 possible choices.
            # using kl distance

            entropy_obj = entropy(self.objs, obj_dist)
            entropy_plc = entropy(self.plcs, plc_dist)

            assert entropy_obj.shape == (1024,)
            assert entropy_plc.shape == (1024,)

            total_entropy = np.zeros_like(entropy_obj)

            if use_obj:
                total_entropy += entropy_obj
            if use_plc:
                total_entropy += entropy_plc

            minimum = np.nanargmin(total_entropy)

            for i in range(len(out)):
                if minimum & (1 << i):
                    out[i] = 1.0
                else:
                    out[i] = 0.0

        return out 

