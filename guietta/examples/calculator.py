from guietta import _, Gui, Quit
import guietta

gui = Gui(
	[ "Enter numbers:",  "__a__", "+", "__b__", ["Calculate"] ],
	[    "Result: -->", "result",   _,       _,             _ ],
	[                _,        _,   _,       _,          Quit ]
)

with gui.Calculate:
	if not gui.is_running:
		gui.result = ""
	else:
		gui.result = float(gui.a) + float(gui.b)

gui.run()
