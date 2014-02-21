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
from __future__ import unicode_literals
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.core import to_ascii
from gs.profile.notify.sender import MessageSender
UTF8 = 'utf-8'


class StartNotifier(object):
    textTemplateName = 'gs-group-start.txt'
    htmlTemplateName = 'gs-group-start.html'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        h = self.request.response.getHeader('Content-Type')
        self.oldContentType = to_ascii(h)

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Could not create the GroupInfo from %s' % self.context
        return retval

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                    name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                    name=self.htmlTemplateName)
        assert retval
        return retval

    def notify(self, adminInfo):
        s = 'New group: {0}'.format(self.groupInfo.name)
        subject = s.encode(UTF8)
        text = self.textTemplate(adminInfo=adminInfo)
        html = self.htmlTemplate(adminInfo=adminInfo)
        ms = MessageSender(self.context, adminInfo)
        ms.send_message(subject, text, html)
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        self.oldContentType)
