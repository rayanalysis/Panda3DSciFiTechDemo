
from direct.showbase.ShowBase import ShowBase

from panda3d.core import WindowProperties, TextNode, Vec4
from direct.gui.DirectGui import *

import Section1.section1 as Section1
import Section2.Section2 as Section2
import Section3.Section3 as Section3
import Section2.Section2 as Section4

import common

from Ships import shipSpecs

TAG_PREVIOUS_MENU = "predecessor"

class Game():
    @staticmethod
    def makeButton(text, command, menu, width, extraArgs = None, leftAligned = True):
        if leftAligned:
            frame = (-0.1, width, -0.75, 0.75)
            alignment = TextNode.ALeft
        else:
            frame = (-width*0.5 , width*0.5, -0.75, 0.75)
            alignment = TextNode.ACenter
        btn = DirectButton(text = text,
                           command = command,
                           scale = 0.1,
                           parent = menu,
                           text_align = alignment,
                           frameSize = frame,
                           text_pos = (0, -0.375)
                           )
        if extraArgs is not None:
            btn["extraArgs"] = extraArgs
        return btn

    def __init__(self):

        common.gameController = self

        properties = WindowProperties()
        properties.setSize(1280, 720)
        common.base.win.requestProperties(properties)

        common.base.win.setClearColor(Vec4(0, 0, 0, 1))

        common.base.disableMouse()

        common.base.exitFunc = self.destroy

        common.base.accept("window-event", self.windowUpdated)

        self.currentMenu = None

        ### Main Menu

        self.mainMenuBackdrop = DirectFrame(
                                            frameSize = (-1/common.base.aspect2d.getSx(), 1/common.base.aspect2d.getSx(), -1, 1),
                                           )

        self.title = DirectLabel(text = "CAPTAIN PANDA",
                                 parent = self.mainMenuBackdrop,
                                 scale = 0.07,
                                 pos = (0, 0, 0.9),
                                 text_align = TextNode.ALeft)
        self.title = DirectLabel(text = "and the",
                                 parent = self.mainMenuBackdrop,
                                 scale = 0.05,
                                 pos = (0, 0, 0.85),
                                 text_align = TextNode.ALeft)
        self.title = DirectLabel(text = "INVASION OF THE MECHANOIDS!",
                                 parent = self.mainMenuBackdrop,
                                 scale = 0.1,
                                 pos = (0, 0, 0.7625),
                                 text_align = TextNode.ALeft)

        self.mainMenuPanel = DirectFrame(
                                    frameSize = (0, 1.25, -1, 1),
                                    frameColor = (0, 0, 0, 0.5)
                                   )

        buttons = []

        btn = Game.makeButton("New Game", self.startGame, self.mainMenuPanel, 10)
        buttons.append(btn)

        btn = Game.makeButton("Chapter Selection", self.selectSection, self.mainMenuPanel, 10)
        buttons.append(btn)

        btn = Game.makeButton("Options", self.openOptions, self.mainMenuPanel, 10)
        buttons.append(btn)

        btn = Game.makeButton("Quit", self.quit, self.mainMenuPanel, 10)
        buttons.append(btn)

        buttonSpacing = 0.2
        buttonY = (len(buttons) - 1)*0.5*buttonSpacing
        for btn in buttons:
            btn.setPos(0.1, 0, buttonY)
            buttonY -= buttonSpacing

        ### Options Menu

        self.optionsTop = 0.35
        self.currentOptionsZ = self.optionsTop
        self.optionSpacingHeading = 0.2

        self.optionsMenu = DirectDialog(
                                        frameSize = (-1, 1, -0.85, 0.85),
                                        fadeScreen = 0.5,
                                        pos = (0, 0, 0),
                                        relief = DGG.FLAT
                                       )
        self.optionsMenu.hide()

        label = DirectLabel(text = "Options",
                            parent = self.optionsMenu,
                            scale = 0.1,
                            pos = (0, 0, 0.65),
                            #text_font = self.font,
                            relief = None)

        self.optionsScroller = DirectScrolledFrame(
                                        parent = self.optionsMenu,
                                        relief = DGG.SUNKEN,
                                        scrollBarWidth = 0.1,
                                        frameSize = (-0.8, 0.9, -0.5, 0.5),
                                        canvasSize = (-0.8, 0.8, -0.4, 0.5),
                                        autoHideScrollBars = False,
                                    )
        self.optionsScroller.horizontalScroll.hide()

        self.addOptionHeading("General")
        self.addOptionSlider("Music Volume", (0, 100), 1, self.setMusicVolume)
        self.addOptionSlider("Sound Volume", (0, 100), 1, self.setSoundVolume)
        self.addOptionHeading("Section 1")
        self.addOptionHeading("Section 2")
        Section2.addOptions()
        self.addOptionHeading("Section 3")
        self.addOptionHeading("Section 4")

        btn = Game.makeButton("Back", self.closeCurrentMenu, self.optionsMenu, 5, leftAligned = False)
        btn.setPos(0, 0, -0.7)

        ### Section Menu

        self.sectionMenu = DirectDialog(
                                        frameSize = (0, 2, -0.85, 0.85),
                                        fadeScreen = 0.5,
                                        pos = (0, 0, 0),
                                        relief = DGG.FLAT
                                       )
        self.sectionMenu.hide()

        label = DirectLabel(text = "Select a Chapter:",
                            parent = self.sectionMenu,
                            scale = 0.1,
                            pos = (0.085, 0, 0.65),
                            text_align = TextNode.ALeft)

        buttons = []

        btn = Game.makeButton("Chapter 1 // A Warrior's Choice", self.startSection, self.sectionMenu, 15, extraArgs = [0])
        buttons.append(btn)

        btn = Game.makeButton("Chapter 2 // Across the Night", self.startSection, self.sectionMenu, 15, extraArgs = [1])
        buttons.append(btn)

        btn = Game.makeButton("Chapter 3 // Facing the Foe", self.startSection, self.sectionMenu, 15, extraArgs = [2])
        buttons.append(btn)

        btn = Game.makeButton("Chapter 4 // The Escape", self.startSection, self.sectionMenu, 15, extraArgs = [3])
        buttons.append(btn)

        buttonSpacing = 0.25
        buttonY = (len(buttons) - 1)*0.5*buttonSpacing
        for btn in buttons:
            btn.setPos(0.1, 0, buttonY)
            buttonY -= buttonSpacing

        btn = Game.makeButton("Back", self.closeCurrentMenu, self.sectionMenu, 5)
        btn.setPos(0.1, 0, -0.7)

        ### Game-over menu

        self.gameOverScreen = DirectDialog(frameSize = (-0.5, 0.5, -0.7, 0.7),
                                           fadeScreen = 0.4,
                                           relief = DGG.FLAT)
        self.gameOverScreen.hide()

        label = DirectLabel(text = "Game Over!",
                            parent = self.gameOverScreen,
                            scale = 0.1,
                            pos = (0, 0, 0.55),
                            #text_font = self.font,
                            relief = None)

        btn = DirectButton(text = "Retry",
                           command = self.restartCurrentSection,
                           pos = (0, 0, 0.25),
                           parent = self.gameOverScreen,
                           scale = 0.1,
                           #text_font = self.font,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           #relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Return to Menu",
                           command = self.openMenu,
                           pos = (0, 0, 0),
                           parent = self.gameOverScreen,
                           scale = 0.1,
                           #text_font = self.font,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           #relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Quit",
                           command = self.quit,
                           pos = (0, 0, -0.25),
                           parent = self.gameOverScreen,
                           scale = 0.1,
                           #text_font = self.font,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           #relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        ### Section 2 ship-selection menu

        buttons = []

        self.shipSelectionMenu = DirectDialog(
                                              frameSize = (0, 2, -0.7, 0.7),
                                              fadeScreen = 0.5,
                                              relief = DGG.FLAT
                                             )
        self.shipSelectionMenu.hide()
        self.shipSelectionMenu.setPythonTag(TAG_PREVIOUS_MENU, self.sectionMenu)

        label = DirectLabel(text = "Select a Ship:",
                            parent = self.shipSelectionMenu,
                            scale = 0.1,
                            pos = (0.085, 0, 0.5),
                            text_align = TextNode.ALeft)

        btn = Game.makeButton("Light fighter", self.sectionSpecificMenuDone, self.shipSelectionMenu, 15,
                              extraArgs = [self.shipSelectionMenu, 1, shipSpecs[0]])
        buttons.append(btn)

        btn = Game.makeButton("Medium Interceptor", self.sectionSpecificMenuDone, self.shipSelectionMenu, 15,
                              extraArgs = [self.shipSelectionMenu, 1, shipSpecs[1]])
        buttons.append(btn)

        btn = Game.makeButton("Heavy Bombardment Platform", self.sectionSpecificMenuDone, self.shipSelectionMenu, 15,
                              extraArgs = [self.shipSelectionMenu, 1, shipSpecs[2]])
        buttons.append(btn)

        buttonY = (len(buttons) - 1)*0.5*buttonSpacing
        for btn in buttons:
            btn.setPos(0.1, 0, buttonY)
            buttonY -= buttonSpacing

        btn = Game.makeButton("Back", self.closeCurrentMenu, self.shipSelectionMenu, 5)
        btn.setPos(0.1, 0, -0.55)

        ### Section-data

        self.currentSectionIndex = 0
        self.currentSectionData = None
        self.currentSectionObject = None

        # Stores section-modules and the menu, if any, that's to be
        # shown if they're loaded without the preceding section
        # being run
        self.sections = [
            (Section1, None),
            (Section2, self.shipSelectionMenu),
            (Section3, None),
            (Section4, None),
        ]

        ### Utility

        common.base.accept("f", self.toggleFrameRateMeter)
        self.showFrameRateMeter = False

    def addOptionSlider(self, text, rangeTuple, stepSize, callback):
        pass

    def addOptionHeading(self, text):
        label = DirectLabel(text = text,
                            text_align = TextNode.ACenter,
                            scale = 0.1,
                            parent = self.optionsScroller.getCanvas(),
                            pos = (0, 0, self.currentOptionsZ))
        self.currentOptionsZ -= self.optionSpacingHeading
        self.updateOptionsCanvasSize()

    def updateOptionsCanvasSize(self):
        self.optionsScroller["canvasSize"] = (-0.8, 0.8, self.currentOptionsZ, 0.5)

    def setMusicVolume(self, vol):
        pass

    def setSoundVolume(self, vol):
        pass

    def toggleFrameRateMeter(self):
        self.showFrameRateMeter = not self.showFrameRateMeter

        common.base.setFrameRateMeter(self.showFrameRateMeter)

    def windowUpdated(self, window):
        common.base.windowEvent(window)
        self.mainMenuBackdrop["frameSize"] = (-1/common.base.aspect2d.getSx(), 1/common.base.aspect2d.getSx(),
                                              -1/common.base.aspect2d.getSz(), 1/common.base.aspect2d.getSz())
        self.mainMenuPanel.setX(common.base.render2d, -1)
        self.mainMenuPanel["frameSize"] = (0, 1.25, -1/common.base.aspect2d.getSz(), 1/common.base.aspect2d.getSz())
        self.sectionMenu.setPos(common.base.render, -0.8, 0, 0)
        self.shipSelectionMenu.setPos(common.base.render, -0.6, 0, 0)

    def openMenu(self):
        self.currentSectionIndex = 0
        self.currentSectionData = None

        self.gameOverScreen.hide()
        self.mainMenuBackdrop.show()
        self.mainMenuPanel.show()

        self.currentMenu = None

    def openOptions(self):
        self.optionsMenu.show()
        self.currentMenu = self.optionsMenu

    def startGame(self):
        self.startSection(0)

    def startSection(self, index, data = None):
        self.sectionMenu.hide()

        specificMenu = self.sections[index][1]
        if specificMenu is not None and data is None:
            specificMenu.show()
            self.currentMenu = specificMenu
        else:
            self.startSectionInternal(index, data)

    def sectionSpecificMenuDone(self, menu, sectionIndex, data):
        menu.hide()
        self.startSectionInternal(sectionIndex, data)

    def startSectionInternal(self, index, data):
        if self.currentSectionObject is not None:
            self.currentSectionObject.destroy()

        self.mainMenuPanel.hide()
        self.mainMenuBackdrop.hide()
        self.currentMenu = None

        self.currentSectionIndex = index
        self.currentSectionData = data

        sectionModule = self.sections[index][0]

        if hasattr(sectionModule, "initialise"):
            initialisationMethod = sectionModule.initialise
        elif hasattr(sectionModule, "initialize"):
            initialisationMethod = sectionModule.initialize

        self.currentSectionObject = initialisationMethod(data)

    def selectSection(self):
        self.sectionMenu.show()
        self.currentMenu = self.sectionMenu

    def restartCurrentSection(self):
        self.gameOverScreen.hide()
        self.startSectionInternal(self.currentSectionIndex, self.currentSectionData)

    def gameOver(self):
        if self.currentSectionObject is not None:
            self.currentSectionObject.destroy()
            self.currentSectionObject = None

        if self.gameOverScreen.isHidden():
            self.gameOverScreen.show()

    def closeCurrentMenu(self):
        if self.currentMenu is not None:
            self.currentMenu.hide()
            if self.currentMenu.hasPythonTag(TAG_PREVIOUS_MENU):
                otherMenu = self.currentMenu.getPythonTag(TAG_PREVIOUS_MENU)
                otherMenu.show()
                self.currentMenu = otherMenu
            else:
                self.currentMenu = None

    def destroy(self):
        self.shipSelectionMenu.clearPythonTag(TAG_PREVIOUS_MENU)

    def quit(self):
        self.destroy()

        common.base.userExit()

game = Game()
common.base.run()
