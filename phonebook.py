# Code for serializing and deserializing data
#
# It takes arguments from the command line and prints out the result of it's operation
#
# If the user specifies --list_formats argument the code will print out the list of supported data formats
#
# If the user specifies a data format and the file name (e.g. "--yaml data_file.yaml")
# the code will read the specified file and serialize it according to the specified data format.
# Then, the code will deserialize the data and print it to the standard output
#
# In order for the developer to add a new data format, they need to
# - write a serializing and deserializing functions
# - register the new data format and corresponding (de)serializing functions 
#   at the top of the main function using the register_data_format function

import sys
import json
import yaml
import argparse

# Class that (de)serializes the user data in different formats
class Phonebook:
    def __init__(self):
        self.data_formats = []
        self.name = "Phonebook"

    def register_data_format(self, form, s_function, d_function):
        temp = {}
        temp['format'] = form
        temp['serializer'] = s_function
        temp['deserializer'] = d_function
        self.data_formats.append(temp)

    def list_data_formats(self):
        if not self.data_formats:
            return []
        forms = []
        for data_format in self.data_formats:
            forms.append(data_format['format'])
        return forms

    def serialize(self, f, form):
        funct = None
        for data_format in self.data_formats:
            if data_format['format'] == form:
                funct = data_format['serializer']
                break
        if funct == None:
            raise Exception("Calling the serialize function of the object {} and the function is not registered!". format(self.name))

        return funct(f)

    def deserialize(self, l, form):
        funct = None
        for data_format in self.data_formats:
            if data_format['format'] == form:
                funct = data_format['deserializer']
                break
        if funct == None:
            raise Exception("Calling the deserialize function of the object {} and the function is not registered!". format(self.name))

        return funct(l)

# (De)Serializing functions for different data formats
# If adding a new data format, this is the place to add the (de)serializing functions
def serialize_yaml(f):
    with open(f, 'r') as file:
        return yaml.safe_load(file)

def deserialize_yaml(ulist):
    print(yaml.dump(ulist))


def serialize_json(f):
    jfile = open(f)
    return json.load(jfile)

def deserialize_json(ulist):
    print(json.dumps(ulist, indent=4))


def main():
    # Create the phonebook object
    pb = Phonebook()

    # Register the available data format
    # If adding a new data format, this is the place to register the format and associated (de)serializing functions
    pb.register_data_format('yaml', serialize_yaml, deserialize_yaml)
#    pb.register_data_format('json', serialize_json, deserialize_json)

    # Collect all registered data formats
    data_formats = pb.list_data_formats()

    # Get command line arguments
    parser = argparse.ArgumentParser(prog="Phonebook", description="Serializes data from a given file and then deserializes the data and prints them out", epilog="Animal Logic challenge")
    parser.add_argument("--list_formats", action='store_true', help="List all supported data formats.")

    # Look for registered data formats
    for form in data_formats:
        parser.add_argument("--{}".format(form))

    args = vars(parser.parse_args())

    # If the user asked for the list of formats, provide the list and terminate the execution
    if args['list_formats'] == True:
        if not data_formats:
            print("No data format is registered")
        else:
            print("Registered formats:")
            for form in data_formats:
                print(form)
        return

    # Go through all the data formats specified in the command line
    # and for each registered data format, do the serialization and deserialization
    for form in data_formats:
        data_file = args[form]
        if data_file:
            users = pb.serialize(data_file, form)
            pb.deserialize(users, form)

if __name__ == "__main__":
    main()

