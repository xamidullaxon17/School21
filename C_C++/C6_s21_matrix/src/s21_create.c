#include "s21_matrix.h"

int s21_create_matrix(int rows, int columns, matrix_t *result) {
  TResult status = OK;
  if (rows < 1 || columns < 1) {
    status = INCORRECT_MATRIX;
  } else {
    result->rows = rows;
    result->columns = columns;
    result->matrix = calloc(rows, sizeof(double *));
    status = INCORRECT_MATRIX;
    if (result->matrix != NULL) {
      for (int i = 0; i < result->rows; i++)
        result->matrix[i] = calloc(columns, sizeof(double));
      status = OK;
    }
  }
  return status;
}