#============================== IBM Code Challenge =============================
# mat_operation.py
#
# Provides a class that performs matrix operations.
#
# Description:
#     A MatrixOperation class is provided which accepts two matrices and a name.
#     It calculates the product of the two matrices, assuming that is valid, and
#     then provides an API to the user so they can access a variety of other
#     useful statistics on the product, such as the cumulative product along
#     the rows.
#
#     A MatrixOperationError class is also provided so that the MatrixOperation
#     class can throw errors specific to it.
#
#===============================================================================

import numpy as np

class MatrixOperation(object):
    """
    Provides a class for inputting two matrices and calculating statistics on
    the product of those two matrices. The algorithms used here to calculate the
    statistics are optimal as this class uses the numpy algorithms. The statistics
    are calculated on the fly which can be efficient if they're not all needed,
    but can be taxing if they have to be repeated generated.
    """

    ROW = 0
    COL = 1

    def __init__(self, name, matrixA, matrixB):
        """
        Initialization function for a MatrixOperation object.

        Input:
            name: A name for the operation, as a string.
            matrixA: The first matrix, as a numpy array, to use in the multiplication.
            matrixB: The second matrix, as a numpy array, to use in the multiplication.
        """

        # Define a validity flag indicating whether this object successfully
        # instantiated.
        self.__valid = False

        # -- Input Validation --------------------------------------------------

        # Verify the two matrices have the necessary properties
        self.__verifyMatrixProperties(matrixA, 'first')
        self.__verifyMatrixProperties(matrixB, 'second')

        # Verify that the matrices can be multiplied, i.e., the number of columns
        # in the first matrix is equal to the number of rows in the second matrix.
        matrixACol = np.shape(matrixA)[1]
        matrixBRow = np.shape(matrixB)[0]
        if matrixACol != matrixBRow:
            errmsg = ('Invalid matrix sizes to allow for multiplication. First '
                      f' matrix columns ({matrixACol}) does not match second '
                      f' matrix rows ({matrixBRow}).')
            raise MatrixOperationError(errmsg)

        # -- Create Class Variables --------------------------------------------

        # Define user provided values
        self.__name    = name
        self.__matrixA = matrixA
        self.__matrixB = matrixB

        # Define the product of matrix A and matrix B. This is performed by the
        # constructor since all subsequent operations the user may request relies
        # on this result. And since this is easily the most intenstive statistic
        # the user may request, it's better to do it once.
        self.__product = np.matmul(matrixA, matrixB)

        # Everything was successful up to here, so mark the object as valid
        self.__valid = True

    def __verifyMatrixProperties(self, matrix, order):
        """
        Verifies the matrices input to the constructor are valid. Namely that
        they have the correct dimension and are of the correct size.

        Input:
            matrix: A matrix, as a numpy array. It should be 2D and no greater
                than 10x10.
            order: A string, indicating whether this is the first (matrix A)
                or the second (matrix B) matrix. Used for error outputs.

        Raises:
            MatrixOperationError: Raises in the event that the input matrix is
                not 2D, is empty, or is greater than 10x10.
        """
        
        # Get the shape and number of dimentions of the matrix
        shape = np.shape(matrix)
        size = np.size(matrix)
        dims = len(shape)
        
        # Verify that the matrix has two dimensions
        if dims != 2:
            errmsg = (f'Invalid number of dimensions ({dims}) of {order} matrix. '
                      'Must be exactly 2.')
            raise MatrixOperationError(errmsg)

        # Verify that the matrix is not empty
        if size == 0:
            errmsg = f'Input for {order} matrix is empty.'
            raise MatrixOperationError(errmsg)

        # Verify that the matrix does not have a dimension greater than 10
        for i, dim in enumerate(shape):
            if dim > 10:
                errmsg = (f'Invalid dimension size of {dim} for dimension {i} '
                          f'of {order} matrix. Must be <= 10.')
                raise MatrixOperationError(errmsg)

    #===========================================================================
    # Functions for Statistics on Column of Product Matrix
    #===========================================================================
    
    def getProductColSum(self, colNum):
        return self.__getProductStatistic(np.sum, MatrixOperation.COL, colNum)

    def getProductColProd(self, colNum):
        return self.__getProductStatistic(np.prod, MatrixOperation.COL, colNum)

    def getProductColCumSum(self):
        return self.__getProductStatistic(np.cumsum, MatrixOperation.COL)

    def getProductColCumProd(self):
        return self.__getProductStatistic(np.cumprod, MatrixOperation.COL)

    #===========================================================================
    # Functions for Statistics on Row of Product Matrix
    #===========================================================================

    def getProductRowSum(self, rowNum):
        return self.__getProductStatistic(np.sum, MatrixOperation.ROW, rowNum)

    def getProductRowProd(self, rowNum):
        return self.__getProductStatistic(np.prod, MatrixOperation.ROW, rowNum)

    def getProductRowCumSum(self):
        return self.__getProductStatistic(np.cumsum, MatrixOperation.ROW)

    def getProductRowCumProd(self):
        return self.__getProductStatistic(np.cumprod, MatrixOperation.ROW)    

    #===========================================================================
    # Functions for Statistics on Total Product Matrix
    #===========================================================================

    def getProductTotalSum(self):
        return self.__getProductStatistic(np.sum)

    def getProductTotalProd(self):
        return self.__getProductStatistic(np.prod)

    def getProductTotalMean(self):
        return self.__getProductStatistic(np.mean)

    def getProductTotalMedian(self):
        return self.__getProductStatistic(np.median)

    def getProductTotalMin(self):
        return self.__getProductStatistic(np.min)

    def getProductTotalMax(self):
        return self.__getProductStatistic(np.max)

    #===========================================================================
    # Utility Functions
    #===========================================================================
    
    def __getProductStatistic(self, statFunc, direction = None, index = None):
        """
        Main function for calculating the requested statistic of the product of
        the two matrices input on construction. The user provides a function handle
        and additional parameters to aid in the calculation.

        Input:
            statFunc: Function handle of the statistic to calculate on the product
                matrix.
            direction: If the statistic is calcualted along a particular axis
                (either rows or columns), specify this here. Should be either the
                ROW or COL value, if it is not None. Defaults to None.
            index: If the statistic is meant to return a specific row/column, this
                specifies the row/column to return. Only has use if direction is
                specified (i.e., not None). Defaults to None.

        Raises:
            MatrixOperationError: Raised if the provided index is out of bounds.
        """

        matrix = self.product
        axis   = None

        # Determine if the statistic is to be calculated along a particular row
        # or column, or else on the entire matrix. If a direction is provided,
        # use the index to get the column/row to calculate the statistic on, but
        # first make sure the index is in range. If a direction is not provided
        # set the entire product matrix as the thing to calculate the statistic
        # on.
        if direction == MatrixOperation.COL:
            if index is not None:
                # Verify that the index provided is not greater than the number
                # of columns. If it is, throw an error.
                if index < 0 or self.productCols <= index:
                    errmsg = (f'Column number ({index}) is out of bounds of product '
                              f'matrix. Must be in [0,{self.productCols}).')
                    raise MatrixOperationError(errmsg)

                # Set the matrix to calculate the statistic on
                matrix = self.product[:, index]
            else:
                axis = 0

        elif direction == MatrixOperation.ROW:
            if index is not None:
                # Verify that the index provided is not greater than the number
                # of rows. If it is, throw an error.
                if index < 0 or self.productRows <= index:
                    errmsg = (f'Row number ({index}) is out of bounds of product '
                              f'matrix. Must be in [0,{self.productRows}).')
                    raise MatrixOperationError(errmsg)

                # Set the matrix to calculate the statistic on
                matrix = self.product[index, :]
            else:
                axis = 1

        # Calcualte the statistic of the matrix using the provided statistic
        # function, and along the specified axis.
        statistic = statFunc(matrix, axis = axis)

        return statistic

    #===========================================================================
    # Properties
    #===========================================================================

    @property
    def valid(self):
        return self.__valid

    @property
    def name(self):
        return self.__name

    @property
    def matrixA(self):
        return self.__matrixA

    @property
    def matrixB(self):
        return self.__matrixB

    @property
    def product(self):
        return self.__product

    @property
    def productShape(self):
        return np.shape(self.__product)

    @property
    def productRows(self):
        return self.productShape[0]

    @property
    def productCols(self):
        return self.productShape[1]

class MatrixOperationError(Exception):
    """
    A simple Error class used to throw errors for the MatrixOperation class
    """
    pass
