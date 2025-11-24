#ifndef S21_UTILS_H
#define S21_UTILS_H

#include <stdint.h>

#include "s21_decimal.h"

typedef enum { FALSE, TRUE } TBool;

typedef enum { SUCCESS, FAULT } TResult;

typedef enum { OK, TOO_BIG, TOO_SMALL, ZERO_DIVISION } TRes;

#define TOTAL_BYTES 4
#define MAX_BIT 32
#define TOTAL_BITS 96
#define MAX_EXP 28
#define FLOAT_ACCURACY 7

#define MINUS 0x80000000        // 10000000 00000000 00000000 00000000
#define EXP 0x00ff0000          // 00000000 11111111 00000000 00000000
#define BROKEN_MASK 0x7FE0FFFF  // 01111111 11100000 11111111 11111111

#define SET_ZERO(val) ((val) = (s21_decimal){0})
#define SET_MINUS(val) ((val)->bits[3] |= MINUS)
#define CHECK_MINUS(val) ((val.bits[3] & MINUS) ? 0 : 1)
#define verification_zero(val) \
  ((val).bits[0] == 0 && (val).bits[1] == 0 && (val).bits[2] == 0)
#define check_broken(val) (val.bits[3] & BROKEN_MASK)

TBool find_bit(s21_decimal value, int bit);
void set_bit(s21_decimal *value, int bit);
TBool shift_bit_left(s21_decimal *decimal, int n);

void normal_form_exp(s21_decimal *value_1, s21_decimal *value_2);
int take_exp(s21_decimal value);
void set_exp(s21_decimal *dst, int scale);
TBool exp_increase(s21_decimal *value);
int exp_reduction(s21_decimal *value);

s21_decimal abs_decimal(s21_decimal value);
void sub_decimals(s21_decimal value_1, s21_decimal value_2,
                  s21_decimal *result);
s21_decimal divide(s21_decimal value_1, s21_decimal value_2,
                   s21_decimal *result);

#endif
