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
from __future__ import absolute_import, unicode_literals
from datetime import datetime
SUBSYSTEM = 'gs.group.start'
from logging import getLogger
log = getLogger(SUBSYSTEM)
from pytz import UTC
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
    AuditQuery, event_id_from_data
from Products.XWFCore.XWFUtils import munge_date

UNKNOWN = '0'
START = '1'
START_FAILED = '2'


class AuditEventFactory(object):
    implements(IFactory)

    title = 'Group Start Audit-Event Factory'
    description = 'Creates a GroupServer audit event for starting a group'

    def __call__(self, context, event_id, code, date,
        userInfo, instanceUserInfo, siteInfo, groupInfo=None,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        if code == START:
            event = StartEvent(context, event_id, date, userInfo, siteInfo,
                                groupInfo, instanceDatum, supplementaryDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
              userInfo, instanceUserInfo, siteInfo, groupInfo,
              instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


class StartEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person starting a group.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, adminInfo, siteInfo, groupInfo,
                name, privacy):
        BasicAuditEvent.__init__(self, context, id, START, d, adminInfo,
                            None, siteInfo, groupInfo, name, privacy, SUBSYSTEM)

    def __unicode__(self):
        retval = '%s (%s) started the group %s (%s) on '\
            '%s (%s). The new group is called %s and is %s.' %\
           (self.userInfo.name, self.userInfo.id,
            self.groupInfo.name, self.groupInfo.id,
            self.siteInfo.name, self.siteInfo.id,
            self.instanceDatum, self.supplementaryDatum)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event groupserver-group-start-%s' %\
          self.code
        retval = '<span class="%s">The %s group %s was started</span>' % \
                    (cssClass, self.supplementaryDatum, self.instanceDatum)
        retval = '%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class Auditor(object):
    def __init__(self, context, siteInfo):
        self.siteInfo = siteInfo
        self.context = context
        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code, adminInfo, groupInfo=None, instanceDatum='',
                supplementaryDatum=''):
        d = datetime.now(UTC)
        eventId = event_id_from_data(adminInfo, adminInfo,
            self.siteInfo, code, instanceDatum, supplementaryDatum)

        e = self.factory(self.context, eventId, code, d, adminInfo, None,
                self.siteInfo, groupInfo, instanceDatum, supplementaryDatum,
                SUBSYSTEM)

        self.queries.store(e)
        log.info(e)
