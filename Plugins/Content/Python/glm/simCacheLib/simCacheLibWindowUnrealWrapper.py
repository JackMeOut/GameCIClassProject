#**************************************************************************
#*                                                                        *
#*  Copyright (C) Golaem S.A. - All Rights Reserved.                      *
#*                                                                        *
#**************************************************************************

from glm.ui import windowUnrealWrapper
from glm.Qtpy.Qt import QtCore, QtWidgets
import unreal
import os


#**********************************************************************
#
# SimCacheLibWindowUnrealWrapper
# Unreal wrapper for SimCacheLibWindow
#
#**********************************************************************
class SimCacheLibWindowUnrealWrapper(windowUnrealWrapper.WindowUnrealWrapper):
    #******************************************************************
    # Specific
    #******************************************************************

    #------------------------------------------------------------------
    # Returns the app stylesheet
    #------------------------------------------------------------------
    def getStyleSheet(self):
        return 'QWidget#itemLib:hover { background-color: #597b9b ; }'

    #------------------------------------------------------------------
    # Updates the item snapshot and returns it
    #------------------------------------------------------------------
    def updateItemSnapshot(self, item):
        return item

    #------------------------------------------------------------------
    # Create a sim cache proxy node, fills it from item and returns it
    #------------------------------------------------------------------
    def createSimCacheProxyFromItem(self, lib, itemIdx):

        # # should we use instanced characters
        # msgBox = QtWidgets.QMessageBox()
        # msgBox.setText("Do you want to use skinned characters ?")
        # msgBox.setInformativeText("If your characters are made of rigid meshes, and you don't need layout interactions, choose NO. Characters will use instancing, for better performances with high character count scenes, but the layout interactions will be disabled (no per-entity selection/displacement in viewport).\nIf your assets are skinned assets and/or you need to use layout interactions, choose YES (this is the default, and former, case).")
        # msgBox.setStandardButtons( QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel )
        # msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        # msgBoxResult = msgBox.exec_()
        # if (msgBoxResult == QtWidgets.QMessageBox.Cancel):
            # return
        
        item = lib.getLibItemAt(itemIdx)
        if (item.isInitialized()):
            location = unreal.Vector()
            # create cache node
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.GolaemCache.static_class(), location)
            if actor is not None:
                # we also need to set editable properties one by one (so that they are not overriden when playing in PIE, which set cacheLibraryFile and cacheIndex again)
                actor.set_editor_property('bEnableLayout', item.enableLayout)
                actor.set_editor_property('layoutFile', item.layoutFile)
                actor.set_editor_property('terrainFileSource', item.sourceTerrain) # source terrain may need some unlock / lock to be set
                actor.set_editor_property('terrainFileDest', item.destTerrain )
                actor.set_editor_property('currentFrame', item.startFrame + 1)
                actor.set_editor_property('startFrame', item.startFrame)
                actor.set_editor_property('endFrame', item.endFrame)
                actor.set_editor_property('charactersFiles',  item.characterFiles)
                actor.set_editor_property('cacheDirectory', item.cacheDir)
                actor.set_editor_property('cacheName', item.cacheName) # cache name last to have everything for init
                # actor.set_editor_property('crowdFields', ';'.join(item.crowdFields))
                actor.set_editor_property('crowdFields', item.crowdFields)

                # get browser skeletal meshes
                skeletalMeshes = dict()
                allContent = unreal.EditorAssetLibrary.list_assets('/Game/')
                for content in allContent:
                    contentTag = unreal.EditorAssetLibrary.get_tag_values(content)
                    if 'Skeleton' in contentTag:
                        contentName = os.path.splitext(os.path.basename(content))[0]
                        skeletalMeshes[contentName] = content
                # get character files name
                characterFiles = item.characterFiles.split(';')
                inCharacters = actor.get_editor_property('inCharacters')
                skeletalMeshList = []
                if len(skeletalMeshes) and len(characterFiles) == len(inCharacters) and len(characterFiles):
                    self.log('info', 'Trying to connect SkeletalMeshes with similar names')
                    for characterFile in characterFiles:
                        characterName = os.path.splitext(os.path.basename(characterFile))[0]
                        if characterName in skeletalMeshes:
                            skeletalMeshObj = unreal.EditorAssetLibrary.load_asset(skeletalMeshes[characterName])
                            skeletalMeshList.append(skeletalMeshObj)
                            self.log('info', 'Found a skeletalMesh asset named "' + characterName + '", connect it!')
                        else:
                            skeletalMeshList.append(None)
                            self.log('info', 'Could not find a skeletalMesh asset named "' + characterName + '"')
                    # connect
                    #print skeletalMeshList
                    actor.set_editor_property('inCharacters', skeletalMeshList)
            return actor
        return None

    #------------------------------------------------------------------
    # Updates a sim cache lib from a set of nodes and returns it
    #------------------------------------------------------------------
    def fillSimCacheLibFromProxies(self, lib, nodes):
        return lib

    #------------------------------------------------------------------
    # Return true if a button is available is this interface
    #------------------------------------------------------------------
    def isButtonAvailable(self, buttonName):
        if buttonName == "Import from selected / scene Simulation Cache Proxy" or buttonName == "Update Thumbnail from Viewport":
            return False
        return True
