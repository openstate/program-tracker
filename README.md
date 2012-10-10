program-tracker
===============

Tracks Election Programs


core is the base, which handles the programs itself
topic handles the topics

made with Django 1.4

Dependencies:

- south: http://south.aeracode.org/
- jquery + plugins (included): http://jquery.com/
- mkvirtualenv: http://stackoverflow.com/questions/9520887/mkvirtualenv-no-site-packages-command-getting-command-not-found-error

installation
============

  1. `git clone git@github.com:hmvp/program-tracker.git`
  2. `mkvirtualenv programtracker`
  3. `workon programtracker`
  4. `pip install -r requirements.txt`
  5. `cp programtracker/settings\_local.py.example programtracker/settings\_local.py`
  6. edit your local settings
  7. `./manage.py syncdb`
  8. `./manage.py migrate`
  9. `./manage.py runserver`
  10. `./manage.py loaddata core/bootstrap.json`

import
======

Programs 2012:

1.  Find the id of the program you want to import
2.  Find the filename you want to import. This works for the files in /programmas/ where the part without the extension is the part you need to remember.
3.  Go to <url>/import/add/<filename>/to/<id>/ (e.g. /import/add/cda/to/3/)
4.  Repeat for all programs.

Lipschits Data:

1.  Extract the zip into the main folder, now you have a folder named 'LipschitsBooksinXML'
2.  Note the year you want to import, it is in the filename of the xml files in the LipschitsBooksinXML folder
3.  Go to /import/add/<year>/

license
=======
	This file is part of Program-tracker.

    Program-tracker is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Program-tracker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Program-tracker.  If not, see <http://www.gnu.org/licenses/>.