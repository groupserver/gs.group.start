# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
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
from zope.component.interfaces import ObjectEvent
from zope.component.interfaces import IObjectEvent


class IGSGroupCreatedEvent(IObjectEvent):
    """ An event issued after a group has been created, and all core
        changes to the group have been made."""


class GSGroupCreatedEvent(ObjectEvent):
    implements(IGSGroupCreatedEvent)
