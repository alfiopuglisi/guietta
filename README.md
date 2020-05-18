# guietta

A tool for making simple Python GUIs

Guietta is a tool that makes simple GUIs *simple*:


    from guietta import _, Gui, Quit
    
    gui = Gui(
        
      [  'Enter numbers:', '__a__'  , '+' , '__b__',  ['Calculate'] ],
      [  'Result:  -->'  , 'result' ,  _  ,    _   ,       _        ],
      [  _               ,    _     ,  _  ,    _   ,      Quit      ]
    )

    gui.run()


And here it is:

![Example GUI](http://guietta.com/_images/example.png)


# Installation

 **pip install guietta**
 

If you use conda, please read our page on
[QT incompatibilities with conda](https://guietta.readthedocs.io/en/latest/qt_conda.html).


# Documentation

https://guietta.readthedocs.io/en/latest/