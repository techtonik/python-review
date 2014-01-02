#!/usr/bin/env python
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
    version='1206',
    author='Google Inc. & Co.',
    author_email='codereview-discuss@googlegroups.com',
    url='http://codereview.appspot.com/',

    description='upload script for Rietveld code review tool',
    long_description="""
Usage::

    python -m review [options]

Changes:


 `1206:7f692a624f2e`_ - 2013-11-11

 - Improved git similarity detection, by ilevy (24120043)
 - Add timeout to deal with connection hands, by hinoka (21530045)
 - Fix for "git config diff.noprefix true", by newt (21070043)
 - Parallel upload of patch and base files, by Ojan Vafai (12629043)
 - Fix binary uploads with git, by Chris Phan (13668043)
 - Add API to skip authentication (11915043)
 - Show supported values for --vcs option (10822044)
 - Treat svg as text (10117044)
 - Treat images as binaries (9183044)
 - Support OAuth, by dhermes (8736046, 8633045, 8621045, 8621045, ...)
 - Fix Gnome's keyring integration, by vadimsh (7385046, 8725043)
 - Add wiki links to --help output

 `966:66d93f2615b7`_ - 2012-11-30

 - Pass the account type through to the HttpRpcServer, by Dominic Hamon.
 - Use git similarity option, by Robert Iannucci (6574057, 6726050)
 - Fix Removing/updating password in keyring is not possible (#329, 6492080)
 - Fix HTTP 403 error on python 2.7 (6490072)
 - Fix support for renamed files, aka git mv in upload.py (#251, 4333051)
 - Upload binary files that are not images (6221063)
 - Add message from upload.py when updating an issue (#351, 5687062)
 - Make sure color is not used in git diff (5619043)
 - Default --title on --message and clamp at 100 chars (5574050)

 `801:2f5709156db2`_ - 2011-01-10  --  Options meaning changed

 - Subversion 1.7 support, by Jocelyn Fiat (issue #359, 5529052)
 - Command line options made intuitive (review 5476044)::

     1. on first submission
        -t, --title       issue subject
        -m, --message     issue description
        -F, --file <file> read description from file
     2. on issue update
        -t, --title       new patchset title
        -m, --message     message to reviewers
        -F, --file <file> read message from file

 - New upload_complete hook for async processing (review 5440044)
 - Print error messages for server errors (review 5399053) 
 - Fix fail when Hg is executed from subdir (issue #345, 5364065)
 - Allow empty files to be uploaded from Git (review 5370042)

 `709:840f9bb917ba`_ - 2011-09-22

 - Add repository ID field to link Issue with Repository (review 5093045)
 - More fixes to fit upload.py options in one screen (review 4962070)

 `695:ba3f47e4a614`_ - 2011-09-07

 - Hide perforce options unless explicitly requested (4968071)
 - --send_patch option to attach diff instead of inline, by Kaelyn (4881041)
 - Ignore git submodules when generating diffs (issue #324, 4822044)
 - Escape @ in filenames when running SVN commands (issue #322, 4745041)
 - Remove MIMETYPES whitelist as a way to detect if file is binary (4641078)

.. _`1206:7f692a624f2e`: http://code.google.com/p/rietveld/source/list?path=/upload.py&r=7f692a624f2e
.. _`966:66d93f2615b7`: http://code.google.com/p/rietveld/source/list?path=/upload.py&r=66d93f2615b7
.. _`801:2f5709156db2`: http://code.google.com/p/rietveld/source/list?path=/upload.py&r=2f5709156db2
.. _`709:840f9bb917ba`: http://code.google.com/p/rietveld/source/list?path=/upload.py&r=840f9bb917ba
.. _`695:ba3f47e4a614`: http://code.google.com/p/rietveld/source/list?path=/upload.py&r=ba3f47e4a614

* Rietveld Home Page:   http://codereview.appspot.com/
* Rietveld Development: http://code.google.com/p/rietveld/
* This script: http://bitbucket.org/techtonik/python-review/
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
