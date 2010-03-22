"""
Package `upload.py` script as `review.py` for uploading to PyPI
as executable module that can be then called as::

  python -m review

"""

# To update PyPI package, issue
#   python setup.py sdist upload


from distutils.core import setup
import shutil, sys


upload_py_dir = "../../static/"

def get_upload_py_version():
    """return latest revision number of upload.py"""
    with open(upload_py_dir + ".svn/entries") as f:
        entries = [l.strip() for l in f.readlines()]

    # check known working copy version
    # it seems to be entries[0]
    if entries[0] != '10':
        sys.exit("Error: Unknown SVN working copy version")

    # check upload.py modification revision
    idx = entries.index("upload.py")
    entry = entries[idx:idx+33]
    rev = int(entry[9])
    return rev


shutil.copyfile(upload_py_dir + "upload.py", "review.py")
version = get_upload_py_version()
description = """
Usage::

    python -m review [options]

* Home Page:   http://codereview.appspot.com/
* Development: http://code.google.com/p/rietveld/
* Discussions: http://groups.google.com/group/codereview-discuss
"""

setup(
    name='review',
    version='r%s' % version,
    author='Google Inc. & Co.',

    description='rietveld code review upload script',
    long_description=description,
    license='Apache 2.0',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],

    py_modules=['review'],
)
