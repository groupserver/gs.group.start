# coding=utf-8
from zope.interface import Interface 
from zope.schema import Choice, TextLine, ASCIILine
from Products.GSGroup.interfacesprivacy import secruityVocab

class IAboutGroup(Interface):
    u'A Little About Your First Group'
    grpName = TextLine(title=u'Group Name',
                description=u'The name of your first group. You can '\
                    u'change it later',
                required=True)
                
    grpId = ASCIILine(title=u'Group ID',
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

