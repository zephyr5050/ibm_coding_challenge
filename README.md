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
    * [Code Design](#code-design)
    * [File Breakdown](#file-breakdown)
    * [GUI Layout](#gui-layout)

## Overview

This project creates a GUI that presents the users with the ability to enter two matrices, calculate statistics related to the input, and see the result.

### File Overview

This project provides several files which are breifly described below.

* `mat_main.py` - The entry point to the program. It should be executed directly from the file or from the command line via the command `python mat_main.py`. This will launch the main GUI for the user to interact with.
* `mat_gui.py` - The main file used to generate the GUI. This file provides a class that subclasses the PyQt `QMainWindow` class. It constructs the GUI, provides callbacks for interaction events and is the main point of interaction for the user.
* `mat_widgets.py` - An ancillary file that provides additional widgets that are used within `mat_gui.py`. These are broken out as a logical group of classes and functions that are separate from the main GUI.
* `mat_operation.py` - Provides a `MatrixOperation` class which abstracts the matrix operations and statistics calculations away from the GUI.
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

This program is developed for Python 3.6.10. The following python modules, not included in the standard library, are used:

* PyQt5
* numpy (v1.18.1)

## Design

This section gives an overview of the design of the program and why it was created the way it was. This starts by explaining how the coding challenge was interpreted, and goes on to explain design choices for specific components of the project.

### Interpretation

From reading through the coding challenge, the points below detail the interpretation of the challenge, and with more work, would be the basis for forming a set of requirements for the program.

1. The challenge asks for the ability to enter two matrices (I chose to limit to 10x10, just so they didn't get too unwieldy) and calculate statistics on them. All statistics requested were either the product of the two matrices, or else a statistic of the product of the two matrices. For that reason, the product of the matrices always has to be calculated, no matter what the use requests (and thus the user's input must always be able to be multiplied).
2. The challenge asks to only present the statistics that the user requests. Since the product must always be calculated, no matter the statistic, that is calculated first, but the other statistics are calculated on the fly.
3. The challenge requests that user's be able to give a name to a "run" in the statistics. The concept of a "run" was not defined, but it was interpretted to mean a single instance of a user entering two matrices and choosing a single statistic to calculate for them. If the user wants to calculate multiple statistics on the same matrices, that would count as a new "run" where they could enter a new name and receive a new output.
4. The challenge requests that the user be able to observe the statistics in a useful way. A text box was chosen to output to and each "run" outputs a header (optionally with the user's run name), the two matrices used in the operation, and the result of the statistic (along with the name of what the statistic is). In this way the user sees all the inputs and outputs of the operation. The textbox allows the user to easily copy any information, e.g., if they want to use the result elsewhere. The inputs are provided so the user could, in theory, reproduce the statistic themselves and verify it. If the the operation is on the product of the matrices, the intermediary result of calculating that product is not provided to the user, primarily because they did no request it.

### Code Design

#### Coding Style

In general, the coding style intends to conform to commonly accepted python coding styles outlined in [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/). Compliance is not guarateed, and with more time/effort the program could have been run through a PEP 8 linter and issues addressed. Even more important than a coding style is internal consistency. This program aims for consistency in filenames, class naming, formatting, etc.

#### Design Choices

A variety of design choices were made when creating this program, which are detailed below.

1. Class functions and variables which are intended to be "private" are preceded by a double underscore (`__`). Python has no true private concept, but these variables will be name mangled to a degree, making them less accessible to the user.
2. Within the `MatrixOperation` class, the `__getProductStatistic` function was created which is the sole function for calculating statistics on the product matrix. The pulicly available API provides an individual function per statistic, but each of them simply passes a function handle for the statistic to calculate to this function. This allows for a single location for error checking on the inputs so code is not reproduced for each function which calculates and returns a single statistic.
3. Various values such as the input matrices and product matrix are exposed to the user as properties of the `MatrixOperation` class. In this way, they can access the values safely, without being able to modify them directly. Other, simple calculations such as the shape of the product are also returned this way as they are simple to calculate and return.
4. The `mat_gui.py` file performs the construction of the GUI. It tries to partition the construction into meaningful chunks in a hierarchical way such that no individual function that is part of the contruction is unweildy. The longer a function is, the more prone to errors it is and it is harder to review. For the most part, the functions are broken down into creating individual frames which have GUI elements in them (including sub-frames). Since each frame requires a grid and handling of frame/grid properties, this work has been abstracted to a decorator, `@frame`. This decorator handles things like assigning grids and setting frame/grid properties and the functions themselves simply have to handle placing widgets in the frame. The grid to hold the widgets is passed into the decorated functions as a keyword argument.
5. The core of the program is broken up between `mat_main.py`, `mat_gui.py` and `mat_operations.py`. The program was chosen to be broken this way as each file handles a logical component of the program. The first, `mat_main.py`, simply handles the entry point to the program. This should do little to no heavy lifting as the user just wants to execute this file. The second, `mat_gui.py` handles the heavy lifing to creating the GUI and defining the responses when the user interacts with it. Finally, the `mat_operations.py` file was created to abstract the actual statistic calculation process away from the GUI. In this way, future developers could go in and expand one or the other separately without needing to know how the other worked (they of course would need to be cognizent of the interface between the two).
6. The GUI uses collapsable frames. This was chosen to try and make the input process more intuitive. If the user sees too many buttons and entry fields, they may get confused about what to enter where and how to do it. The collapsable frames allows the user to see the important elements first, and if they decide they want to view what is collapsed, they can expand and explore that element. Tooltips are provided to help guide the user's process.
7. The output of the statistics is as raw monospaced text. A text box was chosen so the result could be easily copied and used elsewhere (as opposed to another table or GUI element that would make copying the result a challenge). The output is monospaced so the output lines up nicely and is easier to compare one line against another. The output text box was set so users could highlight and copy, but not modify, so the output cannot become corrupted/invalid.
8. The statistics history is kept in the form of text output. Neither the GUI, nor the MatrixOperations class has a form of saving the history other than the text output. This means that if the user provides the same matrix again, an identical MatrixOperations object is created, despite one having been previously created with the same inputs. A more robust process would be to implement a history class that maintains all the information from past operations and can be referenced if the user provides the same inputs.

The above provides a description of design choices for variouls elements of the program. Additional design choices for smaller pieces are commented in the relevent areas of code.

### File Breakdown

This project is requires only a handlful of files. As such, everything has been included in a flat directory structure. If this project were to grow, it would require creating a better structure. A logical way to break this up would be to create a folder for the front end (i.e., all the GUI related components), a folder for the back end (i.e., all the underlying programs that perform the heavy lifting) and a test folder for containing unit tests. The project could be further sub-divided as necessary. The `mat_main.py` would remain at the highest level. This more complicated structure would benefit from defining `__init__.py` files to make make importing easier between files.

### GUI Layout

The design of the GUI was set up to try and be a natural flow, based on the order of operations the user would perform. At a high level, the main GUI screen is broken into four regions.

1. An area to enter the name of the run.
2. An area to enter the matrices.
3. An area to choose the statistic to calculate.
4. An area to view the result.

These areas are laid out top to bottom with the idea that the user will logically start at the top and work their way down. The area where the user enters the matrices is broken into two side-by-side frames to show their equal importance. They are labeled Matrix A and Matrix B so the user gets the sense that there is an order of operations in which matrix is first and which is second.

Within the matrix input frames, are two collapsable frames which are initially collapsed. The idea here is to not overwhelm the user with options and choices. Hide initially unnecessary elements and let them delve into what they might need. Again, the frame is laid out from top to bottom in the order in which the user might interact with it. At the top is a collapsable frame for setting the matrix size. Once the user has set the appropriate size, they can enter the values into the matrix themselves, or, below the matrix entry area, is another collapsable frame that allows them to randomly generate values.

Initially the output text area with the results of the matrix operations is not shown. It is only shown if an operation has been performed, or loaded from a file. This is to avoid confusion in the user with what to do with a blank text area.
