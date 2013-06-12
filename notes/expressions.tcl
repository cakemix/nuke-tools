## On/Off in GUI mode
$gui
$gui ? 1 : 0
$gui ? 1 : 16 #scanline render

# Use python wrapped in tcl
[python nuke.tcl("value gain")]
