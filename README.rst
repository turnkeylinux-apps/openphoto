OpenPhoto - All your photos in one spot
=======================================

`OpenPhoto`_ helps put all your photos in one spot. Wherever you decide.
Amazon S3, DropBox or in your garage. Liberate your photos and take back
control because our photos are the most valuable digital files we have
and we don't want them scattered across numerous sites on the web.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- OpenPhoto configurations:
   
   - Installed from upstream source code to /var/www/openphoto

- SSL support out of the box.
- `PHPMyAdmin`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, phpMyAdmin: username **root**
-  OpenPhoto: default username is email set at first boot


.. _OpenPhoto: http://theopenphotoproject.org/
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _PHPMyAdmin: http://www.phpmyadmin.net
