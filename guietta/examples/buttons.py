# -*- coding: utf-8 -*-

import os.path
from guietta import B, L, _, Gui

gui = Gui(
    
  [ ['left']                   ],     # Simple button
  [ (['left'], 'bb')           ],     # Simple button, renamed
  [ B('left')                  ],     # Previous two with explicit B
  [ (B('left'), 'bb')          ],  
  [ ['left.png']               ],     # Image button
  [ ['left.png', 'aa']         ],     # Image button + text
  [ (['left.png'], 'bb')       ],     # Image button, renamed
  [ (['left.png', 'aa'], 'bb') ],     # Image button + text, renamed
  [ B('left.png')               ],    # Previous for with explicit B
  [ B('left.png', 'aa')         ],
  [ (B('left.png'), 'bb')       ],
  [ (B('left.png', 'aa'), 'bb') ],

  [ ['leftt.png']               ],     # Previous 8 with wrong filename
  [ ['leftt.png', 'aa']         ],
  [ (['leftt.png'], 'bb')       ],
  [ (['leftt.png', 'aa'], 'bb') ],
  [ B('leftt.png')               ],
  [ B('leftt.png', 'aa')         ],
  [ (B('leftt.png'), 'bb')       ],
  [ (B('leftt.png', 'aa'), 'bb') ],

  images_dir = os.path.dirname(__file__))

while True:
    name, event = gui.get()

    print(name, event)

    if name == None:
        break


