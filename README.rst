==================
``gs.group.start``
==================
~~~~~~~~~~~~~
Start a group
~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-10-24
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

Introduction
=============

This product defines the forms_ for starting a GroupServer_
group, and the underlying `group creation`_ code.

Forms
=====

There are two forms used with starting a group: the main `Start a
Group`_ form, and the `Check Identifier`_ form, which is used by
the Start a Group form.

Start a Group
-------------

The *Start a Group* form (``startgroup.html`` in the site
context) takes three fields: a name, a group identifier, and a
privacy setting. The associated JavaScript creates a default ID
from the name. It also uses the `Check Identifier`_ form to
ensure that the identifier is unique. If it is then the *Group
started* notification_ is sent to all site administrators after
`group creation`_.

Notification
~~~~~~~~~~~~

The notification ``gs-group-started.html`` (which renders in the
group context, along with its ``.txt`` equivalent) is used to
inform all the site administrators that the group has been
started. It is similar to the *Group welcome* notification
[#join]_, but with less general detail as leaving and viewing
profiles is less important when administrators start a group.
Because the notification is sent to all the administrators,
including the one that created the group, the notification is
written in *agentless* passive voice.

Check Identifier
----------------

The JavaScript resource ``/gs-group-start-20130712.js`` (and the
minified ``-min-*.js`` equivalent) uses the *Check identifier*
form to see if a group exists. The form takes an identifier as
input, and returns ``1`` if a group with that identifier exists,
or ``0`` otherwise [#ID]_.

Group Creation
==============

The ``gs.group.start.MoiraeForGroup`` class creates and deletes
group. The constructor takes a site-info instance, while the main
``create`` method has the following interface::

  create(groupName, groupId, groupPrivacy, mailHost, adminInfo)

``groupName``:
  The title of the group.

``groupId``:
  The unique identifier for the group.

``privacy``:
  The privacy for the group. It is a string of ``'public'`` for a
  public group, or ``'private'`` for a private group. Any other
  string will be interpreted as a request for a secret group.

``mailhost``:
  The mail-host (right-hand-side) porting of the email address
  for the group.

``adminInfo``:
  The user-info instance for person will be made the
  administrator for the group.

The ``create`` method returns the group-info instance for the
newly created group.

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.start/
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

.. [#join] See <https://github.com/groupserver/gs.group.member.join>.

.. [#ID] The need to check the group identifier to ensure it is
         unique is because the all the mailing instances exist in
         the same ``ListManager`` folder. In addition the
         identifier for each list must mach the identifier for
         the group. See
         `Bug 117. <https://redmine.iopen.net/issues/117>`_

..  LocalWords:  Organization html txt
