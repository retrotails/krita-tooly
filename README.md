# krita-tooly
![screenshot](/screenshot.png?raw=true)  
this is a simple toolbox replacement I wrote for personal use.  
the default toolbox can't be customized, and adding custom buttons to the top toolbar shows text instead of icons, so I wrote this plugin.  
if you want different tools, you'll have to find the krita action that activates them, and the internal name for the icon (see comment in script) and make your changes to the "tools" dictionary.  
## limitations/TODO:
* hard-coded tools
* minimum size for tooly window is larger than default toolbox, quite large on my tiny screen
* tooly can't be placed in krita's top toolbar. that would be reeeeeally nice. or if krita just fixed toolbar entries not having their icons.
## installing:
copy "tooly" folder and "tooly.desktop" into pykrita folder
