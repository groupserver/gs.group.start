# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, print_function, unicode_literals
from zope.cachedescriptors.property import Lazy
from gs.content.email.base import GroupEmail, TextMixin
from Products.GSGroup.interfaces import IGSMailingListInfo
UTF8 = 'utf-8'


class StartedMessage(GroupEmail):

    @Lazy
    def supportEmail(self):
        m = 'Hi!\n\nThe group {0}\n    {1}\nwas started and...'
        msg = m.format(self.groupInfo.name, self.groupInfo.url)
        sub = 'Group started'
        retval = self.mailto(self.siteInfo.get_support_email(), sub, msg)
        return retval

    @Lazy
    def email(self):
        l = IGSMailingListInfo(self.groupInfo.groupObj)
        retval = l.get_property('mailto')
        return retval


class StartedMessageText(StartedMessage, TextMixin):

    def __init__(self, context, request):
        super(StartedMessageText, self).__init__(context, request)
        filename = 'gs-group-started-{0}.txt'.format(self.groupInfo.id)
        self.set_header(filename)
