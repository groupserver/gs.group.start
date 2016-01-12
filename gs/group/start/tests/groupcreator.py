# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from mock import MagicMock, patch, call
from unittest import TestCase
from gs.group.start.groupcreator import (MoiraeForGroup, )


class MoiraeForGroupExceptionTest(TestCase):
    'Test the exceptions raised by the MoiraeForGroup class'

    def test_name_missing(self):
        m = MoiraeForGroup(MagicMock())
        with self.assertRaises(ValueError):
            m.create('', 'example', 'public', 'smtp.example.com', MagicMock())

    def test_id_missing(self):
        m = MoiraeForGroup(MagicMock())
        with self.assertRaises(ValueError):
            m.create('Example', '', 'public', 'smtp.example.com', MagicMock())

    def test_id_type(self):
        'Test that the group ID must be a string'
        m = MoiraeForGroup(MagicMock())
        with self.assertRaises(TypeError):
            m.create('Example', {'foo': 'bar'}, 'public', 'smtp.example.com', MagicMock())

    def test_privacy_missing(self):
        m = MoiraeForGroup(MagicMock())
        with self.assertRaises(ValueError):
            m.create('Example', 'example', '', 'smtp.example.com', MagicMock())

    def test_mailhost_missing(self):
        m = MoiraeForGroup(MagicMock())
        with self.assertRaises(ValueError):
            m.create('Example', 'example', 'public', '', MagicMock())

    def test_admin_missing(self):
        m = MoiraeForGroup(MagicMock())
        with self.assertRaises(ValueError):
            m.create('Example', 'example', 'public', 'smtp.example.com', None)

    def test_delete_group_id(self):
        m = MoiraeForGroup(MagicMock())
        with self.assertRaises(ValueError):
            m.delete(MagicMock(), '', MagicMock())

    def test_delete_group_id_type(self):
        'Test that the group ID for deleting a group must be a string'
        m = MoiraeForGroup(MagicMock())
        with self.assertRaises(TypeError):
            m.delete(MagicMock(), {'foo': 'bar'}, MagicMock())


class MoiraeForGroupFolderTest(TestCase):
    'Test the creating and deleting the group folder'

    @patch('gs.group.start.groupcreator.GSGroupFolder')
    @patch('gs.group.start.groupcreator.add_marker_interfaces')
    def test_create_group_folder(self, m_ami, m_GSGF):
        m = MoiraeForGroup(MagicMock())
        m.groupsFolder = MagicMock()

        r = m.create_group_folder('example')
        m_GSGF.assert_called_once_with('example')
        self.assertEqual(1, m.groupsFolder._setObject.call_count)
        self.assertEqual(m.groupsFolder.example, r)
        self.assertEqual(1, m_ami.call_count)

    def test_delete_group_folder(self):
        m = MoiraeForGroup(MagicMock())
        m.groupsFolder = MagicMock()
        del m.groupsFolder.aq_explicit.example

        m.delete_group_folder('example')
        m.groupsFolder.manage_delObjects.assert_called_once_with(['example'])

    def test_delete_group_folder_fail(self):
        m = MoiraeForGroup(MagicMock())
        m.groupsFolder = MagicMock()
        with self.assertRaises(AttributeError):
            m.delete_group_folder('example')


class MoiraeForGroupPropertiesTest(TestCase):
    'Tets for the group properties'

    def test_set_properties(self):
        m = MoiraeForGroup(MagicMock())
        folder = MagicMock()
        m.set_group_properties(folder, 'Example')

        calls = [
            call(b'is_group', True, b'boolean'),
            call(b'short_name', 'example', b'string'),  # Note: lower case "example"
            call(b'real_life_group', 'people in Example', b'string'),
            call(b'group_template', b'standard', b'string'), ]
        folder.manage_addProperty.assert_has_calls(calls)
        folder.manage_changeProperties.assert_called_with(title='Example')

    def test_set_security(self):
        m = MoiraeForGroup(MagicMock())
        m.site_root = MagicMock()
        folder = MagicMock()
        folder.getId.return_value = 'example'
        adminInfo = MagicMock()
        adminInfo.id = 'an_admin'
        m.set_security(folder, adminInfo)

        m.site_root.acl_users.userFolderAddGroup.assert_called_with('example_member')
        self.assertEqual(2, folder.manage_defined_roles.call_count)
        folder.manage_addLocalGroupRoles.assert_called_with(b'example_member', [b'GroupMember', ])
        folder.manage_addLocalRoles.assert_called_with('an_admin', (b'GroupAdmin', ))

    def test_del_user_group(self):
        m = MoiraeForGroup(MagicMock())
        m.site_root = MagicMock()
        m.delete_user_group('example')

        m.site_root.acl_users.userFolderDelGroups.assert_called_with([b'example_member'])

    def test_create_administration(self):
        m = MoiraeForGroup(MagicMock())
        folder = MagicMock()
        m.create_administration(folder)

        calls = [
            call(b'Manage users', [b'DivisionAdmin', b'GroupAdmin', b'Manager', b'Owner'], 0),
            call(b'Manage properties', [b'DivisionAdmin', b'Manager', b'Owner'], 0),
            call(b'Add Page Templates', [b'DivisionAdmin', b'Manager', b'Owner'], 0),
            call(b'Add Folders', [b'DivisionAdmin', b'Manager', b'Owner'], 0), ]
        folder.manage_permission.assert_has_calls(calls)


