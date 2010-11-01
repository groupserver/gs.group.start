# coding=utf-8
from Products.Five import BrowserView

class CheckIdForm(BrowserView):
    def __init__(self, site, request):
        BrowserView.__init__(self, site, request)
        self.idToCheck = request['id']
        
    def __call__(self):
        checker = CheckId(self.context)
        return checker.exists(self.idToCheck) and '1' or '0'

class CheckId(object):

    def __init__(self, context):
        self.context = context
        
    def exists(self, idToCheck):
        return self.existing_group(idToCheck)\
            or self.existing_site(idToCheck)\
            or self.existing_user(idToCheck)
            
    def existing_group(self, groupId):
        listManager = self.context.ListManager
        return groupId in listManager.objectIds()

    def existing_site(self, siteId):
        content = self.context.Content
        return siteId in content.objectIds()

    def existing_user(self, userId):
        acl_users = self.context.acl_users
        return userId in acl_users.getUserNames()

