import h5py
import json
import os

# define input path
input_path = '/home/sharedFolder/data/BMquant_dataset/aged/diaphysis'

# define output path
output_path = '../../data/info/'

# define name of info json file
json_file_name = 'channel_info_aged_diaphysis.json'


# create directory if it does not exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# get a list of all the files in the directory
file_list = os.listdir(input_path)

# filter the list to only include .ims files
ims_files = [f for f in file_list if f.endswith('.ims')]

# initialize dict for channels in each image
image_info_list = []

# iterate images
for n_image, image_file in enumerate(ims_files):
    # open ims file
    with h5py.File(os.path.join(input_path, image_file), 'r') as f:
        # generate list of available channels
        image_channel_ids = [int(ch_id.split(sep=' ')[-1]) for ch_id in f['DataSetInfo'] if ch_id.startswith('Channel')]
        # sort image channel ids
        image_channel_ids.sort()
        # generate list of channel names
        image_channel_names = [f['DataSetInfo'][f'Channel {i}'].attrs['Name'].tobytes().decode('ascii', 'ignore') for i in image_channel_ids]

    # append entry to image channel list
    image_info_list.append({'image_id': n_image,
                            'file_name': image_file,
                            'n_channels': len(image_channel_names),
                            'channel_names': image_channel_names})

    # initialize a dictionary for counting the images where a single channel is present
    count_dict = {}
    # iterate image info list
    for img_info in image_info_list:
        # read channel names from image info dict
        channels = img_info['channel_names']
        # iterate channels
        for ch in channels:
            # initialize channel counter
            count_dict[ch] = 0
    # iterate images
    for img_info in image_info_list:
        # read image channels from info dict
        channels = img_info['channel_names']
        # iterate channels of counter dict
        for ch in count_dict.keys():
            # check if channel is present in current image
            if ch in channels:
                # if so, increment counter
                count_dict[ch] += 1
    # sort counting dict by most frequent channels
    count_dict = {k: v for k, v in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)}

    # combine image info list and channel counter in one dict
    info_dict = {'image_info_list': image_info_list,
                 'channel_counts': count_dict}

    # write info_dict to a JSON file
    with open(os.path.join(output_path, json_file_name), 'w') as f:
        json.dump(info_dict, f, indent=4)





