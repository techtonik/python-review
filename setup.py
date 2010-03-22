"""
Package `upload.py` script as `review.py` for uploading to PyPI
as executable module that can be then called as::

  python -m review

"""

# To update PyPI package, issue
#   python setup.py sdist upload


from distutils.core import setup
import shutil, sys


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

upload_py_path = "../../static/upload.py"
version = get_svn_path_revision(upload_py_path)
shutil.copyfile(upload_py_path, "review.py")
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
