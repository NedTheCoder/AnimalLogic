import sys
import os

def execute_shell_command(command):
    stream = os.popen(command)
    output = stream.read()
    return output

def compare_multiline_strings(str1, str2):
    arr1 = str1.split()
    arr2 = str2.split()
    return arr1 == arr2

def main():

    formats_message = execute_shell_command('python phonebook.py --list_formats')

    if 'No data format is registered' in formats_message:
        print('Can not test the code because no data format is registered.')
        return False

    data_formats = formats_message.splitlines()
    data_formats.pop(0)

    if not data_formats:
        print('List of supported formats is empty!')
        return False

    # Go through all the supported formats and verify that the tested code returns the correct string
    verdict = True
    for form in data_formats:
        # Get the code response
        command = "python phonebook.py --{} test_file.{}".format(form, form)
        print("Executing command '{}'".format(command))
        format_response = formats_message = execute_shell_command(command)

        # Get the content of the test file
        f_content = open("test_file.{}".format(form), "r").read()

        # Compare the two and set the verdict
        if not compare_multiline_strings(format_response, f_content):
            verdict = False
            print("Test failed for the format {}".format(form))
        else:
            print("Test for the format {} passed".format(form))

    return verdict


if __name__ == "__main__":
    main()

