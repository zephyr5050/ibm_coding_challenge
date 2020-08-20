#============================== IBM Code Challenge =============================
# mat_gui.py
#
# Creates GUI for user to interact with
#
# Description:
#     This generates a GUI that allows the user to enter two matrices, select
#     a mathematical operation, and displays the operation result to the user.
#     The class implements the __init__ function to construct the GUI and breaks
#     each component out into a new function to help compartmentalize the
#     construction.
#
# Todo:
#     Add save/restore callback and link to menu items
#===============================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import re

import pdb

from mat_widgets import *
from mat_operation import *

class MatOpGUI(QMainWindow):

    #===========================================================================
    # Define class constants
    #===========================================================================

    # Define the list of mathematical operations the user can perform on the
    # two operations.
    OPERATIONS = ['Multiply',
                  'Sum of Column of Product',
                  'Product of Column of Product',
                  'Cumulative Sum Along Column of Product',
                  'Cumulative Product Along Column of Product',
                  'Sum of Row of Product',
                  'Product of Row of Product',
                  'Cumulative Sum Along Row of Product',
                  'Cumulative Product Along Row of Product',
                  'Min of Product',
                  'Max of Product',
                  'Mean of Product',
                  'Median of Product',
                  'Total Sum of Product',
                  'Total Product of Product']

    # Define the operations that, when selected, will cause the operations
    # selection row/column entry field to appear to the user.
    OPS_TO_MAKE_ENTRY_VISIBLE = ['Sum of Column of Product',
                                 'Product of Column of Product',
                                 'Sum of Row of Product',
                                 'Product of Row of Product']

    # Define the operations that will act on a row of the resultant matrix.
    # This will be used to determine the placeholder text of a line edit field
    # for entering a row/column, to help the user.
    OPS_ON_ROW = ['Sum of Row of Product',
                  'Product of Row of Product']
    
    #===========================================================================
    # Initialization function
    #===========================================================================

    def __init__(self):
        """
        Initialization function for the MatOpGUI class. This will construct the
        GUI, primarily through the __createGUI method, and display it to the user.
        """

        # Call the super class init function to make sure this generates properly
        super().__init__()

        # -- Define Instance Variables -----------------------------------------



        # Define variables for GUI properties
        self.__fontFamily = 'Calibri'
        self.__fontColor  = QColor(250,250,250)
        self.__guiColor   = QColor(162, 62, 72) # Official GUI color

        # Define counter for the number of operations performed
        self.__opCounter = 0

        # -- Set Window Properties ---------------------------------------------

        self.setAcceptDrops(True)
        self.setWindowTitle('Matrix Operations')
        self.resize(800,400)
        self.setWindowIcon(QIcon('imgs/icon.png'))

        # -- Create and Show the GUI -------------------------------------------
        
        # Create and show the GUI
        self.__createGUI()
        self.show()

    def frame(func):
        """
        Wrapper function for creating frames in a widget. This allows a function
        to simply add content to a frame without handling the process of creating
        grids and frames. This will automatically use a QGridLayout.
        """

        def wrapper(self, pos, *args, grid = None, gridMargin = 0, gridSpacing = 0,
                    bgcolor = QColor(255,255,255,255), frameShape = None,
                    frameShadow = None, lineWidth = 0, **kwargs):

            # Create the QFrame and QGridLayout
            kwargs['frame'] = QFrame(frameShape = frameShape, frameShadow = frameShadow, lineWidth = lineWidth)
            kwargs['grid'] = QGridLayout(margin = gridMargin, spacing = gridSpacing)

            # Call the wrapped function
            func(self, *args, **kwargs)
            
            # Set the background color of the frame
            kwargs['frame'].setAutoFillBackground(True)
            p = kwargs['frame'].palette()
            p.setColor(kwargs['frame'].backgroundRole(), bgcolor)
            kwargs['frame'].setPalette(p)

            # Set the grid created in this function as the frame's layout and
            # add the frame to the parent's grid at the position provided
            kwargs['frame'].setLayout(kwargs['grid'])
            if grid is not None:
                grid.addWidget(kwargs['frame'], *pos)
            else:
                self.grid.addWidget(kwargs['frame'], *pos)

            # Return the frame
            return kwargs['frame']
        
        return wrapper

    #===========================================================================
    # Level 0: Top level GUI creation and menu bar
    #===========================================================================

    def __createGUI(self):
        """
        Highest level function used to create the GUI components
        """

        # -- Define Top-level Components ---------------------------------------
        
        self.widget = QWidget(self)  # The central widget in the main window
        self.grid = QGridLayout()    # The layout manager of the central widget
        
        self.__createMenuBar()     # The menu bar

        # -- Main Gui Components -----------------------------------------------

        self.__headerBar = self.__createHeaderBar((0,0), gridMargin = 5, gridSpacing = 15, bgcolor = self.__guiColor)
        self.__contentFrame = self.__createContentFrame((1,0), gridMargin = 5, gridSpacing = 5)

        # -- Setup the Grid ----------------------------------------------------

        self.grid.setContentsMargins(0,0,0,0)
        self.grid.setSpacing(0)
        self.grid.setRowStretch(1,1)

        # -- Set the Main Widget Properties ------------------------------------

        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)

    def __createMenuBar(self):
        """
        Creates the menu bar of the GUI and adds various menus and items to
        perform tasks.
        """
        
        # Use the PyQt menu construct. This is particularly important for Macs
        # because it will keep the menubar with the GUI window rather than
        # placing it at the top of the screen, as is usual for Macs. We don't
        # want this to happen because Macs take control of the menus if you have
        # it up there and can cause unexpected results.
        self.menuBar().setNativeMenuBar(False)

        # -- File Menu ---------------------------------------------------------

        fileMenu = self.menuBar().addMenu('File')
        fileMenu.setTearOffEnabled(True)

        # Save Menu Item
        saveMenuItem = QAction('Save', fileMenu, shortcut = 'Ctrl+S')
        saveMenuItem.triggered.connect(self.__save)
        fileMenu.addAction(saveMenuItem)

        # Load Menu Item
        loadMenuItem = QAction('Load', fileMenu, shortcut = 'Ctrl+L')
        loadMenuItem.triggered.connect(self.__askForFileAndLoad)
        fileMenu.addAction(loadMenuItem)
        
        # -- Options Menu ------------------------------------------------------

        optionsMenu = self.menuBar().addMenu('Options')
        optionsMenu.setTearOffEnabled(True)

        # Clear Menu Item
        clearMenuItem = QAction('Clear All', optionsMenu, shortcut = 'Ctrl+A')
        clearMenuItem.triggered.connect(self.__clearAll)
        optionsMenu.addAction(clearMenuItem)

        optionsMenu.addSeparator()

        # Quit Menu Item
        quitMenuItem = QAction('Quit', optionsMenu, shortcut = 'Ctrl+Q')
        quitMenuItem.triggered.connect(self.close)
        optionsMenu.addAction(quitMenuItem)

    #===========================================================================
    # Level 1: Header and Main Content Frame
    #===========================================================================

    @frame
    def __createHeaderBar(self, *args, **kwargs):
        """
        Create the large header bar at the top of the GUI. This just adds a nice,
        convenient banner at the top for branding.
        """
        
        # Create the Matrix Operations Label, configure it, and add it to the grid
        matOpLabel = QLabel('Matrix Operations')
        configureQLabel(matOpLabel, font = self.__fontFamily, font_size = 20,
                        font_color = self.__fontColor, alignment = Qt.AlignCenter)
        kwargs['grid'].addWidget(matOpLabel, 0, 1)

    @frame
    def __createContentFrame(self, *args, **kwargs):
        """
        Create the main content of the GUI. This is a second frame below the header.
        This calls several sub-functions that create specific elements of the main
        content frame.
        """

        # Create the frame at the top for entering the name of the run
        runNameFrame = self.__createRunNameFrame(
            (0,0,1,2), grid = kwargs['grid'], gridmargin = 5, gridSpacing = 5,
        )

        # Set the tool tip for this frame to help the user out
        runNameFrame.setToolTip('Optionally choose a name for your run.')

        # -- Create Matrix Input Frames ----------------------------------------

        # Create the two frames which allows the user to input the two matrices
        self.__matrixAFrame = self.__createMatrixAInputFrame(
            (1,0), grid = kwargs['grid'], gridMargin = 5, gridSpacing = 5,
            frameShape = QFrame.StyledPanel, frameShadow = QFrame.Sunken, lineWidth = 0,
        )
        self.__matrixBFrame = self.__createMatrixBInputFrame(
            (1,1), grid = kwargs['grid'], gridMargin = 5, gridSpacing = 5,
            frameShape = QFrame.StyledPanel, frameShadow = QFrame.Sunken, lineWidth = 0,
        )

        # Set the tool tips for this frame to help the user out.
        self.__matrixAFrame.setToolTip((
            'Enter values for Matrix A here. You can change the matrix size to\n'
            'a max of 10x10 and also randomly generate values for the matrix.'
        ))
        self.__matrixBFrame.setToolTip((
            'Enter values for Matrix B here. You can change the matrix size to\n'
            'a max of 10x10 and also randomly generate values for the matrix.'
        ))

        # -- Create Operation Selection Frame ----------------------------------

        # Create the frame below the two matrices for selecting the matrix
        # operation to perform
        opSelectFrame = self.__createOperationSelectionFrame(
            (2,0,1,2), grid = kwargs['grid'], gridMargin = 0, gridSpacing = 5
        )

        # Set the tool tip for this frame to help the user out
        opSelectFrame.setToolTip((
            'Select an operation to perform from the dropdown list. Some\n'
            'operations act on a single row/column of a matrix. Hit Go!\n'
            'to perform the operation.'
        )) 

        # -- Create Output Text Box --------------------------------------------

        # Create the output text box.
        self.__outputTextBox = QTextEdit()

        # Make it so user's can't modify the text
        self.__outputTextBox.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        
        # Do not allow text wrapping (to prevent the output from becoming too
        # confusing).
        self.__outputTextBox.setLineWrapMode(QTextEdit.NoWrap)

        # Update the font to a monospaced font.
        font = self.__outputTextBox.currentFont()
        font.setPointSize(8)
        font.setFamily('courier')
        self.__outputTextBox.setFont(font)

        # Make it a least 400 pixels tall
        self.__outputTextBox.setMinimumHeight(400)

        # Make the text box initially invisible until data needs to be displayed
        # so as not to confuse the user.
        self.__outputTextBox.setVisible(False)

        # Add to the grid
        kwargs['grid'].addWidget(self.__outputTextBox, 3, 0, 1, 2)

        # -- Set Grid Properties -----------------------------------------------

        kwargs['grid'].setRowStretch(1, 1)
        kwargs['grid'].setColumnStretch(0, 1)
        kwargs['grid'].setColumnStretch(1, 1)

    #===========================================================================
    # Level 2: Name, Matrix, Options, and Output Frames
    #===========================================================================

    @frame
    def __createRunNameFrame(self, *args, **kwargs):
        """
        Create the frame which allows users to enter the name of the run
        """

        # Create the QLabel giving direction to the user
        kwargs['grid'].addWidget(QLabel('Name Your Run'), 0, 0)

        # Create the line edit for the user to enter the name
        self.__nameLineEdit = QLineEdit()
        self.__nameLineEdit.setPlaceholderText('Enter run name...')
        kwargs['grid'].addWidget(self.__nameLineEdit, 0, 1)

        # Set grid properties
        kwargs['grid'].setColumnStretch(1, 1)

    @frame
    def __createMatrixAInputFrame(self, *args, **kwargs):
        """
        Create the input frame for defining Matrix A. This has a label at the
        top demarking this as Matrix A. It has a sub-frame for changing the size
        of the frame, a table for defining the matrix, and a sub-frame for choosing
        to randomly generate the matrix.
        """

        # Create the label at the top of this frame, labeling this as Matrix A
        sectionLabel = QLabel('Matrix A')
        configureQLabel(sectionLabel, font = self.__fontFamily, font_size = 16,
                        alignment = Qt.AlignCenter)
        kwargs['grid'].addWidget(sectionLabel, 0, 0)

        # Create section for specifying the matrix size
        self.__createMatrixASizeFrame(
            (1,0), grid = kwargs['grid'], gridMargin = 0, gridSpacing = 0
        )

        # Create section for inputing the matrix. Default to a 3x3 matrix.
        self.__matrixAInputTable = QTableWidget(3, 3)
        font = self.__matrixAInputTable.horizontalHeader().font()
        font.setWeight(QFont.Bold)
        self.__matrixAInputTable.setAlternatingRowColors(True)
        self.__matrixAInputTable.horizontalHeader().setFont(font)
        self.__matrixAInputTable.verticalHeader().setFont(font)
        for row in range(3):
            for col in range(3):
                self.__matrixAInputTable.setItem(row, col, QTableWidgetItem(''))
        kwargs['grid'].addWidget(self.__matrixAInputTable, 2, 0)

        # Create section for random matrix generation
        self.__createMatrixARandFrame(
            (3,0), grid = kwargs['grid'], gridMargin = 0, gridSpacing = 0
        )

        # Set the grid properties|
        kwargs['grid'].setRowStretch(2,1)
        
    @frame
    def __createMatrixBInputFrame(self, *args, **kwargs):
        """
        Create the input frame for defining Matrix B. This has a label at the
        top demarking this as Matrix B. It has a sub-frame for changing the size
        of the frame, a table for defining the matrix, and a sub-frame for choosing
        to randomly generate the matrix.
        """

        # Create the label at the top of this frame, labeling this as Matrix B
        sectionLabel = QLabel('Matrix B')
        configureQLabel(sectionLabel, font = self.__fontFamily, font_size = 16,
                        alignment = Qt.AlignCenter)
        kwargs['grid'].addWidget(sectionLabel, 0, 0)

        # Create section for specifying the matrix size
        self.__createMatrixBSizeFrame(
            (1,0), grid = kwargs['grid'], gridMargin = 0, gridSpacing = 0
        )

        # Create section for inputing the matrix
        self.__matrixBInputTable = QTableWidget(3, 3)
        font = self.__matrixBInputTable.horizontalHeader().font()
        font.setWeight(QFont.Bold)
        self.__matrixBInputTable.setAlternatingRowColors(True)
        self.__matrixBInputTable.horizontalHeader().setFont(font)
        self.__matrixBInputTable.verticalHeader().setFont(font)
        for row in range(3):
            for col in range(3):
                self.__matrixBInputTable.setItem(row, col, QTableWidgetItem(''))
        kwargs['grid'].addWidget(self.__matrixBInputTable, 2, 0)

        # Create section for random matrix generation
        self.__createMatrixBRandFrame(
            (3,0), grid = kwargs['grid'], gridMargin = 0, gridSpacing = 0
        )

        # Set the grid properties|
        kwargs['grid'].setRowStretch(2,1)

    @frame
    def __createOperationSelectionFrame(self, *args, **kwargs):
        """
        Create the frame which allows the user select the math operation to
        perform.
        """
        
        kwargs['grid'].addWidget(QLabel('Select the Operation:'), 2, 0)

        # Create the dropdown list of operations
        self.__opSelectComboBox = QComboBox()
        self.__opSelectComboBox.addItems(MatOpGUI.OPERATIONS)
        self.__opSelectComboBox.currentIndexChanged.connect(self.__opSelectChanged)
        kwargs['grid'].addWidget(self.__opSelectComboBox, 2, 1)

        # Create the row/column entry field, for operations which return a
        # result from just a single column/row. This will be where the user
        # enters the row/column the return the result from. This will intially
        # be invisible as the default matrix operation is to multiply the two
        # together, which does not require this widget to exist. When an operation
        # is selected that will require this widget, it will be shown to the user.
        self.__opEntryField = QLineEdit()
        self.__opEntryField.setVisible(False)
        kwargs['grid'].addWidget(self.__opEntryField, 2, 2)

        # Create the Go! button
        self.__goButton = QPushButton('Go!')
        self.__goButton.clicked.connect(self.__goButtonClicked)
        kwargs['grid'].addWidget(self.__goButton, 2, 3)

        # Set the grid properties
        kwargs['grid'].setColumnStretch(1,1)

    #===========================================================================
    # Level 3: Matrix Size and Random Generation Collapsable Frames
    #===========================================================================

    # == Matrix A ==============================================================

    @frame
    def __createMatrixASizeFrame(self, *args, **kwargs):
        """
        Create a frame with a collapsable section for allowing the user to change
        the size of the matrix. This is just a text box for entering both the row
        and column and a button to change the size.
        """

        # Create a collapsable section to add the various widgets to. This will
        # make the GUI output a bit cleaner and only show this to the user if
        # they need to see it.
        self.__matrixASizeCollapsable = CollapsableSection('Matrix Size', True)

        # Create the row size entry
        self.__matrixARowSize = QLineEdit('3')
        self.__matrixARowSize.setMaximumWidth(30)
        self.__matrixARowSize.setPlaceholderText('Row')
        self.__matrixASizeCollapsable.addWidget(self.__matrixARowSize, 0, 0)

        # Create the 'X' label
        self.__matrixASizeCollapsable.addWidget(QLabel('X'), 0, 1)

        # Create the col size entry
        self.__matrixAColSize = QLineEdit('3')
        self.__matrixAColSize.setMaximumWidth(30)
        self.__matrixAColSize.setPlaceholderText('Col')
        self.__matrixASizeCollapsable.addWidget(self.__matrixAColSize, 0, 2)

        # Create the Set Size button
        self.__matrixASizeButton = QPushButton('Set Size')
        self.__matrixASizeButton.clicked.connect(self.__matrixASetSizeClicked)
        self.__matrixASizeCollapsable.addWidget(self.__matrixASizeButton, 0, 3)

        # Set the grid properties
        self.__matrixASizeCollapsable.setColumnStretch(4,1)
        kwargs['grid'].addWidget(self.__matrixASizeCollapsable, 1, 0)

    @frame
    def __createMatrixARandFrame(self, *args, **kwargs):
        """
        Create a frame with a collapsable section for allowing the user to randomly
        populate the matrix. The collapsable section has a section for defining
        the range to use and for selecting to generate either decimals or integers.
        Finally there's a button to actually generate the matrix content.
        """

        # Create a collapsable section to add the various widgets to. This will
        # make the GUI output a bit cleaner and only show this to the user if
        # they need to see it.
        self.__matrixARandCollapsable = CollapsableSection('Random Generation', True)

        # -- Create range section ----------------------------------------------

        self.__matrixARandCollapsable.addWidget(QLabel('Range:'), 0, 0)

        # Create the minimum line edit
        self.__matrixAMinRandRange = QLineEdit('0.0')
        self.__matrixAMinRandRange.setMaximumWidth(50)
        self.__matrixAMinRandRange.setPlaceholderText('min')
        self.__matrixARandCollapsable.addWidget(self.__matrixAMinRandRange, 0, 1)

        # Create the '-' label
        self.__matrixARandCollapsable.addWidget(QLabel('-', alignment = Qt.AlignCenter), 0, 2)

        # Create the maximum line edit
        self.__matrixAMaxRandRange = QLineEdit('1.0')
        self.__matrixAMaxRandRange.setMaximumWidth(50)
        self.__matrixAMaxRandRange.setPlaceholderText('max')
        self.__matrixARandCollapsable.addWidget(self.__matrixAMaxRandRange, 0, 3, 1, 2)

        # -- Create number type section ----------------------------------------

        self.__matrixARandCollapsable.addWidget(QLabel('Type:'), 1, 0)

        # Create the button group for the number type radio buttons
        self.__matrixARandButtonGroup = QButtonGroup()

        # Create the 'decimal' radio button
        decimalButton = QRadioButton('Decimal')
        decimalButton.setChecked(True)
        self.__matrixARandButtonGroup.addButton(decimalButton, 0)
        self.__matrixARandCollapsable.addWidget(decimalButton, 1, 1, 1, 3)

        # Create the 'integer' radio button
        integerButton = QRadioButton('Integer')
        self.__matrixARandButtonGroup.addButton(integerButton, 1)
        self.__matrixARandCollapsable.addWidget(integerButton, 1, 4, 1, 1)

        # -- Create generation button ------------------------------------------

        self.__matrixARandGenButton = QPushButton('Generate')
        self.__matrixARandGenButton.clicked.connect(self.__matrixARandGenClicked)
        self.__matrixARandCollapsable.addWidget(self.__matrixARandGenButton, 2, 0, 1, 5)

        # Set the grid properties
        self.__matrixARandCollapsable.setColumnStretch(5, 1)
        kwargs['grid'].addWidget(self.__matrixARandCollapsable, 3, 0)

    # == Matrix B ==============================================================

    def __createMatrixBSizeFrame(self, *args, **kwargs):
        """
        Create a frame with a collapsable section for allowing the user to change
        the size of the matrix. This is just a text box for entering both the row
        and column and a button to change the size.
        """

        # Create a collapsable section to add the various widgets to. This will
        # make the GUI output a bit cleaner and only show this to the user if
        # they need to see it.
        self.__matrixBSizeCollapsable = CollapsableSection('Matrix Size', True)

        # Create the row size entry
        self.__matrixBRowSize = QLineEdit('3')
        self.__matrixBRowSize.setMaximumWidth(30)
        self.__matrixBRowSize.setPlaceholderText('Row')
        self.__matrixBSizeCollapsable.addWidget(self.__matrixBRowSize, 0, 0)

        # Create the 'X' label
        self.__matrixBSizeCollapsable.addWidget(QLabel('X'), 0, 1)

        # Create the col size entry
        self.__matrixBColSize = QLineEdit('3')
        self.__matrixBColSize.setMaximumWidth(30)
        self.__matrixBColSize.setPlaceholderText('Col')
        self.__matrixBSizeCollapsable.addWidget(self.__matrixBColSize, 0, 2)

        # Create the Set Size button
        self.__matrixBSizeButton = QPushButton('Set Size')
        self.__matrixBSizeButton.clicked.connect(self.__matrixBSetSizeClicked)
        self.__matrixBSizeCollapsable.addWidget(self.__matrixBSizeButton, 0, 3)

        # Set the grid properties
        self.__matrixBSizeCollapsable.setColumnStretch(4,1)
        kwargs['grid'].addWidget(self.__matrixBSizeCollapsable, 1, 0)

    @frame
    def __createMatrixBRandFrame(self, *args, **kwargs):
        """
        Create a frame with a collapsable section for allowing the user to randomly
        populate the matrix. The collapsable section has a section for defining
        the range to use and for selecting to generate either decimals or integers.
        Finally there's a button to actually generate the matrix content.
        """

        # Create a collapsable section to add the various widgets to. This will
        # make the GUI output a bit cleaner and only show this to the user if
        # they need to see it.
        self.__matrixBRandCollapsable = CollapsableSection('Random Generation', True)

        # -- Create range section ----------------------------------------------

        self.__matrixBRandCollapsable.addWidget(QLabel('Range:'), 0, 0)

        # Create the minimum line edit
        self.__matrixBMinRandRange = QLineEdit('0.0')
        self.__matrixBMinRandRange.setMaximumWidth(50)
        self.__matrixBMinRandRange.setPlaceholderText('min')
        self.__matrixBRandCollapsable.addWidget(self.__matrixBMinRandRange, 0, 1)

        # Create the '-' label
        self.__matrixBRandCollapsable.addWidget(QLabel('-', alignment = Qt.AlignCenter), 0, 2)

        # Create the maximum line edit
        self.__matrixBMaxRandRange = QLineEdit('1.0')
        self.__matrixBMaxRandRange.setMaximumWidth(50)
        self.__matrixBMaxRandRange.setPlaceholderText('max')
        self.__matrixBRandCollapsable.addWidget(self.__matrixBMaxRandRange, 0, 3, 1, 2)

        # -- Create number type section ----------------------------------------

        self.__matrixBRandCollapsable.addWidget(QLabel('Type:'), 1, 0)

        # Create the button group for the number type radio buttons
        self.__matrixBRandButtonGroup = QButtonGroup()

        # Create the 'decimal' radio button
        decimalButton = QRadioButton('Decimal')
        decimalButton.setChecked(True)
        self.__matrixBRandButtonGroup.addButton(decimalButton, 0)
        self.__matrixBRandCollapsable.addWidget(decimalButton, 1, 1, 1, 3)

        # Create the 'integer' radio button
        integerButton = QRadioButton('Integer')
        self.__matrixBRandButtonGroup.addButton(integerButton, 1)
        self.__matrixBRandCollapsable.addWidget(integerButton, 1, 4, 1, 1)

        # -- Create generation button ------------------------------------------

        self.__matrixBRandGenButton = QPushButton('Generate')
        self.__matrixBRandGenButton.clicked.connect(self.__matrixBRandGenClicked)
        self.__matrixBRandCollapsable.addWidget(self.__matrixBRandGenButton, 2, 0, 1, 5)

        # Set the grid properties
        self.__matrixBRandCollapsable.setColumnStretch(5, 1)
        kwargs['grid'].addWidget(self.__matrixBRandCollapsable, 3, 0)

    #===========================================================================
    # Widget Callbacks and Events
    #===========================================================================

    def dragEnterEvent(self, event):
        """Callback for a drag enter event"""
        
        # If something was dragged into this window, set it as a move event
        event.setDropAction(Qt.MoveAction)

        # If the event has a URL to a file, check if only one file is being dropped
        # in and that file has a .matop extension. If it meets those conditions,
        # accept it, otherwise, ignore it.
        if event.mimeData().hasUrls():
            if len(event.mimeData().urls()) > 1:
                event.ignore()
            elif not event.mimeData().urls()[0].toLocalFile().endswith('.matop'):
                event.ignore()
            else:
                event.accept()
        # Ignore everything else
        else:
            event.ignore()

    def dropEvent(self, event):
        """Callback for file drop event to load a file"""
        
        for url in event.mimeData().urls():
            filename = url.toLocalFile()

        self.__load(filename)

    def __save(self):
        """Callback for saving the output data"""

        # Ask for the file to save to
        outfile, _ = QFileDialog.getSaveFileName(self, 'Select a file to save to', QDir.currentPath(), 'MatOp (*.matop)')

        # If a file was provided, grab all the text from the output text area and
        # write it to that file.
        if outfile:
            with open(outfile, 'w') as file:
                file.write(self.__outputTextBox.toPlainText())

    def __askForFileAndLoad(self):
        """Callback for loading from a file, after asking the user for the file"""

        # Ask for the file to load from
        filename, _ = QFileDialog.getOpenFileName(self, 'Select a file to load', QDir.currentPath(), 'MatOp (*.matop)')

        if filename:
            self.__load(filename)

    def __load(self, filename):
        """Callback for loading from a file, given one is provided"""

        # Load the file's content
        with open(filename, 'r') as file:
            content = file.readlines()
            content = ''.join(content)

        # Set the textbox output to the loaded content
        self.__outputTextBox.setText(content)

        # Now use regex to scan through the content and figure out the operation
        # counter, so it can be set.
        matches = re.findall('Operation (?P<counter>\d+)', content)
        self.__opCounter = max(map(int, matches)) if matches else 0

        # And finally, set the textbox output to visible
        self.__outputTextBox.setVisible(True)

    def __clearAll(self):
        """
        Callback for clearing all the input/output of the GUI. This is connected
        to the "Clear All" menu item.
        """

        # Clear the table for Matrix A. This is done by removing all rows/columns,
        # setting them to the correct amount, then redefining the widget items in
        # the table.
        rowNum = self.__matrixAInputTable.rowCount()
        colNum = self.__matrixAInputTable.columnCount()

        self.__matrixAInputTable.setRowCount(0)
        self.__matrixAInputTable.setRowCount(rowNum)

        self.__matrixAInputTable.setColumnCount(0)
        self.__matrixAInputTable.setColumnCount(colNum)

        for row in range(rowNum):
            for col in range(colNum):
                self.__matrixAInputTable.setItem(row, col, QTableWidgetItem(''))

        # Clear the table for Matrix B in the same way as Matrix A.
        rowNum = self.__matrixBInputTable.rowCount()
        colNum = self.__matrixBInputTable.columnCount()

        self.__matrixBInputTable.setRowCount(0)
        self.__matrixBInputTable.setRowCount(rowNum)

        self.__matrixBInputTable.setColumnCount(0)
        self.__matrixBInputTable.setColumnCount(colNum)

        for row in range(rowNum):
            for col in range(colNum):
                self.__matrixBInputTable.setItem(row, col, QTableWidgetItem(''))

        # Clear out the output text box and set the operation counter to zero again.
        self.__outputTextBox.setText('')
        self.__opCounter = 0

    def __opSelectChanged(self):
        """
        Callback for when the user has selected a new math operation to perform
        from the dropdown list. This exists because for some operations, the user
        needs to add a row or column to perform the operation on. The text box
        for entering this should only be displayed when it is necessary.
        """

        # Check if the new selection is in the operations that makes the entry
        # field appear. If it is, set it as visible, then set the placeholder
        # text to the appropriate text directing them to input a row or a column
        # as appropriate. Otherwise, just make the entry field invisible.
        if self.__opSelectComboBox.currentText() in MatOpGUI.OPS_TO_MAKE_ENTRY_VISIBLE:
            self.__opEntryField.setVisible(True)
            if self.__opSelectComboBox.currentText() in MatOpGUI.OPS_ON_ROW:
                self.__opEntryField.setPlaceholderText('Enter a row...')
            else:
                self.__opEntryField.setPlaceholderText('Enter a column...')
        else:
            self.__opEntryField.setVisible(False)

        # Finally, clear the entry field so they can see the placeholder text and
        # to reset the field.
        self.__opEntryField.clear()

    def __goButtonClicked(self):
        """
        Callback to execute when the Go! button is clicked to perform the mathematical
        operation. A variety of error checking is performed that may result in early
        termination of this method. In every case where the function returns early,
        it will output a messagebox to the user with a message detailing the nature
        of the problem.
        """
        
        # -- Perform Error Checking --------------------------------------------

        # If the entry field is visible for specifying the row/column for operations
        # that act only on a single row/column, make sure the user input a value
        # for it. If no value is found, then let the user know they need to input
        # one.
        if self.__opEntryField.isVisible():
            opEntryFieldText = self.__opEntryField.text()
            opRowOrCol = 'Row' if self.__opSelectComboBox.currentText() in MatOpGUI.OPS_ON_ROW else 'Column'

            # Verify the size is not an empty string
            if not opEntryFieldText:
                QMessageBox.critical(self, f'Invalid Operation {opRowOrCol}', f'{opRowOrCol} for the matrix operation is not provided.')
                return None
            
            # Verify the input is a valid number
            try:
                opEntryFieldFloat = float(opEntryFieldText)
                opEntryFieldInt = int(opEntryFieldFloat)
            except:
                QMessageBox.critical(self, f'Invalid Operation {opRowOrCol}', f'{opRowOrCol} of {opEntryFieldText} for the matrix operation is not a valid number.')
                return None

            # Make sure row input is an integer
            if opEntryFieldFloat != opEntryFieldInt:
                QMessageBox.critical(self, f'Invalid Operation {opRowOrCol}', f'{opRowOrCol} of {opEntryFieldText} for the matrix operation is not a integer.')
                return None
        
        # -- Get Matrices from Table -------------------------------------------

        # This will get the two matrices from the table operate on. If either one
        # is None, that means a valid matrix was not defined in the table and an
        # error was already shown to the user. In that case, just return.
        
        matrixA = self.__getMatrix(self.__matrixAInputTable, 'A')
        if matrixA is None: return
        
        matrixB = self.__getMatrix(self.__matrixBInputTable, 'B')
        if matrixB is None: return

        # -- Create Matrix Operation Object ------------------------------------

        # This process is not optimal as it makes a new MatrixOperation object
        # every time. A better process would be to keep a record of all previously
        # generated MatrixOperation objects and pull from that history.

        try:
            matop = MatrixOperation(self.__nameLineEdit.text(), matrixA, matrixB)
        except MatrixOperationError as e:
            QMessageBox.critical(self, 'Invalid Matrices', str(e))
            return

        # -- Perform Additional Error Checking ---------------------------------

        # Now that the matrices are found, one more error check can be performed,
        # which is to verify that the row/column provided for the operation is
        # within range, based on the matrix sizes. Of course, only check this if
        # it is necessary.
        if self.__opEntryField.isVisible():
            if  self.__opSelectComboBox.currentText() in MatOpGUI.OPS_ON_ROW:
                upperOpLimit = matop.productRows
            else:
                upperOpLimit = matop.productCols
                
            if opEntryFieldInt < 1 or upperOpLimit < opEntryFieldInt:
                QMessageBox.critical(self, f'Invalid Operation {opRowOrCol}', f'{opRowOrCol} {opEntryFieldText} for the matrix is out of bounds [1,{upperOpLimit}].')
                return None

        # -- Get Matrix Operation Result ---------------------------------------

        # Call the right function based on the user's requested operation
        if self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[0]:
            result = matop.product
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[1]:
            result = matop.getProductColSum(opEntryFieldInt - 1)
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[2]:
            result = matop.getProductColProd(opEntryFieldInt - 1)
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[3]:
            result = matop.getProductColCumSum()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[4]:
            result = matop.getProductColCumProd()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[5]:
            result = matop.getProductRowSum(opEntryFieldInt - 1)
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[6]:
            result = matop.getProductRowProd(opEntryFieldInt - 1)
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[7]:
            result = matop.getProductRowCumSum()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[8]:
            result = matop.getProductRowCumProd()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[9]:
            result = matop.getProductTotalMin()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[10]:
            result = matop.getProductTotalMax()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[11]:
            result = matop.getProductTotalMean()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[12]:
            result = matop.getProductTotalMedian()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[13]:
            result = matop.getProductTotalSum()
        elif self.__opSelectComboBox.currentText() == MatOpGUI.OPERATIONS[14]:
            result = matop.getProductTotalProd()
        else:
            # If this point is reached, somehow the text of the combo box doesn't
            # match any text added to it. This point should never be reached, but
            # if it is, present an error to the user. This should not be the user's
            # fault and there would be nothing they could do to fix it, but better
            # to provide some sort of feedback to the user about the issue.
            QMessageBox.critical(self, 'Invalid Operation Selection', 'Invalid Operation Selection: '+self.__opSelectComboBox.currentText())
            return

        # -- Print Output ------------------------------------------------------

        # Make the output text area visible if it is not
        self.__outputTextBox.setVisible(True)

        # Increment the operation counter
        self.__opCounter += 1

        # Construct and print the header for the operation
        header = '\n\n' if self.__opCounter > 1 else ''
        header += '=' * 80 + '\n'
        header += f'=  Operation {self.__opCounter}'
        if self.__nameLineEdit.text():
            header += ': ' + self.__nameLineEdit.text() + ' '
        header += '\n'
        header += '=' * 80 + '\n'
        self.__outputTextBox.append(header)

        # Output the matrices being multiplied
        self.__outputTextBox.append('Matrix A:\n')
        self.__outputTextBox.append(str(matrixA) + '\n')
        self.__outputTextBox.append('Matrix B:\n')
        self.__outputTextBox.append(str(matrixB) + '\n')

        # Output the operation result
        self.__outputTextBox.append(self.__opSelectComboBox.currentText() + ' Result:\n')
        self.__outputTextBox.append(str(result))

    # == Matrix A ==============================================================

    def __matrixASetSizeClicked(self):
        """
        Callback for when the set size button is clicked to change the size input
        for matrix A. This will update the QTableWidget's rows and columns to be
        the appropriate size based on the user's inputs. Some error checking is
        performed to ensure the user's inputs are valid. If a problem is found,
        this will return early with a messagebox indicating the nature of the issue.
        """

        # TODO: save/restore the values already entered so they don't get erased
        # when the size changes.

        # -- Perform Error Checking --------------------------------------------

        # Validate the provided row. If it's invalid, return
        rowNum = self.__validateSize(self.__matrixARowSize, 'A', 'Row')
        if rowNum is None: return
        
        # Set the text to the returned value, which should guarantee the input
        # always looks like an integer.
        self.__matrixARowSize.setText(str(rowNum))

        # Validate the provided column. If it's invalid, return
        colNum = self.__validateSize(self.__matrixAColSize, 'A', 'Col')
        if colNum is None: return
        
        # Set the text to the returned value, which should guarantee the input
        # always looks like an integer.
        self.__matrixAColSize.setText(str(colNum))

        # -- Update matrix size ------------------------------------------------

        self.__matrixAInputTable.setRowCount(0)
        self.__matrixAInputTable.setRowCount(rowNum)

        self.__matrixAInputTable.setColumnCount(0)
        self.__matrixAInputTable.setColumnCount(colNum)

        for row in range(rowNum):
            for col in range(colNum):
                self.__matrixAInputTable.setItem(row, col, QTableWidgetItem(''))

    def __matrixARandGenClicked(self):
        """
        Callback for when the generate button is clicked to generate a random
        matrix for matrix A. After some basic error checking, this just generates
        a random matrix, based on the inputs provided by the user (such as whether
        to generate decimals or integers, and what range to use.

        If an error is found, such as an invalid range value input by the user,
        a messagebox will be displayed with information about the issue and
        the function will return.
        """

        # -- Perform Error Checking --------------------------------------------

        # Validate the minimum range value
        minRangeLimit = self.__validateRange(
            self.__matrixAMinRandRange, 'A', 'Min', self.__matrixARandButtonGroup.checkedId() == 1
        )
        if minRangeLimit is None: return

        # Set the text to the returned value.
        self.__matrixAMinRandRange.setText(str(minRangeLimit))

        # Validate the maximum range value
        maxRangeLimit = self.__validateRange(
            self.__matrixAMaxRandRange, 'A', 'Max', self.__matrixARandButtonGroup.checkedId() == 1
        )
        if maxRangeLimit is None: return

        # Set the text to the returned value.
        self.__matrixAMaxRandRange.setText(str(maxRangeLimit))

        # -- Populate the matrix with random values ----------------------------

        # Get the matrix size
        rowNum = self.__matrixAInputTable.rowCount()
        colNum = self.__matrixAInputTable.columnCount()

        # Generate the matrix
        if self.__matrixARandButtonGroup.checkedId() == 0: # Decimal
            matrix = (np.random.rand(rowNum, colNum) * (maxRangeLimit - minRangeLimit)) + minRangeLimit
        else: # Integer
            matrix = np.random.randint(minRangeLimit, maxRangeLimit, size = (rowNum, colNum))

        # Finally, populate the table with the generated matrix
        self.__setMatrix(self.__matrixAInputTable, matrix)

    # == Matrix B ==============================================================

    def __matrixBSetSizeClicked(self):
        """
        Callback for when the set size button is clicked to change the size input
        for matrix A. This will update the QTableWidget's rows and columns to be
        the appropriate size based on the user's inputs. Some error checking is
        performed to ensure the user's inputs are valid. If a problem is found,
        this will return early with a messagebox indicating the nature of the issue.
        """

        # TODO: save/restore the values already entered so they don't get erased
        # when the size changes.

        # -- Perform Error Checking --------------------------------------------

        # Validate the provided row. If it's invalid, return
        rowNum = self.__validateSize(self.__matrixBRowSize, 'B', 'Row')
        if rowNum is None: return
        
        # Set the text to the returned value, which should guarantee the input
        # always looks like an integer.
        self.__matrixBRowSize.setText(str(rowNum))

        # Validate the provided column. If it's invalid, return
        colNum = self.__validateSize(self.__matrixBColSize, 'B', 'Col')
        if colNum is None: return
        
        # Set the text to the returned value, which should guarantee the input
        # always looks like an integer.
        self.__matrixBColSize.setText(str(colNum))

        # -- Update matrix size ------------------------------------------------

        self.__matrixBInputTable.setRowCount(0)
        self.__matrixBInputTable.setRowCount(rowNum)

        self.__matrixBInputTable.setColumnCount(0)
        self.__matrixBInputTable.setColumnCount(colNum)

        for row in range(rowNum):
            for col in range(colNum):
                self.__matrixBInputTable.setItem(row, col, QTableWidgetItem(''))

    def __matrixBRandGenClicked(self):
        """
        Callback for when the generate button is clicked to generate a random
        matrix for matrix A. After some basic error checking, this just generates
        a random matrix, based on the inputs provided by the user (such as whether
        to generate decimals or integers, and what range to use.

        If an error is found, such as an invalid range value input by the user,
        a messagebox will be displayed with information about the issue and
        the function will return.
        """

        # -- Perform Error Checking --------------------------------------------

        # Validate the minimum range value
        minRangeLimit = self.__validateRange(
            self.__matrixBMinRandRange, 'B', 'Min', self.__matrixBRandButtonGroup.checkedId() == 1
        )
        if minRangeLimit is None: return

        # Set the text to the returned value.
        self.__matrixBMinRandRange.setText(str(minRangeLimit))

        # Validate the maximum range value
        maxRangeLimit = self.__validateRange(
            self.__matrixBMaxRandRange, 'B', 'Max', self.__matrixBRandButtonGroup.checkedId() == 1
        )
        if maxRangeLimit is None: return

        # Set the text to the returned value.
        self.__matrixBMaxRandRange.setText(str(maxRangeLimit))

        # -- Populate the matrix with random values ----------------------------

        # Get the matrix size
        rowNum = self.__matrixBInputTable.rowCount()
        colNum = self.__matrixBInputTable.columnCount()

        # Generate the matrix
        if self.__matrixBRandButtonGroup.checkedId() == 0: # Decimal
            matrix = (np.random.rand(rowNum, colNum) * (maxRangeLimit - minRangeLimit)) + minRangeLimit
        else: # Integer
            matrix = np.random.randint(minRangeLimit, maxRangeLimit, size = (rowNum, colNum))

        # Finally, populate the table with the generated matrix
        self.__setMatrix(self.__matrixBInputTable, matrix)

    #===========================================================================
    # Utilities
    #===========================================================================

    def __setMatrix(self, table, matrix):
        """
        Set the QTableWidget cells with the content from a numpy matrix. Note
        that the table and matrix should have the same dimensions.

        Input:
            table: A QTableWidget object to set the cell values of.
            matrix: A numpy array which has values to store in the table.
        """
        
        # No error checking is performed here to confirm that the table and matrix
        # have the correct size. Since this is an internal function, it is assumed
        # the calling functions are already making sure this isn't an issue.
        # In addition, if an issue were found, there'd be no easy way to handle it
        # as it wouldn't be the user's fault.

        for row in range(np.shape(matrix)[0]):
            for col in range(np.shape(matrix)[1]):
                # Get the item at the current row/column of the table and set the
                # text to the value in the matrix.
                item = table.item(row, col)
                item.setText(str(matrix[row,col]))

    def __getMatrix(self, table, matrixName):
        """
        Extract a numpy array from a QTableWidget. The output array will have the
        same size as the table. If the table does not have a valid value in it, a
        messagebox will be shown to the user with information about the problem and
        the method will return early with None.

        Input:
            table: The QTableWidget object to pull data from for constructing the
                numpy array.
            matrixName: A string, either 'A' or 'B'. Used to populate the error
                message displayed to the user in the event of an issue.

        Output:
            Returns a numpy array of the same dimensions as the table and with values
            from the table. The values are set as floats by default. If the table
            has invalid entries (either because it's empty or not a float), None
            will be returned.
        """
        
        # Extract the row and column number of the table
        rowNum = table.rowCount()
        colNum = table.columnCount()

        # Create a matrix to return, initially all zeros. Make it all floating type.
        result = np.zeros((rowNum, colNum), dtype = np.float)
        
        for row in range(rowNum):
            for col in range(colNum):
                value = table.item(row, col).text()

                # Verify the value is not an empty string
                if not value:
                    row += 1
                    col += 1
                    QMessageBox.critical(self, 'Invalid Matrix Entry', f'Value for cell ({row}, {col}) of matrix {matrixName} is not provided.')
                    return None

                # Verify the input is a valid number
                try:
                    num = float(value)
                except:
                    row += 1
                    col += 1
                    QMessageBox.critical(self, 'Invalid Matrix Entry', f'Value of {value} for cell ({row}, {col}) of matrix {matrixName} is not a valid number.')
                    return None

                # If no issues, store the number in the matrix
                result[row,col] = num

        return result

    def __validateSize(self, lineEdit, matrix, direction):
        """
        Utility function for verifying the size provided by the user in a text box

        Input:
            lineEdit: The QLineEdit object that has data in it about the size to
                extract.
            matrix: A string, either 'A' or 'B'. Used to populate the error
                message displayed to the user in the event of an issue.
            direction: A string, either 'Row' or 'Column'. Used to populate the
                error message displayed to the user in the event of an issue.

        Output:
            Returns the size pulled from the QLineEdit widget as an integer. If
            an error is found (e.g., nothing was provided or the input was not
            an int), then None is returned and a messagebox is presented to the
            user with information about the nature of the issue.
        """
        
        # Pull out the size from the line edit field
        sizeNum = lineEdit.text()

        # Verify the size is not an empty string
        if not sizeNum:
            QMessageBox.critical(self, f'Invalid {direction} Size', f'{direction} size for matrix {matrix} is not provided.')
            return None
        
        # Verify the input is a valid number
        try:
            sizeNumFloat = float(sizeNum)
            sizeNumInt = int(sizeNumFloat)
        except:
            QMessageBox.critical(self, f'Invalid {direction} Size', f'{direction} size of {sizeNum} for matrix {matrix} is not a valid number.')
            return None

        # Make sure row input is an integer
        if sizeNumFloat != sizeNumInt:
            QMessageBox.critical(self, f'Invalid {direction} Size', f'{direction} size of {sizeNum} for matrix {matrix} is not a integer.')
            return None

        # Make sure row input is in valid range
        if sizeNumInt < 1 or 10 < sizeNumInt:
            QMessageBox.critical(self, f'Invalid {direction} Size', f'{direction} size of {sizeNum} for matrix {matrix} is outside valid range of [1,10].')
            return None

        return sizeNumInt

    def __validateRange(self, lineEdit, matrix, end, isInt):
        """
        Utility function for verifying the range provided by the user in a text box

        Input:
            lineEdit: The QLineEdit object that has data in it about the range to
                extract.
            matrix: A string, either 'A' or 'B'. Used to populate the error
                message displayed to the user in the event of an issue.
            end: A string, either 'Row' or 'Column'. Used to populate the
                error message displayed to the user in the event of an issue.
            isInt: A boolean indicating if the output is supposed to be an integer
                or a decimal.

        Output:
            Returns the range pulled from the QLineEdit widget as an integer, or
            float. If an error is found (e.g., nothing was provided or the input
            was not an int as requested), then None is returned and a messagebox
            is presented to the user with information about the nature of the issue.
        """
        
        # Pull out the range from the line edit field
        rangeLimit = lineEdit.text()

        # Verify the limit is not an empty string
        if not rangeLimit:
            QMessageBox.critical(self, f'Invalid {end} Range', f'{end} range limit for matrix {matrix} is not provided.')
            return None

        try:
            rangeLimitFloat = float(rangeLimit)
            rangeLimitInt = int(rangeLimitFloat)
        except:
            QMessageBox.critical(self, 'Invalid {end} Range', f'{end} range limit of {rangeLimit} for matrix {matrix} is not a valid number.')
            return None

        # Make sure the range value is an integer, if it's supposed to be
        if isInt and rangeLimitInt != rangeLimitFloat:
            QMessageBox.critical(self, 'Invalid {end} Range', f'{end} range limit of {rangeLimit} for matrix {matrix} is not an integer, but integer was selected.')
            return None

        return rangeLimitInt if isInt else rangeLimitFloat
