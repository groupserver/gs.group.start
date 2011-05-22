from zope.interface import implements, implementedBy
from OFS.Folder import Folder
from zope.component.interfaces import ObjectEvent
from zope.component.interfaces import IObjectEvent

from Products.XWFChat.interfaces import IGSGroupFolder

class GSGroupFolder(Folder):
    implements(IGSGroupFolder)

def groupAddedHandler(groupFolder, event):
    """ This is an example of how to handle the IObjectAdded event,
        for an IGSGroupFolder. See the configure.zcml for an example of
        how to subscribe to the event.
        
    """
    assert IGSGroupFolder.providedBy(groupFolder), \
       "groupFolder did not implement IGSGroupFolder!"
    
    return


class GSGroupAddedEvent(ObjectEvent):
    implements(IObjectEvent)
        
