"""
This script copies latest upload.py to review.py and refreshes
version in setup.py to upload `review` package to PyPI.
"""
from __future__ import with_statement

import shutil
import os,sys


UPLOAD_PY_PATH = "../upload.py"
REPO_VIEW = "http://code.google.com/p/rietveld/source/detail?r="

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

def history2rst(history):
    import re

    # linkify revisions
    revision = re.compile(r'^(r\d{3,4}) -', re.M)
    anchors = revision.findall(history) # ['r749', 'r745', ...]
    history = revision.sub(r'  | \1_ -', history)
    history += "\n"
    history += "\n".join(
      ['.. _%s: %s%s' % (x, REPO_VIEW, x[1:]) for x in anchors]
    )
    history += "\n"
    return history


if not os.path.exists(UPLOAD_PY_PATH):
  sys.exit("error: upload.py is not found in parent dir")

print "copying ../upload.py to review.py"
shutil.copyfile(UPLOAD_PY_PATH, "review.py")

print "updating version and history in setup.py"
version = get_svn_path_revision(UPLOAD_PY_PATH)
with open("setup.py") as fr:
    setup_contents = fr.readlines()
with open("HISTORY") as fh:
    history_content = fh.read()
with open("setup.py","wb") as fw:
    setup_iter = iter(setup_contents)
    for line in setup_iter:
        # injecting revision number
        vpos = line.find("version='r")
        if vpos != -1:
            line = line[:vpos] + "version='r%s',\n" % version
        fw.write(line)
        
        # injecting HISTORY
        if line.find("Changes::") != -1:
            fw.write("\n")
            fw.write(history2rst(history_content))
            fw.write("\n")
            while line[0] != '*':
                line = setup_iter.next()
            fw.write(line)
print "done."