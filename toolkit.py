from copy import deepcopy
from matrix import *


class SLAE:
    def __init__(self, matrix, vector, precision):
        self.initial_matrix = deepcopy(matrix)
        self.vector = deepcopy(vector)
        self.dimension = len(matrix)
        self.identity = [[0 if i != j else 1 for j in range(len(self.initial_matrix[0]))]
                         for i in range(len(self.initial_matrix))]
        if precision:
            self.precision = 1 / precision
        else:
            raise EnvironmentError("You have to specify the precision value > 0!")

    def set_precision(self, precision):
        self.precision = 1 / precision

    @staticmethod
    def util_sum(matrix, i, x):
        s = 0
        for j in range(len(matrix[0])):
            if j != i:
                s += matrix[i][j] * x[j]
        return s

    def simple_iterative_method(self):
        # A transposed * A
        transposed = Matrix.transposed(self.initial_matrix)
        matrix_a_t_a = Matrix.multiply(transposed, self.initial_matrix)
        a_t_a_norm = Matrix.norm(matrix_a_t_a)
        matrix_b = Matrix.sub(self.identity, Matrix.div(matrix_a_t_a, a_t_a_norm))
        vector_b = Matrix.multiply_matrix_column(transposed, [self.vector[i] / a_t_a_norm for i in range(len(self.vector))])
        iterations_number = 0
        x_prev = [0 for _ in range(len(self.vector))]
        x_vector = deepcopy(vector_b)
        while max_difference(x_vector, x_prev) > self.precision:
            x_prev = deepcopy(x_vector)
            x_vector = Matrix.add_v(Matrix.multiply_matrix_column(matrix_b, x_vector), vector_b)
            iterations_number += 1
        return x_vector, iterations_number, matrix_b, vector_b

    def jacobi_method(self):
        iterations_number = 0
        x_prev = [0 for _ in range(len(self.vector))]
        x_vector = deepcopy(self.vector)
        while max_difference(x_vector, x_prev) > self.precision:
            x_prev = deepcopy(x_vector)
            x_vector = [(-self.util_sum(self.initial_matrix, i, x_vector) +
                         self.vector[i]) / self.initial_matrix[i][i]
                        for i in range(len(x_vector))]
            iterations_number += 1
        return x_vector, iterations_number

    @staticmethod
    def seidel_sum(b_matrix, i, x):
        s = 0
        for j in range(len(x)):
            if i != j:
                s += b_matrix[i][j] * x[j]
        return s

    def seidel_gauss_method(self):
        x_prev = [0 for _ in range(len(self.vector))]
        x_vector = deepcopy(self.vector)
        iterations_number = 0
        while max_difference(x_vector, x_prev) > self.precision:
            x_prev = deepcopy(x_vector)
            for i in range(len(x_vector)):
                x_vector[i] = (-self.seidel_sum(self.initial_matrix, i, x_vector) +
                               self.vector[i]) / self.initial_matrix[i][i]
            iterations_number += 1
        return x_vector, iterations_number

    def incoherence(self, x_vector):
        result = Matrix.multiply_matrix_column(self.initial_matrix, x_vector)
        return [self.vector[i] - result[i]
                for i in range(len(self.vector))]
