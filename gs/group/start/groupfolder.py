# coding=utf-8
from zope.interface import implements, implementedBy
from OFS.Folder import Folder
from zope.component.interfaces import ObjectEvent
from zope.component.interfaces import IObjectEvent
from gs.group.base.interfaces import IGSGroupMarker
from gs.group.type.discussion.interfaces import IGSDiscussionGroup

# Standard group folder
class GSGroupFolder(Folder):
    implements(IGSDiscussionGroup)

# Group Added Event
class GSGroupAddedEvent(ObjectEvent):
    implements(IObjectEvent)

def groupAddedHandler(groupFolder, event):
    """ This is an example of how to handle the IObjectAdded event,
        for an IGSGroupFolder. See the configure.zcml for an example of
        how to subscribe to the event.
        
    """
    assert IGSGroupMarker.providedBy(groupFolder), \
       "groupFolder did not implement IGSGroupMarker!"
    
    return