class MoiraeForGroupListTest(TestCase):
    'Tests for the mailing-list objects'

    @patch.object(MoiraeForGroup, 'set_list_properties')
    def test_create_list(self, m_slp):
        m = MoiraeForGroup(MagicMock())
        m.site_root = MagicMock()
        del m.site_root.ListManager.aq_explicit.example  # So we do not throw a ValueError
        folder = MagicMock()
        folder.getId.return_value = 'example'
        folder.title_or_id.return_value = 'Example'
        m.create_list(folder, 'example.com')

        m_ap = m.site_root.ListManager.manage_addProduct[b'XWFMailingListManager']
        m_ap.manage_addXWFMailingList.assert_called_once_with(
            'example', 'example@example.com', 'example')
        m_slp.assert_called_once_with(folder)

    def test_set_list_poperties(self):
        m = MoiraeForGroup(MagicMock())
        m.site_root = MagicMock()
        m.siteInfo = MagicMock()
        m.siteInfo.id = 'example_site'
        folder = MagicMock()
        folder.getId.return_value = 'example'
        folder.title_or_id.return_value = 'Example'
        m.set_list_properties(folder)

        l = m.site_root.ListManager.aq_explicit.example
        calls = [
            call(b'siteId', 'example_site', b'string'),
            call(b'use_rdb', True, b'boolean'), ]
        l.manage_addProperty.assert_has_calls(calls)
        l.manage_delObjects.assert_called_once_with([b'archive'])

    def test_create_list_exists(self):
        'Test that we cannot create an existing list'
        m = MoiraeForGroup(MagicMock())
        m.site_root = MagicMock()
        folder = MagicMock()
        folder.getId.return_value = 'example'
        # The MagicMock will automatically provide the site_root.ListManger.example attribute
        with self.assertRaises(ValueError):
            m.create_list(folder, 'example.com')

    def test_delete_list(self):
        m = MoiraeForGroup(MagicMock())
        m.site_root = MagicMock()
        m.delete_list('example')

        m.site_root.ListManager.manage_delObjects.assert_called_once_with(['example', ])


class MoiraeForGroupFilesMessagesTest(TestCase):
    'Tests for the files and messages folders'
    def test_create_messages(self):
        folder = MagicMock()
        folder.getId.return_value = 'example'
        m = MoiraeForGroup(MagicMock())
        m.create_messages_area(folder)

        m_ap = folder.manage_addProduct[b'XWFMailingListManager']
        m_ap.manage_addXWFVirtualMailingListArchive2.assert_called_once_with(
            b'messages', 'Messages')
        folder.messages.manage_changeProperties.assert_called_once_with(
            xwf_mailing_list_manager_path=b'ListManager',
            xwf_mailing_list_ids=['example'])

    def test_create_files(self):
        folder = MagicMock()
        folder.getId.return_value = 'example'
        m = MoiraeForGroup(MagicMock())
        m.create_files_area(folder)

        m_ap = folder.manage_addProduct[b'XWFFileLibrary2']
        m_ap.manage_addXWFVirtualFileFolder2.assert_called_once_with(
            b'files', 'Files')


class MoiraeForGroupPrivacyTest(TestCase):

    @patch('gs.group.start.groupcreator.IGSChangePrivacy')
    @patch('gs.group.start.groupcreator.get_the_actual_instance_from_zope')
    @patch('gs.group.start.groupcreator.GSGroupInfo')
    def test_set_privacy_public(self, m_GSGI, m_gaifz, m_IGSCP):
        m = MoiraeForGroup(MagicMock())
        folder = MagicMock()
        m.set_group_privacy(folder, 'public')

        changer = m_IGSCP()
        changer.set_group_public.assert_called_once_with()

    @patch('gs.group.start.groupcreator.IGSChangePrivacy')
    @patch('gs.group.start.groupcreator.get_the_actual_instance_from_zope')
    @patch('gs.group.start.groupcreator.GSGroupInfo')
    def test_set_privacy_private(self, m_GSGI, m_gaifz, m_IGSCP):
        m = MoiraeForGroup(MagicMock())
        folder = MagicMock()
        m.set_group_privacy(folder, 'private')

        changer = m_IGSCP()
        changer.set_group_private.assert_called_once_with()

    @patch('gs.group.start.groupcreator.IGSChangePrivacy')
    @patch('gs.group.start.groupcreator.get_the_actual_instance_from_zope')
    @patch('gs.group.start.groupcreator.GSGroupInfo')
    def test_set_privacy_secret(self, m_GSGI, m_gaifz, m_IGSCP):
        m = MoiraeForGroup(MagicMock())
        folder = MagicMock()
        m.set_group_privacy(folder, 'secret')

        changer = m_IGSCP()
        changer.set_group_secret.assert_called_once_with()

    def test_set_privacy_not_group(self):
        'Test setting the privacy for something that is not a group'
        m = MoiraeForGroup(MagicMock())
        folder = MagicMock()
        del folder.is_group

        with self.assertRaises(TypeError):
            m.set_group_privacy(folder, 'example')

    def test_set_privacy_group_false(self):
        'Test setting the privacy for something that is explicitly not a group'
        m = MoiraeForGroup(MagicMock())
        folder = MagicMock()
        folder.is_group = False

        with self.assertRaises(TypeError):
            m.set_group_privacy(folder, 'example')

    def test_set_privacy_group_no_messages(self):
        'Test setting the privacy for a group that lacks the messasges object'
        m = MoiraeForGroup(MagicMock())
        folder = MagicMock()
        del folder.messages

        with self.assertRaises(AttributeError):
            m.set_group_privacy(folder, 'example')
