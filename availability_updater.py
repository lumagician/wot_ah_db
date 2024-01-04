import os
import hashlib
import json

# Directory containing geojson files
export_directory = "exports/"

# create a list of all the available exports
available_exports = []

# get all the files in the directory
files = os.listdir(export_directory)

# loop through all the files
for file in files:
    # check if the file is a geojson file
    if file.endswith(".geojson"):
        # add the file to the available exports list
        available_exports.append(file)
        # open the file and read it
        with open(os.path.join(export_directory, file), 'rb') as f:
            # read the file
            data = f.read()
            # calculate the hash of the file
            hash_value = hashlib.md5(data).hexdigest()
            # create a new file with the same name as the original file but with a .hash extension
            with open(os.path.join(export_directory, file + ".hash"), 'w') as f2:
                # write the hash to the file
                f2.write(hash_value)

# create a new list to store export dictionaries
export_list = []

# go through all the available exports and read the amount of features in each file, the file size, the filename, and the hash
for export in available_exports:
    # open the file
    with open(os.path.join(export_directory, export), 'r') as f2:
        # read the file
        data = json.load(f2)
        # get the file size
        file_size = os.path.getsize(os.path.join(export_directory, export))
        # get the hash of the file
        with open(os.path.join(export_directory, export + ".hash"), 'r') as f3:
            # read the file
            hash_value = f3.read()
            # create a dictionary with the filename, the amount of features, the file size, and the hash
            export_dict = {"filename": export, "file_size": file_size, "hash": hash_value}
            # append the dictionary to the list
            export_list.append(export_dict)

# create a new file called available_exports.json
with open("available_exports.json", 'w') as f:
    # write the entire list as a JSON array to the file
    f.write(json.dumps(export_list, indent=2))
