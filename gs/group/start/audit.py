# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014, 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
from logging import getLogger
SUBSYSTEM = 'gs.group.start'
log = getLogger(SUBSYSTEM)
from random import SystemRandom
from zope.component.interfaces import IFactory
from zope.interface import implementedBy, implementer
from gs.core import to_id, to_unicode_or_bust, curr_time as now
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, AuditQuery
from Products.XWFCore.XWFUtils import munge_date

UNKNOWN = '0'
START = '1'
START_FAILED = '2'
STOP = '3'


@implementer(IFactory)
class AuditEventFactory(object):
    title = 'Group Start Audit-Event Factory'
    description = 'Creates a GroupServer audit event for starting a group'

    def __call__(self, context, event_id, code, date, userInfo,
                 instanceUserInfo, siteInfo, groupInfo=None,
                 instanceDatum='', supplementaryDatum='', subsystem=''):
        if code == START:
            event = StartEvent(context, event_id, date, userInfo, siteInfo,
                               groupInfo, instanceDatum, supplementaryDatum)
        if code == STOP:
            event = StopEvent(context, event_id, date, userInfo, siteInfo,
                              groupInfo)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
                                    userInfo, instanceUserInfo, siteInfo,
                                    groupInfo, instanceDatum,
                                    supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


@implementer(IAuditEvent)
class StartEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person starting a group.'''

    def __init__(self, context, id, d, adminInfo, siteInfo, groupInfo,
                 name, privacy):
        super(StartEvent, self).__init__(
            context, id, START, d, adminInfo, None, siteInfo, groupInfo,
            name, privacy, SUBSYSTEM)

    def __unicode__(self):
        retval = '%s (%s) started the group %s (%s) on '\
                 '%s (%s). The new group is called %s and is %s.' %\
            (self.userInfo.name, self.userInfo.id, self.groupInfo.name,
             self.groupInfo.id, self.siteInfo.name, self.siteInfo.id,
             self.instanceDatum, self.supplementaryDatum)
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-group-start-%s' % self.code
        retval = '<span class="%s">The %s group %s was started</span>' % \
            (cssClass, self.supplementaryDatum, self.instanceDatum)
        retval = '%s (%s)' % (retval, munge_date(self.context, self.date))
        return retval


@implementer(IAuditEvent)
class StopEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person stopping a group.'''
    def __init__(self, context, id, d, adminInfo, siteInfo, groupInfo):
        super(StopEvent, self).__init__(
            context, id, START, d, adminInfo, None, siteInfo, groupInfo,
            None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = '%s (%s) stoped the group %s (%s) on %s (%s)' %\
            (self.userInfo.name, self.userInfo.id, self.groupInfo.name,
             self.groupInfo.id, self.siteInfo.name, self.siteInfo.id)
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-group-start-%s' % self.code
        retval = '<span class="%s">The group %s was stopped</span>' % \
            (cssClass, self.groupInfo.name)
        retval = '%s (%s)' % (retval, munge_date(self.context, self.date))
        return retval


class Auditor(object):
    def __init__(self, context, siteInfo):
        self.siteInfo = siteInfo
        self.context = context
        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code, adminInfo, groupInfo=None, instanceDatum='',
             supplementaryDatum=''):
        d = now()
        eventId = to_id(to_unicode_or_bust(adminInfo.id)
                        + unicode(d)
                        + unicode(SystemRandom().randint(0, 1024))
                        + to_unicode_or_bust(adminInfo.name)
                        + to_unicode_or_bust(self.siteInfo.id)
                        + to_unicode_or_bust(self.siteInfo.name)
                        + to_unicode_or_bust(code)
                        + to_unicode_or_bust(instanceDatum)
                        + to_unicode_or_bust(supplementaryDatum))

        e = self.factory(self.context, eventId, code, d, adminInfo, None,
                         self.siteInfo, groupInfo, instanceDatum,
                         supplementaryDatum, SUBSYSTEM)
        self.queries.store(e)
        log.info(e)
