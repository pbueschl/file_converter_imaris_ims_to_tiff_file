import h5py
import numpy as np
import nibabel as nib
import os

# define input path
input_path = '//data/LabeledData.h5'
# define output path
output_path = '//data/Dataset001_BM'
# use os.makedirs() to create the directory if it does not exist
if not os.path.exists(output_path):
    os.makedirs(output_path)
# check if subdirectory imageTr exists
if not os.path.exists(os.path.join(output_path,'imagesTr')):
    os.makedirs(os.path.join(output_path,'imagesTr'))
# check if subdirectory labelsTr exists
if not os.path.exists(os.path.join(output_path,'labelsTr')):
    os.makedirs(os.path.join(output_path,'labelsTr'))
# input file
f = h5py.File(input_path, 'r')
# get list of samples
list_of_samples = list(f.keys())
# get number of samples
n_samples = len(list_of_samples)

# set image iterator
im_it = 0
# iterate samples
for sample in f.keys():
    # iterate patches
    for patch in f[sample].keys():
        # set input channel iterator to 0
        in_ch = 0
        # initialize list of label_channels
        list_label_channels = []
        # iterate channels
        for channel in f[sample][patch].keys():
            # check if it is an input channel
            if channel[:10] == 'in_channel':
                # convert data to numpy array
                image = np.array(f[sample][patch][channel])
                # remove padding from image
                image = image[184:, 184:]
                # add a third dimension with a single slice to the image
                image = np.expand_dims(image, axis=2)
                # create a nifti image object
                nifti_image = nib.Nifti1Image(image, np.eye(4))
                # save channel as nifti
                nib.save(nifti_image, os.path.join(output_path, 'imagesTr', f'BM_{im_it:04d}_{in_ch:04d}.nii.gz'))
                # increment input channel counter
                in_ch += 1
            else:
                # fetch number from label channel
                n = int(channel[-1])
                # convert channel data to numpy array and multiply it with fetched number
                label = np.array(f[sample][patch][channel])*n
                # append label array to label channel list
                list_label_channels.append(label)
        # combine label arrays
        # get first label channel
        labels = next(iter(list_label_channels))
        # iterate other label channels
        for label_channel in list_label_channels:
            # update labels
            labels[labels < label_channel] = label_channel[labels < label_channel]

        # add a third dimension with a single slice to the image
        labels = np.expand_dims(labels, axis=2)
        # create a nifti image object
        nifti_labels = nib.Nifti1Image(labels, np.eye(4))
        # save channel as nifti
        nib.save(nifti_labels, os.path.join(output_path, 'labelsTr', f'BM_{im_it:04d}.nii.gz'))

        # increment image counter
        im_it += 1

print('...finished processing!')
