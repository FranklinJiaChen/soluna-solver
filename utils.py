def nlist_to_ntup(input_list):
    """
    Recursively convert a nested list to a nested tuple.
    """
    if isinstance(input_list, list):
        return tuple(nlist_to_ntup(item) for item in input_list)
    else:
        return input_list

def ntup_to_nlist(input_tuple):
    """
    Recursively convert a nested tuple to a nested list.
    """
    if isinstance(input_tuple, tuple):
        return [ntup_to_nlist(item) for item in input_tuple]
    else:
        return input_tuple
