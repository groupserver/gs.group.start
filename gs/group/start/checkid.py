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
        # Group IDs must be unique *ignoring* case, because the ID is
        #   used as the email address.
        listManager = self.context.ListManager
        ids = [lid.lower() for lid in listManager.objectIds()]
        return groupId.lower() in ids

    def existing_site(self, siteId):
        # Having a group with the same ID as a site may cause issues, so
        #   we ban it.
        ids = [sid.lower() for sid in self.context.Content.objectIds()]
        return siteId.lower() in ids

    def existing_user(self, userId):
        # A group with the same ID as a user is unlkely to cause issues,
        #   but ban it just in case
        acl_users = self.context.acl_users
        return userId in acl_users.getUserNames()

