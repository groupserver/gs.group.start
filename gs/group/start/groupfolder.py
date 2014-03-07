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
from zope.interface import implements
from OFS.Folder import Folder
from gs.group.base.interfaces import IGSGroupMarker


# Standard group folder
class GSGroupFolder(Folder):
    implements(IGSGroupMarker)


def groupAddedHandler(groupFolder, event):
    """ This is an example of how to handle the IObjectAdded event,
        for an IGSGroupFolder. See the configure.zcml for an example of
        how to subscribe to the event.

    """
    assert IGSGroupMarker.providedBy(groupFolder), \
       "groupFolder did not implement IGSGroupMarker!"
    return
