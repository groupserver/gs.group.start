# coding=utf-8
import re
from zope.interface import Interface 
from zope.schema import Choice, TextLine, ASCIILine, ValidationError
from Products.GSGroup.interfacesprivacy import secruityVocab
from checkid import CheckId

ID_RE = r'^[a-zA-Z0-9-_]+$'
check_id = re.compile(ID_RE).match # --=mpj17=-- Mmmm, curry

class NotAValidGroupId(ValidationError):
    """Not a valid group identifier"""

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        retval = u'The text "%s" is not a valid group identifier. A '\
            u'group ID can only contain letters, numbers, dashes '\
            u'and underscores. Please pick another ID.' % self.value
        return retval
        
    def __str__(self):
        return unicode(self).encode('ascii', 'ignore')
         
    def doc(self):
        return self.__str__()

def id_used(context, groupId):
    idChecker = CheckId(context)
    retval = idChecker.exists(groupId)
    return retval

class GroupIdUsed(ValidationError):
    """Group identifier already used"""

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        retval = u'The identifier "%s" is already being used. Please ' \
            u'pick another ID.' % self.value
        return retval
        
    def __str__(self):
        return unicode(self).encode('ascii', 'ignore')
         
    def doc(self):
        return self.__str__()
        
class GroupId(ASCIILine):
    '''An group-ID entry.'''
    def constraint(self, value):
        if not(check_id(value)):
            raise NotAValidGroupId(value)
        elif id_used(self.context, value):
            raise GroupIdUsed(value)
        return True

class IAboutGroup(Interface):
    u'A Little About Your First Group'
    grpName = TextLine(title=u'Group Name',
                description=u'The name of your first group. You can '\
                    u'change it later',
                required=True)
                
    grpId = GroupId(title=u'Group ID',
                description=u'The identifier for your group. It '\
                    u'is used to create the URL and the email address '\
                    u'for the group. You can only change it now.',
                required=True)

    grpPrivacy = Choice(title=u'Group Privacy',
                    description=u'How visible the group, and the '\
                        u'group messages will be.',
                    vocabulary=secruityVocab,
                    default='public',
                    required=True)

