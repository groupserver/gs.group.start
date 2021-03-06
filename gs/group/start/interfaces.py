# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
import re
from zope.interface import Interface
from zope.schema import Choice, TextLine, ASCIILine, ValidationError
from gs.core import to_ascii
from Products.GSGroup.interfacesprivacy import secruityVocab
from .checkid import CheckId
from . import GSMessageFactory as _

ID_RE = r'^[a-zA-Z0-9-_]+$'
check_id = re.compile(ID_RE).match  # --=mpj17=-- Mmmm, curry


class NotAValidGroupId(ValidationError):
    """Not a valid group identifier"""

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        retval = _(
            'invalid-id-msg',
            'The text "${id}" is not a valid group identifier. A group ID '
            'can only contain letters, numbers, dashes and underscores. '
            'Please pick another ID.', mapping={'id': self.value})
        return retval

    def __str__(self):
        retval = to_ascii(unicode(self))
        return retval

    def doc(self):
        return str(self)


def id_used(context, groupId):
    idChecker = CheckId(context)
    retval = idChecker.exists(groupId)
    return retval


class GroupIdUsed(ValidationError):
    """Group identifier already used"""

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        retval = _(
            'used-id-msg',
            'The identifier "${id}" is already being used. Please pick '
            'another ID.', mapping={'id': self.value})
        return retval

    def __str__(self):
        return to_ascii(unicode(self))

    def doc(self):
        return str(self)


class GroupId(ASCIILine):
    '''An group-ID entry.'''
    def constraint(self, value):
        if not(check_id(value)):
            raise NotAValidGroupId(value)
        elif id_used(self.context, value):
            raise GroupIdUsed(value)
        return True


class IAboutGroup(Interface):
    'A Little About Your First Group'
    grpName = TextLine(
        title=_('group-name-label', 'Group name'),
        description=_('group-name-help',
                      'The name of your first group. You can change it '
                      'later'),
        required=True)

    grpId = GroupId(
        title=_('group-id-label', 'Group ID'),
        description=_('group-id-help',
                      'The identifier for your group. It is used to create '
                      'the URL and the email address for the group. You '
                      'can only change it now.'),
        required=True)

    grpPrivacy = Choice(
        title=_('group-privacy-label', 'Group Privacy'),
        description=_('group-privacy-help',
                      'How visible the group, and the group messages will '
                      'be.'),
        vocabulary=secruityVocab,
        default='private',
        required=True)
