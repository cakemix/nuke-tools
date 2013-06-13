#!/usr/bin/env python

# example of iterating through selected nodes
for n in nuke.selectedNodes():
    print n.name()
    
# same example but only using a specific node class
for n in nuke.selectedNodes("Camera2"):
    print n.name()
    
# running tcl commands in python
nuke.tcl("value label")