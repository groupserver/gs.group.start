"use strict";jQuery.noConflict();function StartAGroup(d,e,c){var j=null,h=null,l="/existing_id_check",b=false,k={"public":"The group will be <strong>public:</strong> <ul><li>The <strong>group and posts</strong> will be visible to anyone, including search engines.</li><li>Anyone can <strong>join</strong> the group.</li></ul>","private":"The group will be <strong>private:</strong> <ul><li>The <strong>group</strong> will be visible to anyone.</li><li>Only logged in <em>members</em> can view the <strong>posts.</strong></li><li>People must either <em>request membership</em> or be <em>invited</em> to <strong>join</strong> the group.</li></ul>",secret:"The group will be <strong>secret:</strong> <ul><li>The <strong>group</strong> will only be visible to logged in <em>members.</em></li><li>Only logged in <em>members</em> can view the <strong>posts.</strong></li><li>You must <strong>invite</strong> each person to join the group.</li></ul>"},n=null;
j=jQuery(d);h=jQuery(e);function q(t){if(!b){window.setTimeout(s,100)}}function s(){var t=null;
t=i(j.val());h.val(t).trigger("keyup",true);p()}function i(t){var w=null,v=/[ ]/g,u=/[^\w-_]/g;
w=t;w=w.replace(v,"-");w=w.replace(u,"");w=w.toLowerCase();return w}function p(){var u=null,t=null;
u=j.val();if(u==""){u="&#8230;"}t=jQuery(".preview .grpFn");t.html(u)}function f(u,t){if(t==undefined){b=true
}window.setTimeout(m,100)}function m(){var u=null,t=null;t=h.val();u=t;if(u==""){u="&#8230;"
}jQuery(".preview .groupId").html(u);g()}function g(){var t=null;t=h.val();if(n!=null){clearTimeout(n);
n=null}if(t!=""){n=setTimeout(r,250)}}function r(){var u=null,t=null;u=h.val();t={type:"POST",url:l,cache:false,data:{id:u},success:o};
jQuery.ajax(t)}function o(u,w){var t=null,v=null;t=u=="1";if(t){v=h.val();jQuery("#group-id-error code").text(v);
jQuery("#group-id-error").show()}else{jQuery("#group-id-error").hide()}}function a(w){var u=null,v=null,t=null;
v=jQuery("input:radio[name=form\\.grpPrivacy]:checked");u=v.val();jQuery("#visiblity-preview").html(k[u]);
t=jQuery("#gs-group-start-preview-secret");if((u=="secret")&&(t.is(":hidden"))){t.show()
}else{if((u!="secret")&&(t.is(":visible"))){t.hide()}}}return{init:function(){var u=null,t=null;
u={onpaste:q,paste:q,keyup:q};j.bind(u).trigger("paste");t={onpaste:f,paste:f,keyup:f};
h.bind(t).trigger("paste",true);jQuery(c).change(a).change()}}}jQuery(window).load(function(){var a=null;
a=StartAGroup("#form\\.grpName","#form\\.grpId","input:radio[name=form\\.grpPrivacy]");
a.init()});