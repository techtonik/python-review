"""
This script copies latest upload.py to review.py and refreshes
version in setup.py to upload `review` package to PyPI.
"""

import shutil


def get_svn_path_revision(path):
    """return latest modification revision of a path inside svn

       :raise:  EnvironmentError if SVN working copy format is unknown
       :return: int
    """
    from os.path import basename, dirname, join, isdir

    if isdir(path):
        entries_path = join(path, ".svn", "entries")
    else:
        entries_path = join(dirname(path), ".svn", "entries")
    with open(entries_path) as f:
        entries = [l.strip() for l in f.readlines()]

    # check known working copy version
    # it seems to be entries[0]
    if entries[0] != '10':
        raise EnvironmentError(10, "Unknown SVN working copy format")

    # check entry modification revision
    if isdir(path):
        return int(entries[10])
    else:
        idx = entries.index(basename(path))
        entry = entries[idx:idx+33]
        return int(entry[9])

# copy upload.py to review.py
upload_py_path = "../../static/upload.py"
shutil.copyfile(upload_py_path, "review.py")
# replace version/revision in setup.py
version = get_svn_path_revision(upload_py_path)
with open("setup.py") as fr:
    setup_contents = fr.readlines()
with open("setup.py","wb") as fw:
    for line in setup_contents:
        vpos = line.find("version='r")
        if vpos != -1:
            line = line[:vpos] + "version='r%s',\n" % version
        fw.write(line)
