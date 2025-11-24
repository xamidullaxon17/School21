#include "s21_matrix.h"

int s21_calc_complements(matrix_t *A, matrix_t *result) {
  TResult status = INCORRECT_MATRIX;
  if (is_matrix_correct(A)) {
    status = INCORRECT_COUNT;
    if (A->rows == A->columns) {
      status = s21_create_matrix(A->rows, A->columns, result);
      if (status == OK) status = calc_minor_matrix(A, result);
    }
  }
  return status;
}

TResult calc_minor_matrix(matrix_t *A, matrix_t *result) {
  TResult status = OK;
  result->matrix[0][0] = 1;
  if (A->rows != 1) {
    for (int i = 0; i < A->rows; i++)
      for (int j = 0; j < A->columns; j++) {
        double determ;
        matrix_t minored_matrix;
        status = minor(i + 1, j + 1, A, &minored_matrix);
        if (status == OK) {
          status = s21_determinant(&minored_matrix, &determ);
          if (status == 0) result->matrix[i][j] = pow((-1), i + j) * determ;
        }
        s21_remove_matrix(&minored_matrix);
      }
  }
  return status;
}

TResult minor(int row, int column, matrix_t *A, matrix_t *result) {
  TResult status = INCORRECT_MATRIX;
  if (A->matrix != NULL) {
    status = s21_create_matrix(A->rows - 1, A->columns - 1, result);
    if (status == OK) {
      int m, n;
      for (int i = 0; i < A->rows; i++) {
        m = i;
        if (i > row - 1) m--;
        for (int j = 0; j < A->columns; j++) {
          n = j;
          if (j > column - 1) n--;
          if (i != row - 1 && j != column - 1)
            result->matrix[m][n] = A->matrix[i][j];
        }
      }
    }
  }
  return status;
}