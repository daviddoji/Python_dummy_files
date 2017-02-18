#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 13:19:12 2017

@author: david
"""

import os
import sys
import natsort


# input() workaround to support Python 2. Python 3 renamed
# raw_input() => input().
# Alias input() to raw_input() if raw_input() exists (Python 2).
try:
    input = raw_input
except NameError:
    pass


def print_files(directory, file_extensions=['pdf', 'doc', 'mp4',
                                            'mkv', 'vob']):
#def print_movie_files(movie_directory, movie_extensions=['avi', 'dat', 'mp4',
#                                                         'mkv', 'vob']):
    ''' Print files in movie_directory with extensions in movie_extensions,
    recursively.'''

    # Get the absolute path of the movie_directory parameter
    directory = os.path.abspath(directory)
#    movie_directory = os.path.abspath(movie_directory)

    # Get a list of files in movie_directory
    directory_files = natsort.natsorted(os.listdir(directory))
#    movie_directory_files = os.listdir(movie_directory)

    # Traverse through all files
    for filename in directory_files:
#    for filename in movie_directory_files:
        filepath = os.path.join(directory, filename)
#        filepath = os.path.join(movie_directory, filename)

        # Check if it's a normal file or directory
        if os.path.isfile(filepath):

            # Check if the file has an extension of typical video files
            for file_extension in file_extensions:
#            for movie_extension in movie_extensions:
                # Not a movie file, ignore
                if not filepath.endswith(file_extension):
#                if not filepath.endswith(movie_extension):
                    continue

                # We have got a video file! Increment the counter
                print_files.counter += 1
#                print_movie_files.counter += 1

                # Print it's name
                print('{0}'.format(filepath))
        elif os.path.isdir(filepath):
            # We got a directory, enter into it for further processing
            print_files(filepath)
#            print_movie_files(filepath)


if __name__ == '__main__':

    # Directory argument supplied, check and use if it's a directory
    if len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            directory = sys.argv[1]
#            movie_directory = sys.argv[1]
        else:
            print('ERROR: "{0}" is not a directory.'.format(sys.argv[1]))
            exit(1)
    else:
        # Set our movie directory to the current working directory
        directory = os.getcwd()
#        movie_directory = os.getcwd()

    print('\n -- Looking for movies in "{0}" --\n'.format(directory))
#    print('\n -- Looking for movies in "{0}" --\n'.format(movie_directory))

    # Set the number of processed files equal to zero
    print_files.counter = 0
#    print_movie_files.counter = 0

    # Start Processing
    print_files(directory)
#    print_movie_files(movie_directory)

    # We are done. Exit now.
    print('\n -- {0} Movie File(s) found in directory {1} --'.format \
          (print_files.counter, directory))
#    print('\n -- {0} Movie File(s) found in directory {1} --'.format \
#            (print_movie_files.counter, movie_directory))
    print('\nPress ENTER to exit!')

    # Wait until the user presses enter/return, or <CTRL-C>
    try:
        input()
    except KeyboardInterrupt:
        exit(0)
