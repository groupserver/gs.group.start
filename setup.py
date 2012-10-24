# coding=utf-8
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.group.start',
    version=version,
    description="Start a GroupServer Group",
    long_description=open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Framework :: Zope2",
      "Intended Audience :: Developers",
      "License :: Other/Proprietary License",
      "Natural Language :: English",
      "Operating System :: POSIX :: Linux"
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='group security privacy',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='http://www.onlinegroups.net/',
    license='other',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.group'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
        'pytz',
        'zope.cachedescriptors',
        'zope.component',
        'zope.event',
        'zope.formlib',
        'zope.interface',
        'zope.schema',
        'Zope2',
        'gs.content.layout',
        'gs.content.form',
        'gs.group.base',
        'gs.group.type.discussion',  # For the marker interface
        'gs.group.member.join',
        'gs.group.privacy',
        'gs.help',  # For the Admin Help viewlet manager
        'gs.site.change.base',  # For the site-admin links viewlet manager
        'Products.XWFCore',
        'Products.GSAuditTrail',
        'Products.CustomUserFolder',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
