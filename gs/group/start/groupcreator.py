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
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.event import notify
from Products.GSGroup.groupInfo import GSGroupInfo
from Products.XWFCore.XWFUtils import add_marker_interfaces,\
    get_the_actual_instance_from_zope
from gs.core import to_ascii
from gs.group.privacy.interfaces import IGSChangePrivacy
from .audit import Auditor, START, STOP
from .groupfolder import GSGroupFolder
from .event import GSGroupCreatedEvent, GSGroupDeletedEvent

#--=mpj17=-- TODO: Figure out how much of this can be turned into a
# subscriber-based system.


class MoiraeForGroup(object):
    template = 'standard'

    def __init__(self, siteInfo):
        self.siteInfo = siteInfo

    @Lazy
    def groupsFolder(self):
        return getattr(self.siteInfo.siteObj, 'groups')

    @Lazy
    def site_root(self):
        retval = self.siteInfo.siteObj.aq_parent.aq_parent
        assert hasattr(retval, 'site_root'),\
            'No "site_root" in %s' % retval
        return retval

    def create(self, groupName, groupId, groupPrivacy, mailHost, adminInfo):
        if not groupName:
            raise ValueError('No group name')
        if not groupId:
            raise ValueError('No group identifier')
        if not isinstance(groupId, basestring):
            m = 'Group identifier a {0}, not a string'
            raise TypeError(m.format(type(groupId)))
        gid = to_ascii(groupId)

        if not groupPrivacy:
            raise ValueError('No group privacy')
        if not mailHost:
            raise ValueError('No mail host')
        if not adminInfo:
            raise ValueError('No administrator information')

        group = self.create_group_folder(gid.lower())
        self.set_security(group, adminInfo)
        self.create_administration(group)
        self.set_group_properties(group, groupName)
        self.create_list(group, mailHost)
        self.create_messages_area(group)
        self.create_files_area(group)
        self.set_group_privacy(group, groupPrivacy)

        notify(GSGroupCreatedEvent(group))

        groupInfo = GSGroupInfo(group)

        auditor = Auditor(self.site_root, self.siteInfo)
        auditor.info(START, adminInfo, groupInfo, groupName,
                     groupPrivacy)

        assert groupInfo
        return groupInfo

    def delete(self, context, groupId, adminInfo):
        if not groupId:
            raise ValueError('No group ID')
        if not isinstance(groupId, basestring):
            raise TypeError('groupId ({0}) is not a string'.format(groupId))
        gid = to_ascii(groupId)

        groupInfo = createObject('groupserver.GroupInfo', context, gid)

        notify(GSGroupDeletedEvent(groupInfo.groupObj))

        auditor = Auditor(self.site_root, self.siteInfo)
        auditor.info(STOP, adminInfo, groupInfo)

        self.delete_group_folder(gid)
        self.delete_user_group(gid)
        self.delete_list(gid)

    def create_group_folder(self, groupId):
        # Create the group folder
        ob = GSGroupFolder(groupId)
        self.groupsFolder._setObject(groupId, ob)
        group = getattr(self.groupsFolder, groupId)
        ifs = ['gs.group.type.discussion.interfaces.IGSDiscussionGroup']
        add_marker_interfaces(group, ifs)
        assert group
        return group

    def delete_group_folder(self, groupId):
        # Create the group folder
        self.groupsFolder.manage_delObjects([groupId, ])
        if hasattr(self.groupsFolder.aq_explicit, groupId):
            m = 'Tried to delete {0} but it remains'.format(groupId)
            raise AttributeError(m)

    def set_group_properties(self, group, groupName):
        # Set the correct properties
        group.manage_addProperty(b'is_group', True, b'boolean')
        group.manage_addProperty(b'short_name', groupName.lower(),
                                 b'string')
        rlg = 'people in %s' % groupName
        group.manage_addProperty(b'real_life_group', rlg, b'string')
        group.manage_addProperty(b'group_template', self.template,
                                 b'string')
        group.manage_changeProperties(title=groupName)

    def set_security(self, group, adminInfo):
        '''Set the Group Security

        Create the user-group, and create the GroupMember and GroupAdmin
        roles.'''
        # Secure the group
        memberGroup = to_ascii('%s_member' % group.getId())
        # Create the user-group
        self.site_root.acl_users.userFolderAddGroup(memberGroup)
        # Add the roles to the group
        group.manage_defined_roles(b'Add Role', {b'role': b'GroupMember'})
        group.manage_defined_roles(b'Add Role', {b'role': b'GroupAdmin'})
        # Associate the user-group with the group member role
        group.manage_addLocalGroupRoles(memberGroup, [b'GroupMember'])

        # Make the admin a group admin so he or she receives the
        #   Join notifications. See Ticket 611 for more information
        #   <https://projects.iopen.net/groupserver/ticket/611>
        group.manage_addLocalRoles(adminInfo.id, (b'GroupAdmin',))

    def delete_user_group(self, groupId):
        memberGroup = to_ascii('%s_member' % groupId)
        self.site_root.acl_users.userFolderDelGroups([memberGroup])

    def create_administration(self, group):
        assert group
        # In an OGN goup, group and site administrators can add users.
        gRoles = [b'DivisionAdmin', b'GroupAdmin', b'Manager', b'Owner']
        group.manage_permission(b'Manage users', gRoles, 0)
        # In an OGN goup, only site administrators can alter the properties
        siteRoles = [b'DivisionAdmin', b'Manager', b'Owner']
        group.manage_permission(b'Manage properties', siteRoles, 0)
        # Without the Add Page Templates permission the admin will not be
        #   able to add content!
        group.manage_permission(b'Add Page Templates', siteRoles, 0)
        group.manage_permission(b'Add Folders', siteRoles, 0)

    def create_list(self, group, mailhost):
        assert group, 'No group'
        assert mailhost, 'No mailhost'
        listManager = self.site_root.ListManager
        if hasattr(listManager.aq_explicit, group.getId()):
            m = 'The ListManager already has a list for "{0}".'.format(group.getId())
            raise ValueError(m)
        mailto = '%s@%s' % (group.getId(), mailhost)
        xwfmailingList = \
            listManager.manage_addProduct[b'XWFMailingListManager']
        xwfmailingList.manage_addXWFMailingList(group.getId(), mailto,
                                                group.title_or_id().lower())
        groupList = self.set_list_properties(group)
        return groupList

    def set_list_properties(self, group):
        listManager = self.site_root.ListManager
        if not hasattr(listManager.aq_explicit, group.getId()):
            m = 'The ListManager lacks a list for "{0}".'.format(group.getId())
            raise ValueError(m)
        groupList = getattr(listManager.aq_explicit, group.getId())
        groupList.manage_addProperty(b'siteId', self.siteInfo.id, b'string')
        groupList.manage_addProperty(b'use_rdb', True, b'boolean')
        # Delete the GroupServer 0.9 "archive", as it is now handled by the
        #   relational database.
        try:
            groupList.manage_delObjects([b'archive'])
        except:
            pass
        return groupList

    def delete_list(self, groupId):
        listManager = self.site_root.ListManager
        listManager.manage_delObjects([groupId, ])

    def create_messages_area(self, group):
        assert group
        xwfmail = group.manage_addProduct[b'XWFMailingListManager']
        xwfmail.manage_addXWFVirtualMailingListArchive2(b'messages',
                                                        'Messages')
        assert group.messages, \
            'Messages area not added to "s"' % group.getId()
        messages = group.messages
        messages.manage_changeProperties(
            xwf_mailing_list_manager_path=b'ListManager',
            xwf_mailing_list_ids=[group.getId()])

    def create_files_area(self, group):
        assert group
        xwffiles = group.manage_addProduct[b'XWFFileLibrary2']
        xwffiles.manage_addXWFVirtualFileFolder2(b'files', 'Files')
        assert hasattr(group.aq_explicit, 'files'), \
            'Files area not added to "%s"' % group.getId()

    def set_group_privacy(self, group, groupPrivacy):
        # Set the privacy: Which must be done **AFTER** the folder is
        #   made into a group
        if ((not hasattr(group, 'is_group')) or (not group.is_group)):
            raise TypeError('The group does not appear to be a group.')
        if not hasattr(group, 'messages'):
            raise AttributeError('No messages in the group.')

        g = get_the_actual_instance_from_zope(group)
        assert g
        gi = GSGroupInfo(g)
        assert gi.groupObj

        privacyChanger = IGSChangePrivacy(gi)
        if groupPrivacy == 'public':
            privacyChanger.set_group_public()
        elif groupPrivacy == 'private':
            privacyChanger.set_group_private()
        else:
            privacyChanger.set_group_secret()
