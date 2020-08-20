# IBM Coding Challenge

This repository contains the response to the IBM Coding Challenge. The stated goal of the challenge is to develop a Python program which can accept two matrices as input and output requested mathematical operations to the user. See the TBD file for full details on the constraints and requirements of the coding challenge.

## Table of Contents

* [Overview](#overview)
    * [File Overview](#file-overview)
    * [Usage Overview](#usage-overview)
* [Execution](#execution)
    * [Requirements](#requirements)
* [Design](#design)
    * [Interpretation](#interpretation)
    * [File Breakdown](#file-breakdown)

## Overview

This project creates a GUI that presents the users with the ability to enter two matrices, calculate statistics related to the input, and see the result.

### File Overview

This project provides several files which are breifly described below.

* `mat_main.py` - The entry point to the program. It should be executed directly from the file or from the command line via the command `python mat_main.py`. This will launch the main GUI for the user to interact with.
* `mat_gui.py` - The main file used to generate the GUI. This file provides a class that subclasses the PyQt `QMainWindow` class. It constructs the GUI, provides callbacks for interaction events and is the main point of interaction for the user.
* `mat_widgets.py` - An ancillary file that provides additional widgets that are used within `mat_gui.py`. These are broken out as a logical group of classes and functions that are separate from the main GUI.
* `mat_operation.py` - Provides a `MatrixOperation` class which abstracts the matrix operations away from the GUI.
* `mat_unit_test.py` - Provides unit tests for the `mat_operation.py` file.
* `example_savefile.matop` - An example save file from a a usage of this program that can be loaded by the user.
* `gui_image.png` - An image of the GUI, for reference.

Additionally, there is an `imgs` folder which has several image files used in the GUI. Users do not need to interact with these files in any way.

### Usage Overview

The image below shows the GUI created by this program, with all the elements on display.

![Image of GUI](/gui_image.png?raw=true "Image of GUI")

The following provides a general overview of how to use this GUI.

1. Optionally, choose to enter a name for the run. This will be included in the output.
2. Starting with Matrix A, ensure it is the desired size. Enter the size in the "Matrix Size" section, as a row length and column length. Hit the set size button. Note that this will clear the matrix of its content. The size is limited to be less than 10x10.
3. Either enter the matrix values, or else choose to randomly populate the matrix with values. If the user decides to randomly generate values for the matrix, a range must be given and the user can choose between randomly choosing decimal values or integer values.
4. Perform the same actions for Matrix B.
5. Below the two matrices, select, from the dropdown list, a statistic to calculate. The "Multiply" option simply multiplies matrix A and B together (in that specific order). All the other statistics provided are on the matrix that is the product of A and B. Some statistics are on only a single row/column of the product matrix and the user must enter a value. Hit the Go! button to calcualte the requested statistic.
6. The output field at the bottom shows the information for the specific run, including the name of the run, if provided, the input matrices, and the result of the statistic.

Aside from the above actions, users can perform the following actions.

* Load a file, either by going to **File** &rarr; **Load**, using the keyboard shortcut <kbd>Ctrl</kbd> + <kbd>L</kbd>, or dragging a file into the window. Only `.matop` files can be loaded.
* Save a file, either by going to **File** &rarr; **Save** or using the keyboard shortcut <kbd>Ctrl</kbd> + <kbd>S</kbd>. The output file will be of the `.matop` type.
* Clear the entire GUI of content, either by going to **Options** &rarr; **Clear All** or using the keyboard shortcut <kbd>Ctrl</kbd> + <kbd>A</kbd>.
* Quit the GUI, either by going to **Options** &rarr; **Quit**, using the keyboard shortcut <kbd>Ctrl</kbd> + <kbd>Q</kbd>, or just exiting out of the window.

## Execution

Execute the program by executing `mat_gui.py` directly or else running from the command line via the command `python mat_gui.py`.

The unit test can be executed separately from everything else by executing `mat_unit_test.py` directly or else running from the command line via the command `mat_unit_test.py`.

### Requirements

This program is developed for Python 3.6.10. The following python modules are used:

* PyQt5
* numpy (v1.18.1+)
* re (v2.2.1+)
* unittest

## Design

This section gives an overview of the design of the program and why it was created the way it was. This starts by explaining how the coding challenge was interpretted, and goes on to explain design choices for specific components of the project.

### Interpretation



### File Breakdown

This project is requires only a handlful of files. As such, everything has been included in a flat directory structure. If this project were to grow, it would require creating a better structure. A logical way to break this up would be to create a folder for the front end (i.e., all the GUI related components), a folder for the back end (i.e., all the underlying programs that perform the heavy lifting) and a test folder for containing unit tests. The `mat_main.py` would remain at the highest level. This more complicated structure would benefit from defining `__init__.py` files to make make importing easier between files.
