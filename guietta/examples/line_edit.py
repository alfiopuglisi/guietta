'''
Example with different line edit initializations
'''
from guietta import Gui, E, _, Quit, QMessageBox

gui = Gui(
 [ '__foo__'    , _ ],
 [ '__bar__:10' , _ ],
 [ E('tux')     , _ ],
 [ (E('a'), 'b'), _ ],
 [ ('__c__', 'd'),_ ],
 [  ['Show']    , Quit ])

with gui.Show:
    if gui.is_running:
        msg = 'Widget values:\n'
        for widget in 'foo bar tux b d'.split():
            msg += '%s = %s\n' % (widget, gui.proxy(widget).get())
        QMessageBox.information(None, None, msg)

gui.run()

