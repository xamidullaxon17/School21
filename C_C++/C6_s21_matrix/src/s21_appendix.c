#include "s21_matrix.h"

TBool is_matrix_correct(matrix_t *matrix) {
  return (matrix != NULL && matrix->matrix != NULL && matrix->rows >= 1 &&
          matrix->columns >= 1)
             ? TRUE
             : FALSE;
}