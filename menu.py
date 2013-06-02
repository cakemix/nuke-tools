''' menu.py for use with finPipeline
Copyright (C) 2012  Miles Lauridsen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl.html/>.'''

import os
import re
import sys
import nuke
import fin_Tools
import Send2Rush as s2r
import os.path
import djv_this
import fin_assetManager
import pixelfudger
import animatedSnap3D

### GET ENV VARS SETUP ###
finServer = os.environ.get('SERVER', None)
jobServer = os.environ.get('JOB_SERVER', None)
user = os.environ.get('USER', None)
### END ENV VARS SETUP ###


### BEGIN DJVIEW SETUP ###
## Use DJView as playback
menu = nuke.menu('Nuke')
m = menu.findItem('Render')
m.addCommand('Flipbook Selected in &DJV', 'nukescripts.flipbook( djv_this.djv_this, nuke.selectedNode() )', 'Ctrl+F', index=9)
### END DJVIEW SETUP


### BEGIN OCIO SETUP ###
import nukescripts.ViewerProcess; nukescripts.ViewerProcess.unregister_viewers()
import nukescripts.ViewerProcess; nukescripts.ViewerProcess.register_viewers(defaultLUTS = False, ocioConfigName = os.environ.get('OCIO', None));
### END OCIO SETUP ###


### BEGIN FAVORITES SETUP ###
## Add Favorites directories
nuke.addFavoriteDir('Job Server', jobServer )
toolbar = nuke.toolbar("Nodes")
### END FAVORITES SETUP ###

### BEGIN LUMA GIZMO SETUP ###
## LUMA Pictures gizmo collector

if __name__ == '__main__':
  # Just in case they didn't use the supplied init.py
  gizManager = globals().get('gizManager', None)
  if gizManager is None:
      print 'Problem finding GizmoPathManager - check that init.py was setup correctly'
  else:
      gizManager.addGizmoMenuItems()
      # Don't need it no more...
      del gizManager
### END LUMA SETUP ###


### BEGIN ASSET MANAGEMENT SETUP ###
# CREATE A READ NODE AND OPEN THE "DB" TAB
def customRead():
        n = nuke.createNode( 'Read' )
        n['DB'].setFlag( 0 )

# ADD CUSTOM READ AND WRITE TO TOOLBAR
nuke.menu( 'Nodes' ).addCommand( 'Image/WriteAsset', lambda: nuke.createNode( 'WriteAsset' ), 'w' )
nuke.menu( 'Nodes' ).addCommand( 'Image/Read', customRead, 'r' )

# ADD EASY SAVE TO SHOT MENU
shotMenu = '%s - %s' % ( os.getenv( 'SEQ' ), os.getenv('SHOT') )
nuke.menu( 'Nuke' ).addCommand( shotMenu+'/Easy Save', fin_assetManager.easySave )


# SET FILE BROWSER FAVORITES
nuke.addFavoriteDir(
    name = 'NUKE SCRIPTS',
    directory = fin_assetManager.nukeDir(),
    type = nuke.SCRIPT)

# HELPER FUNCTION FOR NUKE SCRIPT PANEL
def nkPanelHelper():
        # GET ALL NUKE SCRIPTS FOR CURRENT SHOT
        nkScripts = fin_assetManager.getNukeScripts()
        if not nkScripts:
                # IF THERE ARE NONE DON'T DO ANYTHING
                return
        # CREATE PANEL
        p = fin_assetManager.NkPanel( nkScripts )
        # ADJUST SIZE
        p.setMinimumSize( 200, 200 )

        # IF PANEL WAS CONFIRMED AND A NUKE SCRIPT WAS SELECTED, OPEN IT
        if p.showModalDialog():
                if p.selectedScript:
                        nuke.scriptOpen( p.selectedScript )

# ADD CALLBACKS
nuke.addOnScriptSave( fin_assetManager.checkScriptName )
nuke.addOnUserCreate( nkPanelHelper, nodeClass='Root')
nuke.addOnUserCreate( fin_assetManager.createVersionKnobs, nodeClass='Read' )
nuke.addKnobChanged( fin_assetManager.updateVersionKnob, nodeClass='Read' )
#nuke.addBeforeRender( assetManager.createOutDirs, nodeClass='Write' )
nuke.knobDefault( 'Write.beforeRender', 'fin_assetManager.createOutDirs()')
### END ASSET MANAGEMENT SETUP ###


### BEGIN RUSH SETUP ###
## Uncomment this if RUSH is used
#m = menubar.addMenu("Render")
#m.addCommand("Create Paths", "fin_Tools.createPaths()")
#m.addCommand("Fix Paths", "fixPath.fixPath()")
#m.addCommand("Send2Rush", "s2r.Nuke2Rush()")
### END RUSH SETUP ###


### BEGIN GIZMO SETUP ###
##Keyer_CB
nuke.menu("Nodes").addCommand("Keyer/Keyer_CB", "nuke.createNode('Keyer_CB')", icon="Keyer.png")

##ScannedGrain_CB
nuke.menu("Nodes").addCommand("Draw/ScannedGrain_CB", "nuke.createNode('ScannedGrain_CB')", icon="ScannedGrainCB.png")

##Grain_CB
nuke.menu("Nodes").addCommand("Draw/Grain_CB", "nuke.createNode('Grain_CB')", icon="GrainCB.png")

### END GIZMO SETUP ###


### BEGIN MENU SETUP ###
## Presets Backdrop
presetBackdropMenu = nuke.menu('Nuke').addMenu('presetBackdrop')
presetBackdropMenu.addCommand('Preset Backdrop', 'presetBackdrop.presetBackdrop()', 'ctrl+alt+b')

## Victor Menu
VMenu = toolbar.addMenu('V!ctor', icon='V_Victor.png')
VMenu.addCommand('V_CheckMatte', 'nuke.createNode("V_CheckMatte")', icon='V_CheckMatte.png')
VMenu.addCommand('V_IdBuilder', 'nuke.createNode("V_IdBuilder")', icon='V_IdBuilder.png')
VMenu.addCommand('V_IdPackage', 'nuke.createNode("V_IdPackage")', icon='V_IdPackage.png')
VMenu.addCommand('V_IdFilter', 'nuke.createNode("V_IdFilter")', icon='V_IdFilter.png')
VMenu.addCommand('V_ColorRenditionChart', 'nuke.createNode("V_ColorRenditionChart")', icon='V_ColorRenditionChart.png')
VMenu.addCommand('V_ColorTracker', 'nuke.createNode("V_ColorTracker")', icon='V_ColorTracker.png')
VMenu.addCommand('V_CompareView', 'nuke.createNode("V_CompareView")', icon='V_CompareView.png')
VMenu.addCommand('V_Slate', 'nuke.createNode("V_Slate")', icon='V_Slate.png')

## DW Menu
dwMenu = toolbar.addMenu("DW Tools", "dw_menu.png")
dwMenu.addCommand("Cameras/Camera Project Current Frame", "dw_camProjSet_v1_1.camProjSingle()", "shift+c", "dw_camProjCurFrame.png")
dwMenu.addCommand("Cameras/Camera Project Source", "dw_camProjSet_v1_1.camProjMultiple()", "ctrl+shift+c", "dw_camProjSource.png")

### END MENU SETUP ###

### End