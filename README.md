# File Converter - Imaris IMS to TIFF File

This is a command line tool that converts Imaris IMS files into TIFF files. 
It extracts the intensity arrays together with the corresponding meta information from the IMS file and saves it into an OME TIFF File. 

## User Instructions:

First clone the git repository: 

```bash
git clone https://github.com/username/project.git
```

Then create the corresponding mamba/conda environment and activate it:
```bash
# change directory 
cd file_converter_imaris_ims_to_tiff_file
# create environment 
mamba env create -f environment.yml
# activate environment
mamba activate ims_file_converter
```
(If you use conda instead of mamba, please replace mamba with conda.)

And now Imaris IMS files can be converted into OME TIFF Files by the following commanc
```bash
python ims_to_ome_tiff_converter.py -i <path_to_source_ims_file> -o <path_to_directory_for_saving_the_ome_tiff_file>
```
