#include "s21_utils.h"

#include "s21_decimal.h"

TBool find_bit(s21_decimal value, int bit) {
  int index = bit / MAX_BIT;
  unsigned int mask = 1 << (bit % MAX_BIT);
  return (value.bits[index] & mask) ? TRUE : FALSE;
}

void set_bit(s21_decimal *value, int bit) {
  int index = bit / MAX_BIT;
  unsigned int mask = 1 << (bit % MAX_BIT);
  value->bits[index] |= mask;
}

TBool shift_bit_left(s21_decimal *decimal, int n) {
  TBool flag = TRUE;
  int count = 0;
  while (count < n && flag) {
    if (find_bit(*decimal, (TOTAL_BITS - 1))) flag = FALSE;
    for (int i = TOTAL_BYTES - 2; i >= 0; i--) {
      decimal->bits[i] <<= 1;
      if (i > 0) {
        int hrbit =
            ((i - 1) * MAX_BIT) + (MAX_BIT - 1);  // старший бит в правом байте
        if (find_bit(*decimal, hrbit)) set_bit(decimal, hrbit + 1);
      }
    }
    count++;
  }
  return flag;
}

s21_decimal abs_decimal(s21_decimal value) {
  value.bits[3] &= ~MINUS;
  return value;
}

void sub_decimals(s21_decimal value_1, s21_decimal value_2,
                  s21_decimal *result) {
  s21_decimal min_value, max_value;
  if (s21_is_greater(value_1, value_2)) {
    max_value = value_1;
    min_value = value_2;
  } else {
    max_value = value_2;
    min_value = value_1;
  }

  int temp_one = 0;
  for (int index = 0; index < TOTAL_BYTES - 1; index++) {
    for (int bit = 0; bit < MAX_BIT; bit++) {
      TBool larger_bit = find_bit(max_value, bit + (index * MAX_BIT));
      TBool smaller_bit = find_bit(min_value, bit + (index * MAX_BIT));
      int dif = larger_bit - smaller_bit - temp_one;

      if (dif == 0)
        temp_one = 0;
      else if (dif == 1) {
        set_bit(result, bit + (index * MAX_BIT));
        temp_one = 0;
      } else if (dif == -1) {
        set_bit(result, bit + (index * MAX_BIT));
        temp_one = 1;
      } else if (dif == -2)
        temp_one = 1;
    }
  }
}

int take_exp(s21_decimal value) { return (value.bits[3] & EXP) >> 16; }

void set_exp(s21_decimal *dst, int scale) {
  dst->bits[3] &= ~EXP;
  dst->bits[3] |= (EXP & (scale << 16));
}

void normal_form_exp(s21_decimal *value_1, s21_decimal *value_2) {
  int exp_1, exp_2;
  exp_1 = take_exp(*value_1);
  exp_2 = take_exp(*value_2);

  if (exp_1 != exp_2) {
    for (int i = 0; i < abs(exp_1 - exp_2); i++)
      if (exp_1 > exp_2) {
        if (0 == exp_increase(value_2)) exp_reduction(value_1);
      } else {
        if (0 == exp_increase(value_1)) exp_reduction(value_2);
      }
  }
}

TBool exp_increase(s21_decimal *value) {
  TBool success_code = TRUE;
  int current_exp = take_exp(*value);
  if (current_exp >= MAX_EXP)
    success_code = FALSE;
  else {
    s21_decimal tmp_eight = *value, tmp_two = *value;
    set_exp(&tmp_eight, 0);
    set_exp(&tmp_two, 0);
    if (!shift_bit_left(&tmp_eight, 3) || !shift_bit_left(&tmp_two, 1))
      success_code = FALSE;
    if (success_code) {
      if (s21_add(tmp_eight, tmp_two, value) != 0) success_code = FALSE;
      set_exp(value, current_exp + 1);
    }
  }
  return success_code;
}

int exp_reduction(s21_decimal *value) {
  TBool flag = FALSE;
  int remainder = 0;
  s21_decimal result;
  SET_ZERO(result);

  for (int i = (TOTAL_BITS - 1); i >= 0; i--) {
    remainder = remainder << 1;
    shift_bit_left(&result, 1);
    if (find_bit(*value, i)) remainder++;
    if (remainder - 10 >= 0) {
      set_bit(&result, 0);
      remainder -= 10;
    }
  }
  if (flag || verification_zero(*value) || !take_exp(*value))
    flag = TRUE;
  else {
    result.bits[3] = value->bits[3];
    set_exp(&result, take_exp(*value) - 1);
    *value = result;
  }
  return flag ? -1 : remainder;
}

s21_decimal divide(s21_decimal value_1, s21_decimal value_2,
                   s21_decimal *result) {
  s21_decimal remainder;
  SET_ZERO(remainder);

  for (int i = (TOTAL_BITS - 1); i >= 0; i--) {
    shift_bit_left(&remainder, 1);
    shift_bit_left(result, 1);
    if (find_bit(value_1, i)) set_bit(&remainder, 0);
    if (s21_is_greater_or_equal(remainder, abs_decimal(value_2))) {
      set_bit(result, 0);
      s21_sub(remainder, abs_decimal(value_2), &remainder);
    }
  }
  return remainder;
}