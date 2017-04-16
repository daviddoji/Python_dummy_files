#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 13:19:12 2017

@author: David Doblas Jiménez
"""

import os
import sys
import natsort


def print_files(directory, file_extensions=['pdf', 'doc', 'mp4',
                                            'mkv', 'vob']):
    ''' Print files in movie_directory with extensions in movie_extensions,
    recursively.'''

    # Get the absolute path of the movie_directory parameter
    directory = os.path.abspath(directory)

    # Get a list of files in movie_directory
    directory_files = natsort.natsorted(os.listdir(directory))

    # Traverse through all files
    for filename in directory_files:
        filepath = os.path.join(directory, filename)

        # Check if it's a normal file or directory
        if os.path.isfile(filepath):

            # Check if the file has an extension of typical video files
            for file_extension in file_extensions:
                # Not a movie file, ignore
                if not filepath.endswith(file_extension):
                    continue

                # We have got a video file! Increment the counter
                print_files.counter += 1

                # Print it's name
                print('{0}'.format(filepath))
        elif os.path.isdir(filepath):
            # We got a directory, enter into it for further processing
            print_files(filepath)


if __name__ == '__main__':

    # Directory argument supplied, check and use if it's a directory
    if len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            directory = sys.argv[1]
        else:
            print('ERROR: "{0}" is not a directory.'.format(sys.argv[1]))
            exit(1)
    else:
        # Set our movie directory to the current working directory
        directory = os.getcwd()

    print('\n -- Looking for files in "{0}" --\n'.format(directory))

    # Set the number of processed files equal to zero
    print_files.counter = 0

    # Start Processing
    print_files(directory)

    # We are done. Exit now.
    print('\n -- {0} File(s) found in directory {1} --'.format
          (print_files.counter, directory))
    print('\nPress ENTER to exit!')

    # Wait until the user presses enter/return, or <CTRL-C>
    try:
        input()
    except KeyboardInterrupt:
        exit(0)
