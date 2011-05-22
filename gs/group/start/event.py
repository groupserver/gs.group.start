from zope.interface import implements, implementedBy
from OFS.Folder import Folder
from zope.component.interfaces import ObjectEvent
from zope.component.interfaces import IObjectEvent

from Products.XWFChat.interfaces import IGSGroupFolder

class IGSGroupCreatedEvent(IObjectEvent):
    """ An event issued after a group has been created, and all core changes
        to the group have been made.

    """

class GSGroupCreatedEvent(ObjectEvent):
    implements(IGSGroupCreatedEvent)
        
