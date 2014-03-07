# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import unicode_literals
from gs.content.form import SiteForm
from gs.core import to_ascii


class CheckIdForm(SiteForm):

    def __init__(self, site, request):
        super(CheckIdForm, self).__init__(site, request)
        self.idToCheck = request['id']

    def __call__(self):
        checker = CheckId(self.context)
        r = '1' if checker.exists(self.idToCheck) else '0'
        retval = to_ascii(r)
        return retval


class CheckId(object):

    def __init__(self, context):
        self.context = context

    def exists(self, idToCheck):
        retval = (self.existing_group(idToCheck)
                    or self.existing_site(idToCheck)
                    or self.existing_user(idToCheck))
        assert type(retval) == bool
        return retval

    def existing_group(self, groupId):
        # Group IDs must be unique *ignoring* case, because the ID is
        #   used as the email address.
        listManager = self.context.ListManager
        retval = (listManager.hasObject(groupId)
                    or listManager.hasObject(groupId.lower()))
        assert type(retval) == bool
        return retval

    def existing_site(self, siteId):
        # Having a group with the same ID as a site may cause issues, so
        #   we ban it.
        content = self.context.Content
        retval = (content.hasObject(siteId)
                    or content.hasObject(siteId.lower()))
        assert type(retval) == bool
        return retval

    def existing_user(self, userId):
        # A group with the same ID as a user is unlkely to cause issues,
        #   but ban it just in case
        acl_users = self.context.acl_users
        retval = (acl_users.hasObject(userId)
                    or acl_users.hasObject(userId.lower()))
        assert type(retval) == bool
        return retval
