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
from mock import MagicMock, call, patch
from unittest import TestCase
from gs.group.start.checkid import (CheckId, )


class CheckIdUserTest(TestCase):

    def test_existing_user(self):
        'Check that an existing user check returns True'
        context = MagicMock()
        ho = context.acl_users.hasObject
        ho.return_value = True
        c = CheckId(context)

        r = c.existing_user('example')
        self.assertTrue(r)
        ho.assert_called_once_with('example')

    def test_existing_user_lower(self):
        'Check that an existing user check is case-insensitive'
        context = MagicMock()
        ho = context.acl_users.hasObject
        ho.side_effect = (False, True)
        c = CheckId(context)

        r = c.existing_user('Example')
        self.assertTrue(r)
        self.assertEqual(2, ho.call_count)
        calls = [call('Example',), call('example', )]
        ho.assert_has_calls(calls)

    def test_existing_user_missing(self):
        'Check an existing user being missing'
        context = MagicMock()
        ho = context.acl_users.hasObject
        ho.side_effect = (False, False)
        c = CheckId(context)

        r = c.existing_user('example')
        self.assertFalse(r)
        self.assertEqual(2, ho.call_count)


class CheckIdSiteTest(TestCase):
    def test_existing_site(self):
        'Check that an existing site check returns True'
        context = MagicMock()
        ho = context.Content.hasObject
        ho.return_value = True
        c = CheckId(context)

        r = c.existing_site('example')
        self.assertTrue(r)
        ho.assert_called_once_with('example')

    def test_existing_site_lower(self):
        'Check that an existing site check is case-insensitive'
        context = MagicMock()
        ho = context.Content.hasObject
        ho.side_effect = (False, True)
        c = CheckId(context)

        r = c.existing_site('Example')
        self.assertTrue(r)
        self.assertEqual(2, ho.call_count)
        calls = [call('Example',), call('example', )]
        ho.assert_has_calls(calls)

    def test_existing_site_missing(self):
        'Check an existing site being missing'
        context = MagicMock()
        ho = context.Content.hasObject
        ho.side_effect = (False, False)
        c = CheckId(context)

        r = c.existing_site('example')
        self.assertFalse(r)


class CheckIdGroupTest(TestCase):
    def test_existing_group(self):
        'Check that an existing group check returns True'
        context = MagicMock()
        ho = context.ListManager.hasObject
        ho.return_value = True
        c = CheckId(context)

        r = c.existing_group('example')
        self.assertTrue(r)
        ho.assert_called_once_with('example')

    def test_existing_group_lower(self):
        'Check that an existing group check is case-insensitive'
        context = MagicMock()
        ho = context.ListManager.hasObject
        ho.side_effect = (False, True)
        c = CheckId(context)

        r = c.existing_group('Example')
        self.assertTrue(r)
        self.assertEqual(2, ho.call_count)
        calls = [call('Example',), call('example', )]
        ho.assert_has_calls(calls)

    def test_existing_group_missing(self):
        'Check an existing group being missing'
        context = MagicMock()
        ho = context.ListManager.hasObject
        ho.side_effect = (False, False)
        c = CheckId(context)

        r = c.existing_group('example')
        self.assertFalse(r)


class CheckIdExistsCheck(TestCase):

    @patch.object(CheckId, 'existing_group')
    @patch.object(CheckId, 'existing_site')
    @patch.object(CheckId, 'existing_user')
    def test_group(self, m_eu, m_es, m_eg):
        m_eg.return_value = True
        m_es.return_value = False
        m_eu.return_value = False
        context = MagicMock()
        c = CheckId(context)

        r = c.exists('example')
        self.assertTrue(r)

    @patch.object(CheckId, 'existing_group')
    @patch.object(CheckId, 'existing_site')
    @patch.object(CheckId, 'existing_user')
    def test_site(self, m_eu, m_es, m_eg):
        m_eg.return_value = False
        m_es.return_value = True
        m_eu.return_value = False
        context = MagicMock()
        c = CheckId(context)

        r = c.exists('example')
        self.assertTrue(r)

    @patch.object(CheckId, 'existing_group')
    @patch.object(CheckId, 'existing_site')
    @patch.object(CheckId, 'existing_user')
    def test_user(self, m_eu, m_es, m_eg):
        m_eg.return_value = False
        m_es.return_value = False
        m_eu.return_value = True
        context = MagicMock()
        c = CheckId(context)

        r = c.exists('example')
        self.assertTrue(r)

    @patch.object(CheckId, 'existing_group')
    @patch.object(CheckId, 'existing_site')
    @patch.object(CheckId, 'existing_user')
    def test_none(self, m_eu, m_es, m_eg):
        m_eg.return_value = False
        m_es.return_value = False
        m_eu.return_value = False
        context = MagicMock()
        c = CheckId(context)

        r = c.exists('example')
        self.assertFalse(r)
