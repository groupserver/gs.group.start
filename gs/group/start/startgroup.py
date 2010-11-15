# coding=utf-8
try:
    from five.formlib.formbase import PageForm
except ImportError:
    from Products.Five.formlib.formbase import PageForm
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFCore.XWFUtils import getOption
from gs.group.member.join.interfaces import IGSJoiningUser
from gs.content.form.radio import radio_widget
from interfaces import IAboutGroup
from groupcreator import MoiraeForGroup

class StartGroupForm(PageForm):
    label = u'Start a Group'
    pageTemplateFileName = 'browser/templates/startgroup.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        PageForm.__init__(self, context, request)
        self.__siteInfo = self.__formFields = self.__emailDomain = None
        self.__loggedInUser = None
    
    @property
    def form_fields(self):
        if self.__formFields == None:
            self.__formFields = form.Fields(IAboutGroup, 
                                            render_context=False)
            self.__formFields['grpPrivacy'].custom_widget = radio_widget
        return self.__formFields        

    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = \
                createObject('groupserver.SiteInfo', self.context)
        return self.__siteInfo
    
    @property
    def loggedInUser(self):
        if self.__loggedInUser == None:
            self.__loggedInUser = createObject('groupserver.LoggedInUser', 
                                    self.context)
        return self.__loggedInUser
    @property
    def emailDomain(self):
        if self.__emailDomain == None:
            self.__emailDomain = getOption(self.context, 'emailDomain', '')
        return self.__emailDomain
    
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

