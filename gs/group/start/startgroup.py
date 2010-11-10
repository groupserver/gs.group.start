# coding=utf-8
try:
    from five.formlib.formbase import PageForm
except ImportError:
    from Products.Five.formlib.formbase import PageForm
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.radio import radio_widget
from interfaces import IAboutGroup
from groupcreator import MoiraeForGroup

class StartGroupForm(PageForm):
    label = u'Start a Group'
    pageTemplateFileName = 'browser/templates/startgroup.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        PageForm.__init__(self, context, request)
        self.__siteInfo = self.__formFields = None

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
    
    @form.action(label=u'Start', failure='handle_start_action_failure')
    def handle_start(self, action, data):
        self.status = u'This should do stuff'
        
    def handle_start_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'

