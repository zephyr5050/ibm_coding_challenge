#============================== IBM Code Challenge =============================
# mat_widgets.py
#
# Provides several widgets for use in constructing and configuring the main GUI.
#
# Description:
#     This file provides many custom widgets which are subclassed from Qt widgets
#     to provide additional, custom functionality. The general widgets provided
#     include a button which uses images and can cycle through images as it's
#     clicked, a collapsable frame, and a clickable frame.
#
#===============================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def configureQLabel(label, font = 'Calibri', font_size = 12, font_emphasis = None,
                    font_color = QColor(60,60,60), alignment = None):
    """
    Simple function for configuring a QLabel in a variety of ways. Provided for
    convenience.
    """
    label.setFont(QFont(font, font_size, font_emphasis) if font_emphasis else QFont(font, font_size))
    label.setStyleSheet('color: #{}'.format(hex(font_color.rgba())[2:]))
    if alignment: label.setAlignment(alignment)

class ImageButton(QAbstractButton):
    """
    Provides a button which presents an image to the user, rather than a simple
    rectangle. Additionally, multiple images can be provided and this will
    cycle through the images as the button is clicked. This can be used to cycle
    through a normal image and a "cancel" image for example.
    """

    def __init__(self, *args, size = None, parent = None):
        """
        Initialization function

        Input:
            size: The size to make the image. If none is provided, defaults to
                the image size.
            parent: The parent widget which owns this widget, to be passed
                on to the super class constructor.
        """
        
        # Call super constructor
        super().__init__(parent)
        
        # Define instance variables
        self.enabled = True
        self.__images = list(args)
        self.__state = 0
        self.__pixmap = QPixmap(self.__images[self.__state])
        if size:
            # Use provided size if one was provided
            self.__size = size
        else:
            # Use size of image if no size was provided
            self.__size = QSize(self.__pixmap.width(), self.__pixmap.height())

    def nextImage(self):
        """Update the image if more than one was provided"""
        if len(self.__images) > 1:
            self.__state = (self.__state + 1) % len(self.__images)
            self.__pixmap = QPixmap(self.__images[self.__state])
        
    def mouseReleaseEvent(self, event):
        # Do not respond if button is disabled
        if not self.enabled: return

        # Move to the next image
        self.nextImage()
        
        # Call the super method
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.__pixmap)

    def sizeHint(self):
        return self.__size

    @property
    def state(self):
        return self.__state

class LineLabel(QFrame):
    """
    Defines a label which has an extended line after it. This is useful for headers
    and separating sections. In reality, it is a frame, despite being called a
    LineLabel.
    """

    def __init__(self, text, font = 'Calibri', fontSize = 12, fontEmphasis = None, fontColor = QColor(60, 60, 60)):
        super().__init__()

        # Create the grid and add it to the frame
        self.grid = QGridLayout(margin = 0, spacing = 2)
        self.setLayout(self.grid)

        # Create the QLabel
        self.label = QLabel(text)
        configureQLabel(self.label, font, fontSize, fontEmphasis, fontColor)
        self.grid.addWidget(self.label, 0, 0, 3, 1)

        # Create the separator
        self.grid.addWidget(Separator('Horizontal'), 1, 1)

        # Configure the grid
        self.grid.setColumnStretch(1, 1)
        self.grid.setRowStretch(0, 2)
        self.grid.setRowStretch(2, 1)

class Separator(QFrame):
    """
    Convenience class used for creating a line as a separator. This is actually
    just a frame with no size and a one pixel border.
    """

    def __init__(self, direction = 'Horizontal', lineWidth = 1):
        super().__init__()

        if direction == 'Horizontal':
            self.setFrameShape(QFrame.HLine)
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        elif direction == 'Vertical':
            self.setFrameShape(QFrame.VLine)
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        else:
            raise Exception('Invalid separator direction. Expected Horizontal or Vertical.')

        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(lineWidth)

class CollapsableSection(QFrame):
    """
    Creates a frame which is designed for collapsing and hiding its main content.
    This uses a LineLabel for the header and an ImageButton to display the hidden
    or visible state. The header line is a clickable frame.
    """

    def __init__(self, title, initialCollapseState):
        super().__init__()

        # Set class variables
        self.__collapsed = False
        
        # Create the grid and add it to the frame
        self.__grid = QGridLayout(margin = 0, spacing = 2)
        self.setLayout(self.__grid)

        # -- Create the Title Frame --------------------------------------------

        #titleFrame = QFrame()
        titleFrame = ClickableFrame(self.toggleCollapseState)
        titleGrid = QGridLayout(margin = 0, spacing = 5)
        titleFrame.setLayout(titleGrid)

        # Add the line label widget
        titleGrid.addWidget(LineLabel(title, fontEmphasis = QFont.Bold), 0, 0)

        # Create the collapse button
        self.collapseButton = ImageButton('imgs/down_triangle.png', 'imgs/up_triangle.png', size = QSize(8,8))
        self.collapseButton.clicked.connect(self.__collapse)
        titleGrid.addWidget(self.collapseButton, 0, 1)

        # Configure the title grid
        titleGrid.setColumnStretch(0, 1)

        # Add the title frame to the grid
        self.__grid.addWidget(titleFrame, 0, 0)

        # -- Create the widget frame -------------------------------------------

        self.__widgetFrame = QFrame()
        self.__widgetGrid = QGridLayout(margin = 0, spacing = 2)
        self.__widgetFrame.setLayout(self.__widgetGrid)

        # Add the widget frame to the grid
        self.__grid.addWidget(self.__widgetFrame, 1, 0)

        # Set the initial collapse state
        self.setCollapseState(initialCollapseState)

    def setCollapseState(self, state):
        self.__widgetFrame.show() if state == False else self.__widgetFrame.hide()
        self.collapseButton.nextImage()
        self.__collapsed = state

    def toggleCollapseState(self):
        self.__collapsed = not self.__collapsed
        self.setCollapseState(self.__collapsed)

    # == Adding widgets & configuring the widgets grid methods =================
    
    def addWidget(self, widget, *args, **kwargs):
        self.__widgetGrid.addWidget(widget, *args, **kwargs)

    def setRowMinimumHeight(self, row, minHeight):
        self.__widgetGrid.setRowMinimumHeight(row, minHeight)

    def setRowStretch(self, row, stretch):
        self.__widgetGrid.setRowStretch(row, stretch)

    def setColumnMinimumWidth(self, col, minWidth):
        self.__widgetGrid.setColumnMinimumHeight(col, minWidth)

    def setColumnStretch(self, col, stretch):
        self.__widgetGrid.setColumnStretch(col, stretch)

    def setContentsMargin(self, margin):
        self.__widgetGrid.setContentsMargins(margin, margin, margin, margin)

    def setContentsMargins(self, left_margin, top_margin, right_margin, bottom_margin):
        self.__widgetGrid.setContentsMargins(left_margin, top_margin, right_margin, bottom_margin)

    def setSpacing(self, spacing):
        self.__widgetGrid.setSpacing(spacing)

    @property
    def grid(self):
        return self.__widgetGrid

    # == Event Callbacks =======================================================

    def __collapse(self):
        self.__widgetFrame.show() if self.__collapsed else self.__widgetFrame.hide()
        self.__collapsed = not self.__collapsed

class ClickableFrame(QFrame):
    """
    Convenience class which implements the mousePressEvent and executes a callback
    when the event is triggered.
    """

    def __init__(self, callback):
        super().__init__()
        self.__callback = callback

    def mousePressEvent(self, event):
        event.accept()
        self.__callback()
