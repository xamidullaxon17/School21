#include <math.h>

#include "s21_decimal.h"
#include "s21_utils.h"

int s21_from_int_to_decimal(int src, s21_decimal *dst) {
  TResult flag = SUCCESS;
  if (isnan((float)src) || isinf((float)src) || !dst)
    flag = FAULT;
  else {
    SET_ZERO(*dst);
    if (src < 0) set_bit(dst, 127);
    int number = abs(src);
    dst->bits[0] = number;
  }
  return flag;
}

int s21_from_decimal_to_int(s21_decimal src, int *dst) {
  TResult flag = SUCCESS;
  if (!dst || (unsigned int)src.bits[0] > INT32_MAX || src.bits[1] != 0 ||
      src.bits[2] != 0)
    flag = FAULT;
  else {
    *dst = src.bits[0];
    if (find_bit(src, 127)) *dst = -1 * *dst;
  }
  return flag;
}

int s21_from_float_to_decimal(float src, s21_decimal *dst) {
  SET_ZERO(*dst);
  TResult flag = SUCCESS;
  if (isinf(src) || isnan(src))
    flag = FAULT;
  else {
    if (src != 0) {
      int sign = (src < 0) ? 1 : 0;
      int exp = ((*(int *)&src & ~MINUS) >> 23) - 127;
      double temp = (double)fabs(src);
      int scale = 0;
      while (scale < MAX_EXP && (int)temp / (int)pow(2, 23) == 0) {
        temp *= 10;
        scale++;
      }
      temp = round(temp);
      if (scale <= MAX_EXP && (exp > -94 && exp < 96)) {
        float tmp_float = 0;
        temp = (float)temp;
        while (fmod(temp, 10) == 0 && scale > 0) {
          scale--;
          temp /= 10;
        }
        tmp_float = temp;
        exp = ((*(int *)&tmp_float & ~MINUS) >> 23) - 127;
        dst->bits[exp / MAX_BIT] |= 1 << exp % MAX_BIT;
        for (int i = exp - 1, ii = 22; ii >= 0; i--, ii--)
          if ((*(int *)&tmp_float & (1 << ii)) != 0)
            dst->bits[i / MAX_BIT] |= 1 << i % MAX_BIT;
        set_exp(dst, scale);
        if (sign) SET_MINUS(dst);
      }
    }
  }
  return flag;
}

int s21_from_decimal_to_float(s21_decimal src, float *dst) {
  TResult flag = SUCCESS;
  double tmp = 0.0;
  *dst = 0.0;
  int scale = take_exp(src);
  for (int i = 0; i < MAX_BIT * (TOTAL_BYTES - 1); i++)
    if (find_bit(src, i)) tmp += pow(2, i);
  while (scale) {
    tmp /= 10;
    scale--;
  }
  *dst = (float)tmp;
  if (src.bits[3] & MINUS) *dst = *dst * (-1);
  return flag;
}