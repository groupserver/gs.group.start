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
from mock import MagicMock, patch
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
