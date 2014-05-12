# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.txt', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.txt"), encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(name='gs.group.start',
    version=version,
    description="Start a GroupServer Group",
    long_description=open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='group security privacy',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='https://source.iopen.net/groupserver/gs.group.start/',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.group'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pytz',
        'zope.browserpage',
        'zope.browserresource',
        'zope.cachedescriptors',
        'zope.component',
        'zope.event',
        'zope.formlib',
        'zope.interface',
        'zope.schema',
        'zope.tal',
        'zope.tales',
        'zope.viewlet',  # For the <browser:viewlet /> config
        'Zope2',
        'gs.content.email.base',
        'gs.content.email.layout',
        'gs.content.js.jquery.base',
        'gs.content.layout',
        'gs.content.form',
        'gs.core',
        'gs.group.base',
        'gs.group.type.discussion',  # For the marker interface
        'gs.group.member.join',
        'gs.group.privacy',
        'gs.help',  # For the Admin Help viewlet manager
        'gs.site.change.base',  # For the site-admin links viewlet manager
        'Products.GSAuditTrail',
        'Products.GSGroup',
        'Products.XWFCore',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
