
Troubleshooting
===============

First stop: if you use conda, please read our page on
`QT incompatibilities with conda <qt_conda.html>`_.


If you don't use conda, but you see error messages similar to these
every time you import the guietta module::

   qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
   This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

   Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

   Aborted (core dumped)


This means that some QT plugins are missing, and/or not installed correctly.
Ubuntu 16.04 for example is missing the *libxcb-xinerama0* in its default
installation.

Turn on the plugin debug like this::

   export QT_DEBUG_PLUGINS=1
  
Run again the Guietta program, and you will get a lot more output with
hopefully an error message, which in my case was::


    Cannot load library /usr/local/lib/python3.5/dist-packages/PySide2/Qt/plugins/platforms/libqxcb.so: (libxcb-xinerama.so.0: cannot open shared object file: No such file or directory)

Therefore I installed libxcb-xinerama0::

   sudo apt install libxcb-xinerama0

This problem and successful resoluton was also reported for Ubuntu 20.04