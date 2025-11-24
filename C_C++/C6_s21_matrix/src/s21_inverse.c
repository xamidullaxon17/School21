#include "s21_matrix.h"

int s21_inverse_matrix(matrix_t *A, matrix_t *result) {
  TResult status = INCORRECT_MATRIX;
  if (is_matrix_correct(A)) {
    status = INCORRECT_COUNT;
    double determ;
    s21_determinant(A, &determ);
    if (fabs(determ - 0) > 1e-6) {
      matrix_t det_matrix;
      status = s21_calc_complements(A, &det_matrix);
      if (status == OK) {
        matrix_t transposed_matrix;
        status = s21_transpose(&det_matrix, &transposed_matrix);
        if (status == 0)
          s21_mult_number(&transposed_matrix, 1 / determ, result);
        s21_remove_matrix(&transposed_matrix);
      }
      s21_remove_matrix(&det_matrix);
    }
  }
  return status;
}