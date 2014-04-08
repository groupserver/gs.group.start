"use strict";
// JavaScript for handling all the interlocks associated with Start a Group.
//
// Copyright © 2014 OnlineGroups.net and Contributors.
// All Rights Reserved.
//
// This software is subject to the provisions of the Zope Public License,
// Version 2.1 (ZPL). http://groupserver.org/downloads/license/
//
// THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
// WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
// FITNESS FOR A PARTICULAR PURPOSE.
jQuery.noConflict();

function StartAGroup(grpName, grpId, privacyButtons) {
    // Private variables
    var groupName=null, groupId=null,
        existingIdCheckURL='/existing_id_check',
        grpIdUserMod=false,
        privacyExpln={
            'public': 'The group will be <strong>public:</strong> <ul>'+
                      '<li>The <strong>group and posts</strong> will be '+
                      'visible to anyone, including search engines.</li>'+
                      '<li>Anyone can <strong>join</strong> the '+
                      'group.</li></ul>',
            'private': 'The group will be <strong>private:</strong> <ul>'+
                       '<li>The <strong>group</strong> will be visible to '+
                       'anyone.</li>' +
                       '<li>Only logged in <em>members</em> can view the '+
                       '<strong>posts.</strong></li>'+
                       '<li>People must either <em>request membership</em> '+
                       'or be <em>invited</em> to <strong>join</strong> the '+
                       'group.</li></ul>',
            'secret': 'The group will be <strong>secret:</strong> <ul>'+
                       '<li>The <strong>group</strong> will only be visible '+
                       'to logged in <em>members.</em></li>' +
                       '<li>Only logged in <em>members</em> can '+
                       'view the <strong>posts.</strong></li>'+
                       '<li>You must <strong>invite</strong> '+
                       'each person to join the group.</li></ul>'
        }, 
        idChkTimeout=null;

    groupName = jQuery(grpName);
    groupId = jQuery(grpId);

    // Private methods
    // Group name
    function grpNameChanged(event) {
        if (!grpIdUserMod) {
            // HACK: Delay updating the name by 100ms so the group-name 
            // text entry has a chance to update
            window.setTimeout(grpNameChangeTimeout, 100);
        } 
    }
    
    function grpNameChangeTimeout() {
        // If the user has not modified the ID then update that
        // based on the name.
        var newId=null;
        newId = grpIdFromName(groupName.val());
        groupId.val(newId).trigger('keyup', true);
        updateGrpNamePreview();
    }
    
    function grpIdFromName(origGrpName) {
        // Get an group ID from a group name
        var newGrpId=null, re1=/[ ]/g, re2=/[^\w-_]/g;
        newGrpId = origGrpName;
        newGrpId = newGrpId.replace(re1, '-');
        newGrpId = newGrpId.replace(re2, '');
        newGrpId = newGrpId.toLowerCase();
        return newGrpId;
    }

    function updateGrpNamePreview() {
        var newName=null, grpNames=null;
        
        newName = groupName.val();
        if (newName == '') {
          newName = '&#8230;';
        }
        grpNames = jQuery('.preview .grpFn');
        grpNames.html(newName);
    }

    // Group Id
    function grpIdChanged(event, fakeIfSet) {
        // Callback for someone changing the group ID
        //
        // --=mpj17=-- For a while now I have been working on a
        // way to distinguish between *real* events, triggered by
        // the user, and *fake* events that the code
        // generates. This is the current state of the art. The
        // fakeIfSet argument will not be set by a real event
        // handler. Therefore, all it takes to ensure that I can
        // tell the difference between an actual event and a fake
        // event is to ensure I pass *something* as the fakeIfSet
        // argument.
        
        if (fakeIfSet == undefined) {
            grpIdUserMod = true;
        }
        window.setTimeout(grpIdChangeTimeout, 100);
    }

    function grpIdChangeTimeout() {
        var newId=null, grpIdV=null;
        grpIdV = groupId.val();
        newId = grpIdV;
        if (newId == '') {
          newId = '&#8230;';
        }
        jQuery('.preview .groupId').html(newId);
        checkGroupId()
    }

    function checkGroupId() {
        var id=null;
        id = groupId.val();
        
        if (idChkTimeout != null) {
            clearTimeout(idChkTimeout);
            idChkTimeout = null;
        }
        if (id != '') {
            idChkTimeout = setTimeout(fireGrpIdAjaxCheck, 250);
        }
    }

    function fireGrpIdAjaxCheck() {
        var id=null, d=null;
        
        id = groupId.val();
        d = {
          type: "POST",
          url: existingIdCheckURL,
          cache: false,
          data: {'id': id},
          success: checkGroupIdReturn
        };
        jQuery.ajax(d);
    }

    function checkGroupIdReturn(data, textStatus) {
        var exists=null, id=null;
        exists = data == '1';
        if (exists) {
          id = groupId.val();
          jQuery('#group-id-error code').text(id);
          jQuery('#group-id-error').show();
        } else {
          jQuery('#group-id-error').hide();
        }
        // TODO: Disable the submit button. This requires
        //       interacting with the required-widgets.
    }

    // Privacy
    function grpPrivacyChanged(event) {
        var currentPrivacy=null, selected=null, secret=null;
        selected = jQuery('input:radio[name=form\\.grpPrivacy]:checked');
        currentPrivacy = selected.val();
        jQuery('#visiblity-preview').html(privacyExpln[currentPrivacy]);
        secret = jQuery('#gs-group-start-preview-secret')
        if ((currentPrivacy == 'secret') && (secret.is(':hidden'))) {
            secret.show();
        }
        else if ((currentPrivacy != 'secret') && (secret.is(':visible'))) {
            secret.hide();
        }
    }
    
    // Public methods and properties
    return {
        init: function () {
            var e=null, f=null;
            e = {
                onpaste: grpNameChanged, // IE name for the paste event
                paste:   grpNameChanged, // Gecko name for the paste event
                keyup:   grpNameChanged  // Standard key-up event
            };
            groupName.bind(e).trigger('paste');
            f = {
                onpaste: grpIdChanged, // IE name for the paste event
                paste:   grpIdChanged, // Gecko name for the paste event
                keyup:   grpIdChanged  // Standard key-up event
            }
            groupId.bind(f).trigger('paste', true);
            jQuery(privacyButtons).change(grpPrivacyChanged).change();
        }
    }
} // OGNStartASiteGrp

jQuery(window).load( function () {
    var sag=null;
    sag = StartAGroup('#form\\.grpName', '#form\\.grpId', 
                      'input:radio[name=form\\.grpPrivacy]');
    sag.init();
});
