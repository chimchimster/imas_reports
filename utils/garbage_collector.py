import os


def clear():
    directory = os.getcwd().rstrip('utils') + 'word/temp/'
    for file in os.listdir(directory):
        os.remove(directory + file)