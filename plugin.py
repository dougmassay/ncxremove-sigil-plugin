# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

import os
import sys
import re
from contextlib import contextmanager
from datetime import datetime, timedelta


from epub_utils import epub_zip_up_book_contents
from gui_utilities import fileChooser, update_msgbox
from updatecheck import UpdateChecker

_DEBUG_ = False


@contextmanager
def make_temp_directory():
    import tempfile
    import shutil
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def cleanup_file_name(name):
    # borrowed from calibre from calibre/src/calibre/__init__.py
    # added in removal of non-printing chars
    # and removal of . at start
    import string
    _filename_sanitize = re.compile(r'[\xae\0\\|\?\*<":>\+/]')
    substitute='_'
    one = ''.join(char for char in name if char in string.printable)
    one = _filename_sanitize.sub(substitute, one)
    one = re.sub(r'\s', '_', one).strip()
    one = re.sub(r'^\.+$', '_', one)
    one = one.replace('..', substitute)
    # Windows doesn't like path components that end with a period
    if one.endswith('.'):
        one = one[:-1]+substitute
    # Mac and Unix don't like file names that begin with a full stop
    if len(one) > 0 and one[0:1] == '.':
        one = substitute+one[1:]
    return one

def getTitle(meta):
    _title_pattern = re.compile(r'<dc:title[^<]*>([^<]*)</dc:title>')
    _title = 'filename'

    m = _title_pattern.search(meta)
    if m:
        _title = m.group(1).strip()
    return _title

def run(bk):
    if not bk.epub_version().startswith('3'):
        print('Error: NCXRemove requires a valid EPUB 3.0 ebook as input')
        return -1

    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        GUI = 'tkinter'
    else:
        GUI = 'pyqt'

    ncxid = bk.gettocid()
    if ncxid is None:
        print('Error: EPUB 3.0 ebook has no NCX')
        return -1
    ncxhref = bk.id_to_href(ncxid)

    prefs = bk.getPrefs()

    # set default preference values
    if 'use_file_path' not in prefs:
        prefs['use_file_path'] = os.path.expanduser('~')

    if 'check_for_updates' not in prefs:
        prefs['check_for_updates'] = True
    if 'last_time_checked' not in prefs:
        prefs['last_time_checked'] = str(datetime.now() - timedelta(hours=12))
    if 'last_online_version' not in prefs:
        prefs['last_online_version'] = '0.1.0'

    if prefs['check_for_updates']:
        chk = UpdateChecker(prefs['last_time_checked'], prefs['last_online_version'], bk._w)
        update_available, online_version, time = chk.update_info()
        # update preferences with latest date/time/version
        prefs['last_time_checked'] = time
        if online_version is not None:
            prefs['last_online_version'] = online_version
        if update_available:
            title = 'Plugin Update Available'
            msg = 'Version {} of the {} plugin is now available.'.format(online_version, bk._w.plugin_name)
            update_msgbox(title, msg, GUI)

    if _DEBUG_:
        print('Python sys.path', sys.path)

    doctitle = getTitle(bk.getmetadataxml())
    fname = cleanup_file_name(doctitle) + '_no_ncx.epub'

    outpath = fileChooser(fname, prefs['use_file_path'], GUI)
    if not outpath:
        print("NCXRemove plugin cancelled by user")
        return 0

    with make_temp_directory() as temp_dir:
        bk.copy_book_contents_to(temp_dir)
        opfdata = bk.readotherfile("OEBPS/content.opf").splitlines()
        opfout = os.path.join(temp_dir, 'OEBPS', 'content.opf')
        ncxfile = os.path.join(temp_dir, 'OEBPS', ncxhref)

        open(os.path.join(temp_dir, 'mimetype'),'wb').write('application/epub+zip'.encode('utf-8'))

        newopf = ''
        ncxitem = 'id="{}"'.format(ncxid)
        spineattr = ' toc="{}"'.format(ncxid)

        for line in opfdata:
            skip = False
            # Remove ncx item from the manifest of the OPF
            if line.lstrip().startswith('<item ') and line.find(ncxitem) is not -1:
                skip = True
            # Remove the ncx attribute from the spine tag of the OPF
            if line.lstrip().startswith('<spine') and line.find(spineattr) is not -1:
                line = line.replace(spineattr, '')
            if not skip:
                newopf += line + '\n'
                if _DEBUG_:
                    print(line)
        # Write new OPF to temp directory
        open(opfout,'wb').write(newopf.encode('utf-8'))

        # Delete the the toc.ncx file from the temp directory
        os.remove(ncxfile)

        # Build the new epub from the tmp structure and save to specified location
        epub_zip_up_book_contents(temp_dir, outpath)

    # Save last directory accessed to JSON prefs
    prefs['use_file_path'] = os.path.dirname(outpath)

    # Save prefs to json
    bk.savePrefs(prefs)
    # print ('Path to epub or src {0}'.format(epub))

    return 0

def main():
    print('I reached main when I should not have\n')
    return -1


if __name__ == "__main__":
    sys.exit(main())
