# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import unicode_literals, division, absolute_import, print_function

import os
import sys


def fileChooser(fname, initial_dir, gui='tkinter', title='Save EPUB as', ext='.epub'):
    if gui == 'tkinter':
        from tkinter import Tk
        from tkinter.filedialog import asksaveasfilename

        localRoot = Tk()
        localRoot.withdraw()

        if sys.platform.startswith('darwin'):
            # localRoot is is an empty topmost root window that is hidden by withdrawing it
            # but localRoot needs to be centred, and lifted and focus_force used
            # so that its child dialog will inherit focus upon launch
            localRoot.overrideredirect(True)
            # center on screen but make size 0 to hide the empty localRoot
            w = localRoot.winfo_screenwidth()
            h = localRoot.winfo_screenheight()
            x = int(w/2)
            y = int(h/2)
            localRoot.geometry('%dx%d+%d+%d' % (0, 0, x, y))
            localRoot.deiconify()
            localRoot.lift()
            localRoot.focus_force()

        file_opt = {}
        file_opt['parent'] = localRoot
        file_opt['title']= title
        file_opt['defaultextension'] = ext
        file_opt['initialfile'] = fname
        file_opt['initialdir'] = initial_dir
        file_opt['filetypes'] = [('EPUB', ('.epub'))]

        fpath = asksaveasfilename(**file_opt)
        localRoot.quit()
        return fpath
    elif gui == 'pyqt':
        from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

        # app required but unused
        app = QApplication(sys.argv)
        w = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        initial_name = os.path.join(initial_dir, fname)
        fpath, _ = QFileDialog.getSaveFileName(w,'Save EPUB as:', initial_name,
                                                  'EPUB (*.epub )', options=options)
        return fpath

def update_msgbox(title, msg, gui='tkinter'):
    if gui == 'tkinter':
        from tkinter import Tk
        import tkinter.messagebox as tkinter_msgbox
        localRoot = Tk()
        localRoot.withdraw()
        localRoot.option_add('*font', 'Helvetica -12')
        localRoot.quit()
        return tkinter_msgbox.showinfo(title, msg)
    elif gui == 'pyqt':
        from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

        app = QApplication(sys.argv)
        w = QWidget()
        return QMessageBox.information(w, title, msg)
