# -*- coding: utf-8 -*-

from guietta import QFileDialog

filename = QFileDialog.getOpenFileName(None, "Open File",
                                             "/home",
                                             "Images (*.png *.xpm *.jpg *.jpeg)")

print(filename)
