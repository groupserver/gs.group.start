# coding=utf-8
from pytz import UTC
from datetime import datetime
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from Products.GSGroup.groupInfo import groupInfo_to_anchor
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
    AuditQuery, event_id_from_data
from Products.XWFCore.XWFUtils import munge_date,\
    get_the_actual_instance_from_zope
    
SUBSYSTEM = 'gs.group.start'
import logging
log = logging.getLogger(SUBSYSTEM) #@UndefinedVariable

UNKNOWN      = '0'
START        = '1'
START_FAILED = '2'

class AuditEventFactory(object):
    implements(IFactory)

    title=u'Group Start Audit-Event Factory'
    description=u'Creates a GroupServer audit event for starting a group'

    def __call__(self, context, event_id,  code, date,
        userInfo, instanceUserInfo,  siteInfo,  groupInfo=None,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        if code == START:
          event = StartEvent(context, event_id, date, userInfo,
            siteInfo, groupInfo, instanceDatum, supplementaryDatum)
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
        BasicAuditEvent.__init__(self, context, id,  START, d, 
            adminInfo, None, siteInfo, groupInfo, name, privacy, 
            SUBSYSTEM)
          
    def __str__(self):
        retval = u'%s (%s) started the group %s (%s) on '\
            u'%s (%s). The new group is called %s and is %s.' %\
           (self.userInfo.name,         self.userInfo.id,
            self.groupInfo.name,        self.groupInfo.id,
            self.siteInfo.name,         self.siteInfo.id,
            self.instanceDatum,         self.supplementaryDatum)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event groupserver-group-start-%s' %\
          self.code
        retval = u'<span class="%s">The %s group %s was started</span>' % \
                    (cssClass, self.supplementaryDatum, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class Auditor(object):
    def __init__(self, context, siteInfo):
        self.siteInfo = siteInfo
        self.context = context
        da = context.zsqlalchemy
        self.queries = AuditQuery(da)
        self.factory = AuditEventFactory()
        
    def info(self, code, adminInfo, groupInfo=None, instanceDatum = '', 
                supplementaryDatum = ''):
        d = datetime.now(UTC)
        eventId = event_id_from_data(adminInfo, adminInfo,
            self.siteInfo, code, instanceDatum, supplementaryDatum)
          
        e = self.factory(self.context, eventId,  code, d, 
                adminInfo,  None, self.siteInfo, groupInfo, 
                instanceDatum, supplementaryDatum, SUBSYSTEM)
          
        self.queries.store(e)
        log.info(e)

