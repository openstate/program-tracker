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