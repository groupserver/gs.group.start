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
from __future__ import absolute_import
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form import SiteForm, radio_widget
from gs.group.member.join.interfaces import IGSJoiningUser
from Products.XWFCore.XWFUtils import getOption
from .groupcreator import MoiraeForGroup
from .interfaces import IAboutGroup
from .notify import StartNotifier


class StartGroupForm(SiteForm):
    label = u'Start a group'
    pageTemplateFileName = 'browser/templates/startgroup.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        super(StartGroupForm, self).__init__(context, request)

    @Lazy
    def form_fields(self):
        retval = form.Fields(IAboutGroup, render_context=False)
        retval['grpPrivacy'].custom_widget = radio_widget
        return retval

    @Lazy
    def emailDomain(self):
        retval = getOption(self.context, 'emailDomain', '')
        return retval

    @form.action(label=u'Start', failure='handle_start_action_failure')
    def handle_start(self, action, data):
        groupMoirae = MoiraeForGroup(self.siteInfo)
        newGroup = groupMoirae.create(data['grpName'], data['grpId'],
                              data['grpPrivacy'], self.emailDomain,
                              self.loggedInUser)

        joiningUser = IGSJoiningUser(self.loggedInUser)
        joiningUser.silent_join(newGroup)

        notifier = StartNotifier(newGroup.groupObj, self.request)
        for adminInfo in self.siteInfo.site_admins:
            notifier.notify(adminInfo)

        self.request.RESPONSE.redirect(newGroup.relative_url())
        self.status = u'The group <a href="%s">%s</a> has been started.' %\
            (newGroup.relative_url(), newGroup.name)

    def handle_start_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
