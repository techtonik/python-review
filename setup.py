"""
This setup.py packages `upload.py` script from rietveld project
as `review.py` for PyPI, so that it could be called as::

  python -m review

To update PyPI package, issue::
   python refresh.py
   python setup.py sdist upload
"""

from distutils.core import setup

setup(
    name='review',
    version='r515',
    author='Google Inc. & Co.',
    url='http://codereview.appspot.com/',

    description='rietveld code review upload script',
    long_description="""
Usage::

    python -m review [options]

* Home Page:   http://codereview.appspot.com/
* Development: http://code.google.com/p/rietveld/
* Discussions: http://groups.google.com/group/codereview-discuss/
""",
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
