# -*- coding: utf-8 -*-




from guietta import Gui


gui1 = Gui(['a', 'b', ['C'] ])
gui2 = Gui(['a', 'd', ['E'] ])


gui1.a = 'foo'
gui2.a = 'bar'

gui1.show()
gui2.show()
gui1._app.exec_()

