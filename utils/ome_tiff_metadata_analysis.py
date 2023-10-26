import argparse
import tifffile as tif
import json
import os


def read_ome_tiff_metadata_file(path_to_image):
    """
    Opens an OME TIFF file and returns metadata containing dictionary
    :param path_to_image: path to an OME TIFF file (string)
    :return:  metadata (dict)
    """
    with tif.TiffFile(path_to_image) as f:
        # read metadata
        metadata = f.imagej_metadata
        # restore list from string of channel_names
        metadata['channel_names'] = eval(metadata['channel_names'])
    # return the metadata
    return metadata


def read_ome_tiff_metadata_directory(path_to_directory):
    """
    Iterates OME TIFF files of the passed directory and returns a dictionary containing a list of metadata dictionaries
    of all files as well as the counts in how many images a certain channel is available
    :param path_to_directory: path to a directory that holds OME TIFF files (string)
    :return: (dict) dictionary with information about the single image metadata and channel counts. It is structured in the
             following way: {'image_metadata_list': [metadata_dict_image0, metadata_dict_image1, ...],
                             'channel_counts': {channel_name0: count,
                                                channel_name2: count, ...}}
    """
    # get a list of all files in the directory
    file_list = os.listdir(path_to_directory)

    # filter the list to only include .ome.tif files
    ome_tiff_files = [f for f in file_list if f.endswith('.ome.tif')]

    # initialize list for metadata in each image
    image_metadata_list = []

    # iterate images
    for image_id, image_file in enumerate(ome_tiff_files):
        # read metadata
        metadata = read_ome_tiff_metadata_file(os.path.join(path_to_directory, image_file))
        # add successive image id number to metadata
        metadata['image_id'] = image_id

        # append entry to image metadata list
        image_metadata_list.append(metadata)

    # initialize a dictionary for counting the images where a certain channel is present
    count_dict = {}
    # iterate image info list
    for img_info in image_metadata_list:
        # read channel names from image info dict
        channels = img_info['channel_names']
        # iterate channels
        for ch in channels:
            # initialize channel counter
            count_dict[ch] = 0
    # iterate images
    for img_info in image_metadata_list:
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

    # combine image metadata list and channel counter in one dict
    info_dict = {'image_metadata_list': image_metadata_list,
                 'channel_counts': count_dict}

    # return info_dict
    return info_dict


def main():
    """
    Main function for analysing the metadata of OME TIFF file(s). It reads the metadata of a single OME TIFF file or of
    all OME TIFF files in a given directory and saves them in a JSON file at a given output path.
    In case that a directory was given, the overall channel counts (how many images in the given directory hold a
    certain channel) are added to the JSON file in addition to the metadata of all files
    """

    # Create the parser object
    parser = argparse.ArgumentParser(description='Read available channel names or either a single OME TIFF file or '
                                                 'several OME TIFF files in a given directory.')

    # Add arguments for the input path and output directory
    parser.add_argument('-i', '--input', required=True,
                        help='Path to input OME TIFF file or directory')
    parser.add_argument('-o', '--output', required=True,
                        help='Path for storing a JSON file with the channel name information')

    # Parse the arguments
    args = parser.parse_args()

    # check if output directory exists, if not create it
    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))

    # check if passed input path belongs to a file or directory
    if os.path.isfile(args.input):
        # read metadata from the passed file
        image_info = read_ome_tiff_metadata_file(args.input)
    else:
        # read metadata from all OME TIFF files in dict and count the channel occurrences
        image_info = read_ome_tiff_metadata_directory(args.input)

    # write the image information results to a JSON file
    with open(os.path.join(args.output), 'w') as f:
        json.dump(image_info, f, indent=4)


if __name__ == "__main__":
    main()
