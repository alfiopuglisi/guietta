
from guietta import Gui, _, HSeparator, C, G, R, ___, III, QMessageBox


main = Gui(['<center>Dynamic layout demonstration</center'],
           [HSeparator],
           [   'label1'    , 'label2', ['Click here'] ],
           [G('Inner GUI') ,   ___   ,        _       ],
           [     III       ,   III   ,    'label4'    ],
           [   'label5'    , 'label6',        _       ])

subgui = Gui( [C('checkbox'), '__editbox__'],
              [R('radio')   ,  ['And here!']  ])

subgui.Andhere = lambda x: QMessageBox.information(None, "Clicked",
                           "The editbox contains "+subgui.editbox)

with main.Clickhere:
    if main.is_running:
        main.InnerGUI = subgui


main.run()
      
