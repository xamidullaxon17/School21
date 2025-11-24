#include "s21_matrix.h"

int s21_mult_matrix(matrix_t *A, matrix_t *B, matrix_t *result) {
  TResult status = INCORRECT_MATRIX;
  if (is_matrix_correct(A) && is_matrix_correct(B)) {
    if (A->columns == B->rows) {
      status = s21_create_matrix(A->rows, B->columns, result);
      if (status == OK)
        for (int i = 0; i < A->rows; i++)
          for (int j = 0; j < B->columns; j++)
            for (int k = 0; k < B->rows; k++)
              result->matrix[i][j] += A->matrix[i][k] * B->matrix[k][j];
    } else {
      status = INCORRECT_COUNT;
    }
  }
  return status;
}