NCXRemove (A Sigil Plugin)
============

Export an EPUB3 with NCX removed

**NOTE: this plugin periodically checks for updated versions by connecting to this Github repository (see the configurable preferences section below to disable this behavior)**

Links
=====

* Sigil website is at <http://sigil-ebook.com>
* Sigil support forums are at <http://www.mobileread.com/forums/forumdisplay.php?f=203>
* NCXRemove plugin MobileRead support thread: <https://www.mobileread.com/forums/showthread.php?t=284445>

Building
========

First, clone the repo:

    $ git clone https://github.com/dougmassay/ncxremove-sigil-plugin.git

To create the plugin zip file, run the buildplugin.py script (root of the repository tree) with Python (2 or 3)

    $python ./buildplugin (or just ./buildplugin if Python is on your PATH)

This will create the NCXRemove_vX.X.X.zip file that can then be installed into Sigil's plugin manager.

Using NCXRemove
=================
If you're using Sigil v0.9.0 or later, all dependencies should already be met.

Linux users will have to make sure that the PyQt5 python module (or the Tk python module)  is present if it's not already. On Debian-based flavors this can be done with "sudo apt-get install python3-pyqt5" (or "sudo apt-get install python3-tk") for Python 3.4.

* **Note:** Do not rename any Sigil plugin zip files before attempting to install them

Configurable preferences (available after first run in the plugin's corresponding json prefs file) are:

* **check_for_updates** : a true or false (boolean) value (defaults to true). Change this to "false" if you don't want this plugin to periodically check for updates.

Get more help in the NCXRemove plugin [MobileRead support thread:](http://www.mobileread.com/forums/)


Contributing / Modifying
============
From here on out, a proficiency with developing / creating Sigil plugins is assumed.
If you need a crash-course, an introduction to creating Sigil plugins is available at
http://www.mobileread.com/forums/showthread.php?t=251452.

The core plugin files (this is where most contributors will spend their time) are:

    > plugin.py
    > gui_utilities.py
    > plugin.xml
    > updatecheck.py


Files used for building/maintaining the plugin: 

    > buildplugin  -- this is used to build the plugin.
    > setup.cfg -- used for flake8 style checking. Use it to see if your code complies.
    > checkversion.xml -- used by automatic update checking.

Feel free to fork the repository and submit pull requests (or just use it privately to experiment).



License Information
=======

### NCXRemove

Available under the terms of the [MIT license](http://opensource.org/licenses/mit-license.php)


Copyright (c) 2016 Doug Massay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
