#include "s21_decimal.h"
#include "s21_utils.h"

int s21_is_less(s21_decimal value_1, s21_decimal value_2) {
  TBool flag = FALSE;
  normal_form_exp(&value_1, &value_2);
  if (CHECK_MINUS(value_1) != CHECK_MINUS(value_2))
    flag = (CHECK_MINUS(value_1)) ? TRUE : FALSE;
  else {
    int bit = TOTAL_BITS - 1;
    while (bit >= 0 && find_bit(value_1, bit) == find_bit(value_2, bit)) bit--;
    if (bit >= 0 && find_bit(value_1, bit) < find_bit(value_2, bit))
      flag = TRUE;
  }
  if (CHECK_MINUS(value_1) && !CHECK_MINUS(value_2)) flag = FALSE;
  if (!CHECK_MINUS(value_1) && CHECK_MINUS(value_2)) flag = TRUE;
  if (!CHECK_MINUS(value_1) && !CHECK_MINUS(value_2)) flag = !flag;
  if (s21_is_equal(value_1, value_2)) flag = FALSE;
  return flag;
}

int s21_is_equal(s21_decimal value_1, s21_decimal value_2) {
  TBool flag = TRUE;
  normal_form_exp(&value_1, &value_2);
  int bit = TOTAL_BITS - 1;
  while (bit >= 0) {
    if (find_bit(value_1, bit) != find_bit(value_2, bit)) {
      flag = FALSE;
      bit = 0;
    }
    bit--;
  }
  if (CHECK_MINUS(value_1) != CHECK_MINUS(value_2)) flag = FALSE;
  if (verification_zero(value_1) && verification_zero(value_2)) flag = TRUE;
  return flag;
}

int s21_is_greater(s21_decimal value_1, s21_decimal value_2) {
  return (!s21_is_equal(value_1, value_2) && !s21_is_less(value_1, value_2))
             ? TRUE
             : FALSE;
}

int s21_is_not_equal(s21_decimal value_1, s21_decimal value_2) {
  return (s21_is_equal(value_1, value_2)) ? FALSE : TRUE;
}

int s21_is_greater_or_equal(s21_decimal value_1, s21_decimal value_2) {
  return s21_is_greater(value_1, value_2) || s21_is_equal(value_1, value_2);
}

int s21_is_less_or_equal(s21_decimal value_1, s21_decimal value_2) {
  return s21_is_less(value_1, value_2) || s21_is_equal(value_1, value_2);
}