#============================== IBM Code Challenge =============================
# mat_unit_test.py
#
# Performs unit tests on the classes and functions within this repository.
#
# Description:
#     This process uses the builtin unittest module to perform simple unit tests
#     of the MatrixOperation class. It should be executed as a separate script.
#
#===============================================================================

import unittest
import numpy as np

from mat_operation import *

class TestMatOp(unittest.TestCase):    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define various matrices that can be used in constructing a
        # MatrixOperation object.

        # Create two nominal matrices that can multiply together
        self.matrix_1 = np.array([[1, 2, 3],
                                  [4, 5, 6],
                                  [7, 8, 9]], dtype = np.int64)
        self.matrix_2 = np.array([[0,  9],
                                  [8, -8],
                                  [3,  6]], dtype = np.int64)

        # Create a matrix which can't be multiplied with matrix_1
        self.matrix_3 = np.array([[1, 1],
                                  [4, 5]], dtype = np.int64)

        # Create a 3D matrix
        self.matrix_4 = np.array([[[1,2],[3,4]],
                                  [[5,6],[7,8]]], dtype = np.int64)

        # Create an empty matrix
        self.matrix_5 = np.array([[]])

        # Create a matrix that is larger than 10x10
        self.matrix_6 = np.zeros((11,11))

    def test_nominal_init(self):
        """
        Create a nominal MatrixOperation object and verify that it initialized
        correctly. This will check all the properties and class variables that
        are created upon initialization.
        """

        # Create a nominal MatrixOperation object with two valid matrices
        matop = MatrixOperation('Nominal Matrices',
                                self.matrix_1,
                                self.matrix_2)

        # Verify the initialization is valid
        self.assertTrue(matop.valid)

        # Verify the input name and matrices are correct
        self.assertEqual(matop.name, 'Nominal Matrices')
        self.assertTrue(np.array_equal(matop.matrixA, self.matrix_1))
        self.assertTrue(np.array_equal(matop.matrixB, self.matrix_2))

        # Verify that the matrix product calcualted is correct
        self.assertTrue(np.array_equal(matop.product, np.array([[25,11],[58,32],[91,53]])))

        # Verify that the properties of the matrix product are valid
        self.assertEqual(matop.productShape, (3,2))
        self.assertEqual(matop.productRows, 3)
        self.assertEqual(matop.productCols, 2)

    def test_off_nominal_init(self):
        """
        Creates various off-nominal MatrixOperation objects that are expected
        to fail upon creation due to invalid input and verifies that they failed
        to initialize properly.
        """

        # Create a MatrixOperation object which has two matrices that cannot be
        # multiplied due to mismatching sizes.
        with self.assertRaises(MatrixOperationError):
            matop = MatrixOperation('Mismatched Matrices',
                                    self.matrix_1,
                                    self.matrix_3)
            self.assertFalse(matop.valid)

        # Create a MatrixOperation object which has a matrix that is not 2D
        with self.assertRaises(MatrixOperationError):
            matop = MatrixOperation('3D Matrix',
                                    self.matrix_1,
                                    self.matrix_4)

        # Create a MatrixOperation object which has a matrix that is empty.
        with self.assertRaises(MatrixOperationError):
            matop = MatrixOperation('Empty Matrix',
                                    self.matrix_1,
                                    self.matrix_5)
            self.assertFalse(matop.valid)

        # Create a MatrixOperation object which has a matrix that is larger than
        # 10x10.
        with self.assertRaises(MatrixOperationError):
            matop = MatrixOperation('Large Matrix',
                                    self.matrix_1,
                                    self.matrix_6)
            self.assertFalse(matop.valid)

    def test_nominal_operations(self):
        """
        Create a nominal MatrixOperation object and verify that the matrix
        operations return valid values. No off-nominal inputs will be provided
        for this test.
        """

        # Create a nominal MatrixOperation object with two valid matrices
        matop = MatrixOperation('Nominal Matrices',
                                self.matrix_1,
                                self.matrix_2)

        # Verify the statistics calculated on/along a column produces correct
        # values
        self.assertEqual(matop.getProductColSum(0), 174)
        self.assertEqual(matop.getProductColSum(1), 96)
        self.assertEqual(matop.getProductColProd(0), 131950)
        self.assertEqual(matop.getProductColProd(1), 18656)
        self.assertTrue(np.array_equal(matop.getProductColCumSum(),
                                       np.array([[25,11],
                                                 [83,43],
                                                 [174,96]])))
        self.assertTrue(np.array_equal(matop.getProductColCumProd(),
                                       np.array([[25,11],
                                                 [1450,352],
                                                 [131950,18656]])))

        # Verify the statistics calculated on/along a row produces correct
        # values
        self.assertEqual(matop.getProductRowSum(0), 36)
        self.assertEqual(matop.getProductRowSum(1), 90)
        self.assertEqual(matop.getProductRowSum(2), 144)
        self.assertEqual(matop.getProductRowProd(0), 275)
        self.assertEqual(matop.getProductRowProd(1), 1856)
        self.assertEqual(matop.getProductRowProd(2), 4823)
        self.assertTrue(np.array_equal(matop.getProductRowCumSum(),
                                       np.array([[25,36],
                                                 [58,90],
                                                 [91,144]])))
        self.assertTrue(np.array_equal(matop.getProductRowCumProd(),
                                       np.array([[25,275],
                                                 [58,1856],
                                                 [91,4823]])))

        # Verify the statistics calculated on the entire product matrix are
        # correct.
        self.assertEqual(matop.getProductTotalSum(), 270)
        self.assertEqual(matop.getProductTotalProd(), 2461659200)
        self.assertEqual(matop.getProductTotalMean(), 45)
        self.assertEqual(matop.getProductTotalMedian(), 42.5)
        self.assertEqual(matop.getProductTotalMin(), 11)
        self.assertEqual(matop.getProductTotalMax(), 91)

    def test_off_nominal_operations(self):
        """
        Create a nominal MatrixOperation object and verify that when invalid
        inputs are provided to generate the matrix operations, that errors
        are thrown.
        """

        # Create a nominal MatrixOperation object with two valid matrices
        matop = MatrixOperation('Nominal Matrices',
                                self.matrix_1,
                                self.matrix_2)

        # Verify that a < 0 column input to a statistic function throws an
        # error.
        with self.assertRaises(MatrixOperationError):
            matop.getProductColSum(-1)

        # Verify that a column input that is too large to a statistic function
        # throws an error.
        with self.assertRaises(MatrixOperationError):
            matop.getProductColProd(10)

        # Verify that a < 0 row input to a statistic function throws an error.
        with self.assertRaises(MatrixOperationError):
            matop.getProductRowSum(-5)

        # Verify that a row input that is too large to a statistic function
        # throws an error.
        with self.assertRaises(MatrixOperationError):
            matop.getProductRowProd(4)


if __name__ == '__main__':
    unittest.main()
