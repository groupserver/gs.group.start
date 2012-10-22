# coding=utf-8
from zope.interface import implements
from zope.component.interfaces import ObjectEvent
from zope.component.interfaces import IObjectEvent


class IGSGroupCreatedEvent(IObjectEvent):
    """ An event issued after a group has been created, and all core
        changes to the group have been made."""


class GSGroupCreatedEvent(ObjectEvent):
    implements(IGSGroupCreatedEvent)
