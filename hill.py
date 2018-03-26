import numpy.matrixlib as matrix_lib
import numpy as np
from math import gcd, pow, ceil
import alphabet
import copy

class HillKey(matrix_lib.matrix):
    def __new__(self, key):
        return super(HillKey, self).__new__(self, key)

    def get_modular_multiplicative_inverse(self):
        determinant = self.get_determinant()
        prime_numbers = [1,3,5,7,9,11,15,17,19,21,23,25]
        for number in prime_numbers:
            if int(round(determinant * number % 26)) == int(round(1 % 26)):
                return number

    def get_adjugate_matrix(self):
        matrix = self.getA()
        adjugate_matrix_as_array = []
        for i, line in enumerate(matrix):
            adjugate_matrix_as_array.append([])
            for j, row in enumerate(line):
                tpm_sub_matrix = np.delete(matrix, i, 0)
                tpm_sub_matrix = np.delete(tpm_sub_matrix, j, 1)
                co_factor = pow(-1, i + j) * np.linalg.det(tpm_sub_matrix)
                adjugate_matrix_as_array[i].append(co_factor)
        adjugate_matrix = matrix_lib.matrix(adjugate_matrix_as_array)
        return adjugate_matrix

    def get_size(self):
        matrix = self.getA()
        return len(matrix[0])
    
    def get_determinant(self):
        determinant = None
        try:
           determinant = np.linalg.det(self)
        except np.linalg.LinAlgError:
             return None
        return determinant

    def is_valid(self):
        # Matrix must be a square
        matrix = self.getA()
        if len(matrix[0]) != len(matrix):
            return False
        # Matrix elements must be positive
        for line in matrix:
            for row in line:
                if row < 0:
                    return False
        # Check if the matrix is invertible by calculing the determinant
        determinant = self.get_determinant()
        if not determinant:
            return False
        # Check if the inverted matrix and 26 are coprime integers by checking if the gcd equals 1
        gcd_result = gcd(int(round(determinant)), 26)
        return (gcd_result == 1)


class Hill:
    def __init__(self, key):
        self.key = HillKey(key)

    def _apply_algorithm(self, message, matrix_as_array):
        characters = list(message)
        chunk_length = self.key.get_size()
        grouped_characters  = [characters[i:i + chunk_length] for i in range(0, len(characters), chunk_length)]    
        processed_message = []
        for group in grouped_characters:
            for i, character_to_decrypt in enumerate(group):
                result = 0
                for j, character in enumerate(group):
                    result += int(round(matrix_as_array[i][j])) * alphabet.get_letter_position(character)
                processed_character = int(round(result % 26))
                try:
                    processed_message.append(alphabet.letters[processed_character - alphabet.offset])
                except:
                    pass

        return processed_message

    def encrypt(self, message):
        crypted_message = self._apply_algorithm(message, self.key.getA())
        return "".join(crypted_message)

    def decrypt(self, message):
        adjugate_matrix = self.key.get_adjugate_matrix()
        transposed_adjugate_matrix = adjugate_matrix.transpose()
        modular_multiplicative_inverse = self.key.get_modular_multiplicative_inverse()
        final_matrix = (modular_multiplicative_inverse * transposed_adjugate_matrix % 26).getA()
        decrypted_message = self._apply_algorithm(message, final_matrix)

        return "".join(decrypted_message)
        