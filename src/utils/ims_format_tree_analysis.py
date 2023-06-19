import h5py
import json
import numpy as np


# define path to ims file that should be analysed
filename = '/home/sharedFolder/data/BMquant_dataset/young/diaphysis/FoxP3_Femur_3_Dia.ims'
# define output path to the json file that should hold the tree structure information
json_output_path = '../../data/info/ims_tree_structure_Femur_3_Dia.json'


def print_tree(name, obj):
    """
    Recursive function that analyses the tree structure of the keys in a given ims file (ims files are based on
    hdf5 format).
    :param name: key in parent layer (str)
    :param obj: datastructure that should be analysed
    :return:
    """
    # check if object is an instance of some final classes or if one more layer should be analysed
    if isinstance(obj, (h5py.Dataset, np.ndarray, np.uint64, np.float32)):
        # return information the final layer instance
        return {"type": str(type(obj)), "shape": obj.shape, "dtype": str(obj.dtype)}
    else:
        # check if the current objects holds attribute items
        try:
            # read child items
            children = {**{key: print_tree(key, val) for key, val in obj.attrs.items()}}
        except:
            # initialize an empty dictionary for child items
            children = {}
        # check if the current object holds items
        try:
            # read child items and update the child object dictionary
            children.update({key: print_tree(key, val) for key, val in obj.items()})
        finally:
            # update the child objects and return the final dictionary of child items
            return {**children}


# open the ims file
with h5py.File(filename, 'r') as f:
    # get the tree structure of the file
    tree = print_tree(filename, f)

    # write the tree to a JSON file
    with open(json_output_path, 'w') as file:
        json.dump(tree, file, indent=4)

# print status message
print(f'Finished IMS file tree analysis!')
