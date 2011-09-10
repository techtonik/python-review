#!/usr/bin/env python
"""
This script copies latest upload.py to review.py and refreshes
version in setup.py to upload `review` package to PyPI.
"""
from __future__ import with_statement

import shutil
import os,sys


UPLOAD_PY_PATH = "../upload.py"
REPO_VIEW = "http://code.google.com/p/rietveld/source/detail?r="

def get_hg_repo_revision(path):
    """return current revision of a repository at path

       :raise:  EnvironmentError if `hg` isn't found or path invalid
       :return: string like 'num:hash'
    """
    from subprocess import Popen, PIPE
    if os.path.isfile(path):
        path = os.path.dirname(path)
    try:
        hgprocess = Popen('hg id -ni "%s"' % path, shell=True,
                          stdout=PIPE, stderr=PIPE)
        output = hgprocess.communicate()
        if hgprocess.returncode != 0:
            raise EnvironmentError(hgprocess.returncode, "'hg' returned error")
        hgid, hgnum = output[0].strip().split()
        return hgnum + ':' + hgid
    except OSError:
        raise EnvironmentError(2, "'hg' command not found")

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
revision = get_hg_repo_revision(UPLOAD_PY_PATH)
version = revision.split(':')[0].strip('+')
# after conversion to Mercurial revision number decreased, and the
# latest released r749 corresponds to 655 num in Hg
with open("setup.py") as fr:
    setup_contents = fr.readlines()
with open("HISTORY") as fh:
    history_content = fh.read()
with open("setup.py","wb") as fw:
    foundver = False
    setup_iter = iter(setup_contents)
    for line in setup_iter:
        # injecting revision number
        vpos = line.find("version='r")
        if vpos != -1:
            line = line[:vpos] + "version='r%s',\n" % version
            foundver = True
        fw.write(line)
        
        # injecting HISTORY
        if line.find("Changes::") != -1:
            fw.write("\n")
            fw.write(history2rst(history_content))
            fw.write("\n")
            while line[0] != '*':
                line = setup_iter.next()
            fw.write(line)
    if not foundver:
        print "warning: can't find version string in setup.py"
print "done."
