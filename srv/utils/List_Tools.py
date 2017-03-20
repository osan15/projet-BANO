class List_Tools(object):
    @classmethod
    def all_indices(cls ,value, qlist):
        indices = []
        idx = -1
        while True:
            try:
                idx = qlist.index(value, idx + 1)
                indices.append(idx)
            except ValueError:
                break
        return indices



