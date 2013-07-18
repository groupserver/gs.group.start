# -*- coding: utf-8 -*-
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFCore.XWFUtils import getOption
from gs.content.form import SiteForm
from gs.group.member.join.interfaces import IGSJoiningUser
from gs.content.form.radio import radio_widget
from interfaces import IAboutGroup
from groupcreator import MoiraeForGroup


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
        joiningUser.join(newGroup)

        self.request.RESPONSE.redirect(newGroup.relative_url())

        self.status = u'The group <a href="%s">%s</a> has been started.' %\
            (newGroup.relative_url(), newGroup.name)

    def handle_start_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
