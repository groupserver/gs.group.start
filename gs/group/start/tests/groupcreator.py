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
    'Test the creating and deleting the folder'

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
