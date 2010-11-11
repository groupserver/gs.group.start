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
                'to join the group.',
    }

    // Private methods
    // Group name
    grpNameChanged = function(event) {
        updateGrpNamePreview();

        if (!grpIdUserMod) {
            // HACK: Delay updating the name by 500ms so the group-ID 
            // text entry has a chance to update
            window.setTimeout(grpIdAutoUpdate, 500);
        } 
    };
    
    grpIdAutoUpdate = function() {
        // If the user has not modified the ID then update that
        // based on the name.
        newId = grpIdFromName(jQuery(grpName).val());
        jQuery(grpId).val(newId);
        jQuery(grpId).trigger('keyup', true);
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
        
        var newId = null;
        var grpIdV = jQuery(grpId).val();

        if (fakeIfSet == undefined) {
            grpIdUserMod = true;
        }
        newId = grpIdV;
        if (newId == '') {
          newId = '&#8230;';
        }
        jQuery('.preview .groupId').html(newId);
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
    }
    checkGroupId = function(event) {
        var id = null;
        id = jQuery('#form\\.grpId').val()
        var d = {
          type: "POST",
          url: existingIdCheckURL,
          cache: false,
          data: {'id': id},
          success: checkGroupIdReturn
        };
        if (id != '') {
            jQuery.ajax(d);
        }
    }

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
            e = {
                onpaste: grpNameChanged, // IE name for the paste event
                paste:   grpNameChanged, // Gecko name for the paste event
                keyup:   grpNameChanged, // Standard key-up event
            };
            jQuery(grpName).bind(e);
            jQuery(grpName).trigger('paste');
            jQuery(grpId).keyup(checkGroupId).keyup();
            jQuery(grpId).keyup(grpIdChanged).trigger('keyup', true);
            jQuery(privacyButtons).change(grpPrivacyChanged).change();
        },
    }
}(); // OGNStartASiteGrp

jQuery(document).ready( function () {
    StartAGroup.init(); 
});

