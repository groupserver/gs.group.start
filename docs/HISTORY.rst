Changelog
=========

2.3.4 (2015-09-21)
------------------

* Using ``Hello`` rather than ``Dear`` in the opening salutation
  of the notifications
* Using ``subject`` rather than ``Subject`` in ``mailto:`` URIs

2.3.3 (2015-03-18)
------------------

* Fixing broken internationalisation on the *Start a group* page,
  with thanks and apologies to Lady Donna Dutchess

2.3.2 (2015-03-12)
------------------

* [FR] Adding a partial French translation
* Adding Transifex_ support

.. _Transifex:
   https://www.transifex.com/projects/p/gs-group-start/

2.3.1 (2015-01-26)
------------------

* Cleaning up Unicode, and :pep:`8` issues

2.3.0 (2014-10-24)
------------------

* Adding internationalisation
* Using GitHub_ as the main code repository, and naming the
  reStructuredText files as such.

.. _GitHub: https://github.com/groupserver/gs.group.start/

2.2.6 (2014-06-13)
------------------

* Following ``gs.content.form`` to ``gs.content.form.base``

2.2.5 (2014-06-02)
------------------

* Closing `Bug 4105 <https://redmine.iopen.net/issues/4105>`_

2.2.4 (2014-05-12)
------------------

* Fixing a spelling mistake

2.2.3 (2014-04-8)
-----------------

* Switched the JavaScript to ``use strict;``
* Turing some ``assert`` statements into ``raise``

2.2.2 (2014-03-06)
------------------

* Switching to Unicode literals
* Ensuring the headers have the correct encoding.

2.2.1 (2013-10-30)
------------------

* New *Group started notification*
* Updates to the JavaScript

2.2.0 (2013-07-22)
------------------

* Changing the default privacy to *Private*, from *Public*.
* Updating the user-interface to warn about the usability issues
  inherit with secret groups.
* Updating following the refactor of the jQuery module

2.1.1 (2012-12-17)
------------------

* Fixing JavaScript and IE7
* Dropping the WYMEditor JS from the Start page (again)

2.1.0 (2012-10-24)
------------------

* Removing the ``admingroup`` folder
* Cleaning up the clode, thanks to Ninja-IDE
* Adding the Moiræ to the ``__init__`` for the product
* Fixing the permissions

2.0.1 (2012-06-22)
------------------

* Updating ``SQLAlchemy``

2.0.0 (2012-03-29)
------------------

* Dropping support for the WYMEditor, and following the
  refactoring of the jQuery modules
* Fixing the product dependencies, and cleaning up the imports

1.1.1 (2011-12-19)
------------------

* Adding a link to the *Administer Site* page 
* Switching to ``gs.group.type.discussion`` as the base group
  type, and purged ``Products.XWFChat`` from the codebase

1.1.0 (2011-05-29)
-------------------

* Adding start-group events
* Making the site administrator the group administrator, closing
  `Ticket 611 <https://redmine.iopen.net/issues/611>`_

1.0.3 (2011-03-23)
------------------

* Fixing the factory
* Refactoring of the internal code,

1.0.2 (2010-12-09)
------------------

* Moving the page-specific styles to the global stylesheet (CSS)
* Removing the jQuery links.
* Using the new form-message content-provider.

1.0.1 (2010-11-30)
------------------

* Dropping the ``email_settings`` folder
* Making the SQL quiet

1.0.0 (2010-11-15)
------------------

* Initial version

..  LocalWords:  Changelog Trasifex Transifex
