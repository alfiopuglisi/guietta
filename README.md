# guietta

A tool for making simple Python GUIs

Guietta is a tool that makes simple GUIs *simple*::


    from guietta import _, Gui, Quit
    
    gui = Gui(
        
      [  'Enter numbers:', '__a__'  , '+' , '__b__',  ['Calculate'] ],
      [  'Result:  -->'  , 'result' ,  _  ,    _   ,       _        ],
      [  _               ,    _     ,  _  ,    _   ,      Quit      ]
    )

    gui.run()


And here it is:

![Example GUI](http://guietta.com/_images/example.png)


