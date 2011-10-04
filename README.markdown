Show Tracker
--------------

###Use

1. Run `python ./showtracker.py`
1. Help is in the help tab and should show the first load
1. Submit patches and issues :D

###Requirements

- pyQt 
- Qt-4.7+ 
- python 2.x

###Modifying the resources

When adding, removing, editing resources you must use the qt resource editor.
You must also import resources.resources in to the *_ui.py file you are working on.
The final step to modifying a resource is running `pyrcc4 ./resources.qrc -o resources.py` in the resources folder.

###Generating documentation
1. Run `epydoc --config=epydoc.config` in the root folder
1. Documentation will be located in the `./html/` folder

###Moving from an older version (or where have my shows gone?)
I've updated the code to remove references to version 3 so the application can remain just as Show Tracker for the future. 
This means the ShowTracker3 settings file which is usually located in `~/.config/ShowTracker3/` on linux is now going to be in 
`~/.config/ShowTracker/`. If you have the folder just rename it an the file located inside named `ShowTracker3.conf` to `ShowTracker.conf`.