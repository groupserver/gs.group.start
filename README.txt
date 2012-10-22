Introduction
=============

This product defines the forms_ for starting a GroupServer_ group, and the
underlying `group creation`_ code.

Forms
=====

There are two forms used with starting a group: the main `Start a Group`_
form, and the `Check Identifier`_ form, which is used by the Start a Group
form.

Start a Group
-------------

The *Start a Group* form takes three fields: a name, a group identifier,
and a privacy setting. The associated JavaScript creates a default ID from
the name. It also uses the `Check Identifier`_ form to ensure that the
identifier is unique.

Check Identifier
----------------

The *Check Identifier* form takes an identifier as input. It returns ``1``
if a group with that identifier exists, or ``0`` otherwise [#ID]_.


Group Creation
==============

The ``gs.group.start.MoiraeForGroup`` class creates and deletes group. The
constructor takes a site-info instance, while the main ``create`` method
has the following interface::

  create(groupName, groupId, groupPrivacy, mailHost, adminInfo)

``groupName``:
  The title of the group.

``groupId``:
  The unique identifier for the group.

``privacy``:
  The privacy for the group. It is a string of ``'public'`` for a public
  group, or ``'private'`` for a private group. Any other string will be
  interpreted as a request for a secret group.

``mailhost``:
  The mail-host (right-hand-side) porting of the email address for the
  group.

``adminInfo``:
  The user-info instance for person will be made the administrator for the
  group.

The ``create`` method returns the group-info instance for the newly created
group.

.. [#ID] The need to check the group identifier to ensure it is unique is
         because the all the mailing instances exist in the same
         ``ListManager`` folder. In addition the identifier for each list
         must mach the identifier for the group. See
         `Bug 117. <https://redmine.iopen.net/issues/117>`_

.. _GroupServer: http://groupserver.org
