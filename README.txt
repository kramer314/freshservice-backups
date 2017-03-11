Copyright (c) 2017 Alex Kramer, Cat Tech <1336gm2@follett.com>
See the LICENSE.txt file at the top-level of this distribution.

Description
===========
Basic FreshService backup script that will save data on all tickets.

Dependencies
============
* Python 3.x (most recently tested with Python 3.5)
* Requests Python library (most recently tested with version 2.12)

Setup
=====
Create your own JSON configuration file. See ``./config_default.json`` for an
example. This should be a dictionary with the following fields:

* ``domain``: FreshService helpdesk URL
* ``api_key``: FreshService API key
* ``backup_path``: path to where backups should be stored
* ``backup_format``: Python datetime format string for formatting backup file
  names. See https://docs.python.org/3/library/datetime.html for documentation.
  The backup filenames are given by the output of:

    datetime.utcnow().strftime(backup_format)

* ``json_indent``: Optional, Indentation level for JSON backups

Usage
=====
You can run the backup script with:

  python3 ./backup.py /path/to/config_file.json

This will create two files in the specified ``backup_path``:

* ``[formatted datetime].json``: JSON dump of FreshService ticket information
* ``[formated datetime].log``: Backup log

where ``[formatted datetime]`` is a formatted UTC time at which the backup
script ran, where the formatting is controlled by the parameter
``backup_format``. The JSON dump is formatted with the following parameters:

* ``sort_keys=True``
* ``indent=[json_indent]``

Schedule a ``cron`` job to automate backups. For example, you can create a
script in ``/etc/cron.daily`` to run the backup script once per day, every day.
