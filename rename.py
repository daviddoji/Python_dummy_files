# -*- coding: utf-8 -*-
# !python3
from __future__ import absolute_import
import re
import glob
import os
from normalizr import Normalizr


normalizr = Normalizr(language='es')


def main():
    print(os.path.basename(__file__), "running...")

    renamer("*.pdf", r"\s+", "_")
    renamer("*.pdf", r"\.", "_")
    renamer("*_pdf", r"_pdf", ".pdf")
    renamer("*.pdf", r"__", "_")
    # renamer("*.jpg-large", r"^(.*)\.jpg-large$", r"\1.jpg")
    # renamer("*.unsafe", r"^(.*)\.unsafe$", r"\1")
    # renamer("*.doc", r"^(.*)\.doc$", r"new(\1).doc") #forward
    # renamer("*.doc", r"^new\((.*)\)\.doc", r"\1.doc") #reverse
    print(os.path.basename(__file__), "complete...")


def renamer(files, pattern, replacement):
    isRemove = True

    for pathname in glob.glob(files):
        basename = os.path.basename(pathname)
        normalizations = ['remove_accent_marks']
        basename = normalizr.normalize(basename, normalizations)
        new_filename = re.sub(pattern, replacement, basename)
        if new_filename != basename:
            try:
                os.rename(pathname, os.path.join(os.path.dirname(pathname),
                                                 new_filename))
                print("success: {} changed to -> {}".format(pathname,
                                                            new_filename))
            except:
                print("error: {} already exists".format(new_filename))

                if ('isRemove'):
                    try:
                        os.remove(pathname)
                        print("removed: {} because its a dupe".format(pathname))
                    except:
                        print("error: cannot remove {}".format(pathname))

if __name__ == "__main__":
    main()
