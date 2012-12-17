// JavaScript for handling all the interlocks associated with Start a Group.
var StartAGroup = function () {
    // Private variables
    var grpName = '#form\\.grpName';
    var grpId = '#form\\.grpId';
    var privacyButtons = 'input:radio[name=form\\.grpPrivacy]';
    var existingIdCheckURL =  '/existing_id_check';
    var grpIdUserMod = false;
    var privacyExpln = {
      'public': 'The group and posts will be <strong>visible</strong> '+
                ' to anyone, including search engines, and anyone can '+
                'join the group.',
      'private': 'The group will be  <strong>visible</strong> to '+
                'anyone, but only logged in members can view the' +
                ' posts. People must apply to join the group.',
      'secret': 'The group and posts will be <strong>visible</strong> '+
                'to logged in members only. People must be invited '   +
                'to join the group.'
    }
    var idChkTimeout = null;
    
    // Private methods
    // Group name
    grpNameChanged = function(event) {
        if (!grpIdUserMod) {
            // HACK: Delay updating the name by 100ms so the group-name 
            // text entry has a chance to update
            window.setTimeout(grpNameChangeTimeout, 100);
        } 
    };
    
    grpNameChangeTimeout = function() {
        // If the user has not modified the ID then update that
        // based on the name.
        newId = grpIdFromName(jQuery(grpName).val());
        jQuery(grpId).val(newId);
        jQuery(grpId).trigger('keyup', true);
        updateGrpNamePreview();
    };
    grpIdFromName = function(origGrpName) {
        // Get an group ID from a group name
        var newGrpId = null;
        var re1 = /[ ]/g;
        var re2 = /[^\w-_]/g;
        newGrpId = origGrpName;
        newGrpId = newGrpId.replace(re1, '-');
        newGrpId = newGrpId.replace(re2, '');
        newGrpId = newGrpId.toLowerCase();
        return newGrpId;
    };
    updateGrpNamePreview = function() {
        var newName = null;
        var grpNames  = null;
        
        newName = jQuery(grpName).val();
        if (newName == '') {
          newName = '&#8230;';
        }
        grpNames = jQuery('.preview .grpFn');
        grpNames.html(newName);
    };

    // Group Id
    grpIdChanged = function(event, fakeIfSet) {
        // Callback for someone changing the group ID
        //
        // --=mpj17=-- For a while now I have been working on a way to
        // distinguish between *real* events, triggered by the user, and
        // *fake* events that the code generates. This is the current
        // state of the art. The fakeIfSet argument will not be set by
        // a real event handler. Therefore, all it takes to ensure that
        // I can tell the difference between an actual event and a fake
        // event is to ensure I pass *something* as the fakeIfSet 
        // argument.
        
        if (fakeIfSet == undefined) {
            grpIdUserMod = true;
        }
        window.setTimeout(grpIdChangeTimeout, 100);
    };
    grpIdChangeTimeout = function() {
        var newId = null;
        var grpIdV = jQuery(grpId).val();

        newId = grpIdV;
        if (newId == '') {
          newId = '&#8230;';
        }
        jQuery('.preview .groupId').html(newId);
        checkGroupId()
    };
    checkGroupId = function() {
        var id = null;
        id = jQuery('#form\\.grpId').val();
        
        if (idChkTimeout != null) {
            clearTimeout(idChkTimeout);
            idChkTimeout = null;
        }
        if (id != '') {
            idChkTimeout = setTimeout(fireGrpIdAjaxCheck, 250);
        }
    };
    fireGrpIdAjaxCheck = function() {
        var id = null;
        var d = null;
        
        id = jQuery('#form\\.grpId').val()
        d = {
          type: "POST",
          url: existingIdCheckURL,
          cache: false,
          data: {'id': id},
          success: checkGroupIdReturn
        };
        jQuery.ajax(d);
    };
    checkGroupIdReturn = function(data, textStatus) {
        var exists = null;
        var id = null;
        exists = data == '1'
        if (exists) {
          id = jQuery(grpId).val();
          jQuery('#group-id-error code').text(id);
          jQuery('#group-id-error').show();
        } else {
          jQuery('#group-id-error').hide();
        }
        // TODO: Disable the submit button. This requires interacting
        //       with the required-widgets.
    };

    // Privacy
    grpPrivacyChanged = function(event) {
        var currentPrivacy = null;
        var selected = null;
        selected = jQuery('input:radio[name=form\\.grpPrivacy]:checked');
        currentPrivacy = selected.val();
        jQuery('#visiblity-preview').html(privacyExpln[currentPrivacy]);
    }
    
    // Public methods and properties
    return {
        init: function () {
            var e = {
                onpaste: grpNameChanged, // IE name for the paste event
                paste:   grpNameChanged, // Gecko name for the paste event
                keyup:   grpNameChanged  // Standard key-up event
            };
            jQuery(grpName).bind(e).trigger('paste');
            var f = {
                onpaste: grpIdChanged, // IE name for the paste event
                paste:   grpIdChanged, // Gecko name for the paste event
                keyup:   grpIdChanged  // Standard key-up event
            }
            jQuery(grpId).bind(f).trigger('paste', true);
            jQuery(privacyButtons).change(grpPrivacyChanged).change();
        }
    }
}(); // OGNStartASiteGrp

jQuery(document).ready( function () {
    StartAGroup.init(); 
});

