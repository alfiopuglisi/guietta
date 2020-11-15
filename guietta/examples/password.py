# -*- coding: utf-8 -*-

from guietta import Gui, QMessageBox, PW

gui = Gui(
  [  'Enter password:', PW('password') , ['Check'] ]
)

# Accept both the Enter key and a click on "Check"

with gui.Check, gui.password:
    if gui.is_running:
        if gui.password == '123456':
            QMessageBox.information(None, "Correct!", 'Correct!')
        else:
            QMessageBox.information(None, "Wrong!", 'Wrong!')

gui.run()

