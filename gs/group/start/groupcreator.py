# coding=utf-8
from Products.GSGroup.groupInfo import GSGroupInfo
from Products.XWFCore.XWFUtils import add_marker_interfaces,\
    get_the_actual_instance_from_zope
from gs.group.privacy.interfaces import IGSChangePrivacy
from audit import Auditor, START

class MoiraeForGroup(object):
    template = 'standard'
    
    def __init__(self, siteInfo):
        self.siteInfo = siteInfo

    @property
    def groupsFolder(self):
        return getattr(self.siteInfo.siteObj, 'groups')

    @property
    def site_root(self):
        retval = self.siteInfo.siteObj.aq_parent.aq_parent
        assert hasattr(retval, 'site_root'),\
            'No "site_root" in %s' % retval
        return retval

    def create(self, groupName, groupId, groupPrivacy, mailHost, adminInfo):
        assert groupName, 'No group name'
        assert groupId, 'No group ID'
        assert groupPrivacy, 'No group privacy'
        assert adminInfo, 'No admin'
        
        if type(groupId) == unicode:
            groupId = groupId.encode('ascii', 'ignore')        
                
        group = self.create_group_folder(groupId)
        self.set_security(group)
        self.add_marker(group)
        self.create_administration(group)
        self.set_group_properties(group, groupName)
        self.create_list(group, mailHost)
        self.create_messages_area(group)
        self.create_files_area(group)
        self.set_group_privacy(group, groupPrivacy)
        
        groupInfo = GSGroupInfo(group)
        
        auditor = Auditor(self.site_root, self.siteInfo)
        auditor.info(START, adminInfo, groupInfo, groupName, 
                        groupPrivacy)

        assert groupInfo
        return groupInfo

    def delete(self, groupId):
        assert groupId, 'No group ID'
        
        if type(groupId) == unicode:
            groupId = groupId.encode('ascii', 'ignore')        

        self.delete_group_folder(groupId)
        self.delete_user_group(groupId)
        self.delete_list(groupId)

    def create_group_folder(self, groupId):
        # Create the group folder
        self.groupsFolder.manage_addFolder(groupId)
        group = getattr(self.groupsFolder, groupId)
        assert group
        return group

    def delete_group_folder(self, groupId):
        # Create the group folder
        self.groupsFolder.manage_delObjects([groupId,])
        assert not(hasattr(self.groupsFolder, groupId))

    def set_group_properties(self, group, groupName):
        # Set the correct properties
        group.manage_addProperty('is_group', True, 'boolean')
        group.manage_addProperty('short_name', groupName.lower(), 'string')
        rlg = 'people in %s' % groupName
        group.manage_addProperty('real_life_group', rlg, 'string')
        group.manage_addProperty('group_template', self.template, 'string')
        group.manage_changeProperties(title=groupName)

    def set_security(self, group):
        '''\
        Set the Group Security
        
        Create the user-group, and create the GroupMember and GroupAdmin
        roles.'''
        # Secure the group
        memberGroup = '%s_member' % group.getId()
        # Create the user-group
        self.site_root.acl_users.userFolderAddGroup(memberGroup)
        # Add the roles to the group
        group.manage_defined_roles('Add Role', {'role':'GroupMember'})
        group.manage_defined_roles('Add Role', {'role':'GroupAdmin'})
        # Associate the user-group with the group member role
        group.manage_addLocalGroupRoles(memberGroup, ['GroupMember'])

    def delete_user_group(self, groupId):
        memberGroup = '%s_member' % groupId
        self.site_root.acl_users.userFolderDelGroups([memberGroup])

    def add_marker(self, group):
        # Add the IGSGroupFolder, so the Zope Five pages work!
        interfaces = ('Products.XWFChat.interfaces.IGSGroupFolder',)
        add_marker_interfaces(group, interfaces)        

    def create_administration(self, group):
        assert group
        fss = group.manage_addProduct['FileSystemSite']
        fss.manage_addDirectoryView('GroupServer/admingroup')

        # In an OGN goup, group and site administrators can add users.
        group.manage_permission('Manage users', 
                                ['DivisionAdmin','GroupAdmin','Manager','Owner'],0)
        # In an OGN goup, only site administrators can alter the properties
        group.manage_permission('Manage properties', 
                                ['DivisionAdmin','Manager','Owner'],0)
        # Without the Add XML Template permission the admin will not be
        #   able to paste the content_en in!
        group.manage_permission('Add XML Template', 
                                ['DivisionAdmin','Manager','Owner'],0)
        group.manage_permission('Add Folders', 
                                ['DivisionAdmin','Manager','Owner'],0)
        assert hasattr(group.aq_explicit, 'admingroup')
                
    def create_list(self, group, mailhost):
        assert group, 'No group'
        assert mailhost, 'No mailhost'
        listManager = self.site_root.ListManager
        assert not(hasattr(listManager.aq_explicit, group.getId())), \
            'The ListManager already has a list for "%s".' % group.getId()
        mailto = '%s@%s' % (group.getId(), mailhost)
        xwfmailingList = listManager.manage_addProduct['XWFMailingListManager']
        xwfmailingList.manage_addXWFMailingList(group.getId(), mailto, 
                                                group.title_or_id().lower())
        assert hasattr(listManager.aq_explicit, group.getId()), \
            'The list "%s" was not created in ListManager.' % group.getId()

        groupList = getattr(self.site_root.ListManager.aq_explicit, group.getId())
        groupList.manage_addProperty('siteId', self.siteInfo.id, 'string')
        groupList.manage_addProperty('use_rdb', True, 'boolean')
        # Delete the GroupServer 0.9 "archive", as it is now handled by the 
        #   relational database.
        try:
            groupList.manage_delObjects(['archive'])
        except:
            pass
        return groupList
        
    def delete_list(self, groupId):
        listManager = self.site_root.ListManager
        listManager.manage_delObjects([groupId,])
        
    def create_messages_area(self, group):
        assert group
        xwfmail = group.manage_addProduct['XWFMailingListManager']
        xwfmail.manage_addXWFVirtualMailingListArchive2('messages', 'Messages')
        assert group.messages, 'Messages area not added to "s"' % group.getId()
        messages = group.messages
        messages.manage_changeProperties(xwf_mailing_list_manager_path='ListManager',
                                         xwf_mailing_list_ids=[group.getId()])

    def create_files_area(self, group):
        assert group
        xwffiles = group.manage_addProduct['XWFFileLibrary2']
        xwffiles.manage_addXWFVirtualFileFolder2('files', 'Files')
        assert hasattr(group.aq_explicit, 'files'), \
          'Files area not added to "%s"' % group.getId()
    
    def set_group_privacy(self, group, groupPrivacy):
        assert hasattr(group, 'is_group')
        assert group.is_group
        assert hasattr(group, 'messages')
        # Set the privacy: Which must be done **AFTER** the folder is 
        #   made into a group
        g = get_the_actual_instance_from_zope(group)
        assert g
        gi = GSGroupInfo(g)
        assert gi.groupObj
        privacyChanger = IGSChangePrivacy(gi)
        if groupPrivacy == 'public':
            privacyChanger.set_group_public()
        elif groupPrivacy == 'private':
            privacyChanger.set_group_private()
        else:
            privacyChanger.set_group_secret()

