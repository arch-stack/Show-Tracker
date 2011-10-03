Show Tracker 3
--------------

###Use

1. Run `python ./showtracker3.py`
2. Help is in the help tab and should show the first load
3. Submit patches and issues :D

###Requirements

- pyQt 
- Qt-4.7+ 
- python 2.x

###Modifying the resources

When adding, removing, editing resources you must use the qt resource editor.
You must also import resources.resources in to the *_ui.py file you are working on.
The final step to modifying a resource is running `pyrcc4 ./resources.qrc -o resources.py` in the resources folder.