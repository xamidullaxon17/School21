#include "s21_decimal.h"
#include "s21_utils.h"

int s21_add(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  TRes result_flag = OK;
  SET_ZERO(*result);
  normal_form_exp(&value_1, &value_2);

  if (CHECK_MINUS(value_1) == CHECK_MINUS(value_2)) {
    int temp_one = 0;
    for (int byte = 0; byte < TOTAL_BYTES; byte++)
      for (int bit = 0; bit < MAX_BIT; bit++) {
        int sum_bits = find_bit(value_1, bit + (byte * MAX_BIT)) +
                       find_bit(value_2, bit + (byte * MAX_BIT)) + temp_one;
        TBool bit_set = FALSE;
        switch (sum_bits) {
          case 0:
            continue;
          case 1:
            bit_set = TRUE;
            temp_one = 0;
            break;
          case 2:
            temp_one = 1;
            continue;
          case 3:
            temp_one = 1;
            bit_set = TRUE;
            break;
        }
        if (bit_set) set_bit(result, bit + (byte * MAX_BIT));
      }
    if (!CHECK_MINUS(value_1) && !CHECK_MINUS(value_2)) SET_MINUS(result);
  }
  if (CHECK_MINUS(value_1) != CHECK_MINUS(value_2)) {
    if (s21_is_greater(abs_decimal(value_1), abs_decimal(value_2))) {
      s21_sub(abs_decimal(value_1), abs_decimal(value_2), result);
      if (!CHECK_MINUS(value_1)) SET_MINUS(result);
    } else {
      s21_sub(abs_decimal(value_2), abs_decimal(value_1), result);
      if (!CHECK_MINUS(value_2)) SET_MINUS(result);
    }
  }
  if (take_exp(value_1)) set_exp(result, take_exp(value_1));
  if (find_bit(*result, TOTAL_BITS)) {
    s21_decimal res = *result;
    result_flag = CHECK_MINUS(res) ? TOO_BIG : TOO_SMALL;
  }
  return result_flag;
}

int s21_sub(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  int result_flag = OK;
  SET_ZERO(*result);
  normal_form_exp(&value_1, &value_2);
  if (CHECK_MINUS(value_1) == CHECK_MINUS(value_2)) {
    sub_decimals(abs_decimal(value_1), abs_decimal(value_2), result);
    if (s21_is_greater(abs_decimal(value_1), abs_decimal(value_2)))
      result->bits[3] |= (value_1.bits[3] & MINUS);
    else if (s21_is_greater(value_2, value_1))
      result->bits[3] |= MINUS;
  } else if (CHECK_MINUS(value_1) && !CHECK_MINUS(value_2))
    s21_add(abs_decimal(value_1), abs_decimal(value_2), result);
  else if (!CHECK_MINUS(value_1) && CHECK_MINUS(value_2)) {
    s21_add(abs_decimal(value_1), abs_decimal(value_2), result);
    SET_MINUS(result);
  }
  set_exp(result, take_exp(value_1));
  if (find_bit(*result, TOTAL_BITS)) {
    s21_decimal res = *result;
    result_flag = CHECK_MINUS(res) ? TOO_BIG : TOO_SMALL;
  }
  return result_flag;
}

int s21_mul(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  int result_flag = OK;
  int result_exp;
  SET_ZERO(*result);
  for (int i = 0; i < MAX_BIT * (TOTAL_BYTES - 1); i++) {
    if (find_bit(value_1, i)) {
      s21_decimal tmp_value = value_2;
      if (shift_bit_left(&tmp_value, i))
        s21_add(*result, tmp_value, result);
      else {
        result_flag =
            (CHECK_MINUS(value_1) ^ CHECK_MINUS(value_2)) ? TOO_SMALL : TOO_BIG;
        SET_ZERO(*result);
      }
    }
  }
  result_exp = take_exp(value_1) + take_exp(value_2);
  set_exp(result, result_exp);
  while (take_exp(*result) > 28) exp_reduction(result);
  *result = abs_decimal(*result);
  if (CHECK_MINUS(value_1) ^ CHECK_MINUS(value_2)) SET_MINUS(result);
  if (verification_zero(*result)) set_exp(result, 0);

  return result_flag;
}

int s21_div(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  TRes result_flag = OK;
  TBool val1_zero = FALSE;
  s21_decimal fraction_result;
  SET_ZERO(fraction_result);
  SET_ZERO(*result);
  if (verification_zero(value_2)) result_flag = ZERO_DIVISION;
  if (verification_zero(value_1)) val1_zero = TRUE;

  if (result_flag != ZERO_DIVISION && !val1_zero) {
    normal_form_exp(&value_1, &value_2);
    set_exp(&value_1, 0);
    set_exp(&value_2, 0);
    s21_decimal remainder = divide(value_1, value_2, result);
    s21_decimal fraction_remainder;
    int remainder_exp = 0;

    for (int i = 0; !verification_zero(remainder) && i < FLOAT_ACCURACY; i++) {
      while (s21_is_less(abs_decimal(remainder), abs_decimal(value_2))) {
        exp_increase(&remainder);
        set_exp(&remainder, take_exp(remainder) - 1);
        remainder_exp++;
      }

      SET_ZERO(fraction_result);
      fraction_remainder = divide(remainder, value_2, &fraction_result);
      set_exp(&fraction_result, remainder_exp);
      result_flag = s21_add(*result, fraction_result, result);
      remainder = fraction_remainder;
    }
    if (CHECK_MINUS(value_1) != CHECK_MINUS(value_2)) SET_MINUS(result);
  }
  return result_flag;
}
