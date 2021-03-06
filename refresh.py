#!/usr/bin/env python
"""
This script was used to copy latest upload.py to review.py and
refresh version in setup.py to upload `review` package to PyPI.

After migration of Rietveld to GitHub, it doesn't work anymore.
"""

import shutil
import os,sys

import os
import sys

# --- bootstrap locally ---
__dir__ = os.path.abspath(os.path.dirname(__file__))

import subprocess

def run(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()

def run_capture(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    result = process.communicate()
    return result[0]

# /-- locally ---


ROOT = __dir__
RIETROOT = ROOT + '/rietveld'
UPLOAD_PY_PATH = RIETROOT + '/upload.py'
REPO_VIEW = "http://code.google.com/p/rietveld/source/list?path=/upload.py&r="


def get_hg_path_revision(path):
    """return latest modification revision of a path inside hg

       :raise:  EnvironmentError if `hg` isn't found or path invalid
       :return: string like 'num:hash'
    """
    from subprocess import Popen, PIPE

    cmd = 'hg log -M -l 1 --template "{node|short} {rev}" --cwd "%s" "%s"' \
                % (os.path.dirname(path) or '.', os.path.basename(path))
    try:
        hgprocess = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
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
    revision = re.compile(r'\d{3,4}:[0-9a-f]{12}')
    anchors = revision.findall(history) # ['695:ba3f47e4a614', ...]
    history = revision.sub(r'`\g<0>`_', history)
    history += "\n"
    history += "\n".join(
      ['.. _`%s`: %s%s' % (x, REPO_VIEW, x.split(':')[1]) for x in anchors]
    )
    history += "\n"
    return history

# with the move to GitHub, this is now disfunctional

"""
if not os.path.exists(RIETROOT):
    run('hg clone https://code.google.com/p/rietveld')

if not os.path.exists(UPLOAD_PY_PATH):
  sys.exit("error: upload.py is not found in configured dir")

print "copying upload.py to review.py"
shutil.copyfile(UPLOAD_PY_PATH, "review.py")

print "updating version and history in setup.py"
revision = get_hg_path_revision(UPLOAD_PY_PATH)
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
        vpos = line.find("version='")
        if vpos != -1:
            line = line[:vpos] + "version='%s',\n" % version
            foundver = True
        fw.write(line)
        
        # injecting HISTORY
        if line.find("Changes:") != -1:
            fw.write("\n")
            fw.write(history2rst(history_content))
            fw.write("\n")
            while line[0] != '*':
                line = setup_iter.next()
            fw.write(line)
    if not foundver:
        print "warning: can't find version string in setup.py"

print "done."
"""
