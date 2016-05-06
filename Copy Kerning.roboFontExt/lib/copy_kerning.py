from vanilla import Button, HorizontalLine, Window, PopUpButton, TextBox, Sheet, ProgressBar
from defconAppKit.controls.fontList import FontList
from mojo.roboFont import OpenWindow, AllFonts, RGroups, RKerning

class CopyKerning:

    def __init__(self):
        if AllFonts() is None:
            from vanilla.dialogs import message
            message("No fonts open.", "Open or create a font to copy data to and fro.")
            return

        self.sourceFontList = AllFonts()
        self.destinationFontList = AllFonts()
        self.source_font = self.sourceFontList[0]
        self.destination_fonts = None
        self.groups = None
        self.kerning = None

        ## create a window
        self.w = Window((400, 500), "Copy Groups and Kerning", minSize=(500, 600))
        self.w.sourceTitle = TextBox((15, 20, 200, 20), "Source Font:")
        self.w.sourceFont = PopUpButton((15, 42, 340, 20), [f.info.familyName + ' ' + f.info.styleName for f in self.sourceFontList], callback=self.sourceCallback)
        self.w.desTitle = TextBox((15, 76, 200, 20), "Destination Fonts:")
        self.w.destinationFonts = FontList((15, 96, -15, -115), self.destinationFontList, selectionCallback=self.desCallback)
        self.w.copyButton = Button((-215, -40, 200, 20), 'Copy Groups & Kerning', callback=self.copyCallback)
        self.w.line = HorizontalLine((10, -60, -10, 1))
        self._updateDest()
        ## open the window
        self.w.open()

    def _updateDest(self):
        des = list(self.sourceFontList)
        des.remove(self.source_font)
        self.w.destinationFonts.set(des)

    def copyKerning(self, groups, kerning, source_font, destination_fonts):
        kerning = source_font.kerning.asDict()
        groups = source_font.groups
        for font in destination_fonts:
            font.groups.update(groups)
            font.kerning.update(kerning)

    def sourceCallback(self, sender):
        self.source_font = self.sourceFontList[sender.get()]
        self._updateDest()

    def desCallback(self, sender):
        self.destination_fonts = [sender.get()[x] for x in sender.getSelection()]

    def copyCallback(self, sender):
        self.sheet = Sheet((300, 50), self.w)
        self.sheet.bar = ProgressBar((10, 20, -10, 10), isIndeterminate=True, sizeStyle="small")
        self.sheet.open()
        self.sheet.bar.start()
        self.copyKerning(self.groups, self.kerning, self.source_font, self.destination_fonts)
        self.sheet.bar.stop()
        self.sheet.close()
        del self.sheet
        self.w.close()

OpenWindow(CopyKerning)
