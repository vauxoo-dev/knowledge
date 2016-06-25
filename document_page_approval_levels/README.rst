
.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :alt: License: LGPL-3

Document Page Approval Levels
=============================

This module:
  - Add the model approver.document.page.item, to allow set approvers in
    document page and document history
  - Add field approver_item_ids in document page to allow set the users
    that need approve the histories created by the page. (If you update the
    users list the system renders the histories that are not approved. )
  - Add field approver_item_ids in document history, to allow approve the
    history to users that are assigned in the document page.
    Note: Only the user assigned to the item could approve it.
  - Added validation to only show the valida button in history when all
    items are approveds.
  - When a user is select in an item, this user is added as follower in
    the document page.
  - Change the template that is send when is created a new history for a
    document.
  - When a user approve an item, is added a notification in the page, with the
    next message: "The page has been approved by $USER "
  - Added two new levels in knowledge group, (Approver and Manager)
    The actually group User only can read, write and create pages.
    The user approver have access to Pages, Categories and Histories.
    The manager user have access to all menus in Knowledge.

.. contents::

Installation
============

To install this module, you need to:

- Not special pre-installation is required, just install as a regular Odoo
  module:

  - Download this module from `Vauxoo/knowledge
    <https://github.com/vauxoo/knowledge>`_
  - Add the repository folder into your odoo addons-path.
  - Go to ``Settings > Module list`` search for the current name and click in
    ``Install`` button.

Configuration
=============

To configure this module, you need to:

* There is not special configuration for this module.

Bug Tracker
===========

Bugs are tracked on
`GitHub Issues <https://github.com/Vauxoo/knowledge/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and
welcomed feedback
`here <https://github.com/Vauxoo/knowledge/issues/new?body=module:%20
document_page_approval_levels%0Aversion:%20
8.0.2.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_

Credits
=======

**Contributors**

* Sabrina Romero <sabrina@vauxoo.com> (Planner/Auditor)
* Luis Torres <luis_t@vauxoo.com> (Developer)

Maintainer
==========

.. image:: https://s3.amazonaws.com/s3.vauxoo.com/description_logo.png
   :alt: Vauxoo
   :target: https://www.vauxoo.com
   :width: 200

This module is maintained by the Vauxoo.

To contribute to this module, please visit https://www.vauxoo.com.

