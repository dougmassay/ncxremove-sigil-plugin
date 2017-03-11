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
        file_opt = {}
        file_opt['parent'] = localRoot
        file_opt['title']= title
        file_opt['defaultextension'] = ext
        file_opt['initialfile'] = fname
        file_opt['initialdir'] = initial_dir
        file_opt['filetypes'] = [('EPUB', ('.epub'))]
        localRoot.quit()
        return asksaveasfilename(**file_opt)
    elif gui == 'pyqt':
        from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

        # app required but unused
        app = QApplication(sys.argv)
        w = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        initial_name = os.path.join(initial_dir, fname)
        fileName, _ = QFileDialog.getSaveFileName(w,'Save EPUB as:', initial_name,
                                                  'EPUB (*.epub )', options=options)
        return fileName

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
