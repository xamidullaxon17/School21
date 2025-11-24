#include "s21_matrix.h"

int s21_determinant(matrix_t *A, double *result) {
  TResult status = INCORRECT_MATRIX;
  if (is_matrix_correct(A)) {
    status = INCORRECT_COUNT;
    if (A->rows == A->columns) {
      status = OK;
      *result = A->matrix[0][0];
      if (A->rows != 1) *result = s21_determinant_count(A);
    }
  }
  return status;
}

double s21_determinant_count(matrix_t *A) {
  double result = 0;
  if (A->rows == 2) {
    result =
        A->matrix[0][0] * A->matrix[1][1] - A->matrix[0][1] * A->matrix[1][0];
  } else {
    for (int i = 0; i < A->rows; i++) {
      matrix_t minored_matrix;
      minor(1, i + 1, A, &minored_matrix);
      result += pow((-1), i) * A->matrix[0][i] *
                s21_determinant_count(&minored_matrix);
      s21_remove_matrix(&minored_matrix);
    }
  }
  return result;
}