#include "s21_decimal.h"
#include "s21_utils.h"

int s21_floor(s21_decimal value, s21_decimal *result) {
  TResult flag = SUCCESS;
  if (result == NULL || check_broken(value)) flag = FAULT;
  if (!flag) {
    s21_decimal minus_one = {{1, 0, 0, MINUS}};
    int value_exp = take_exp(value);
    if (value_exp) {
      for (int i = 0; i < value_exp; i++) exp_reduction(&value);
      if (!CHECK_MINUS(value)) s21_add(value, minus_one, &value);
    }
    if (verification_zero(value)) set_exp(&value, 0);
    *result = value;
  }
  return flag;
}

int s21_round(s21_decimal value, s21_decimal *result) {
  TResult flag = SUCCESS;
  if (result == NULL || check_broken(value)) flag = FAULT;
  if (!flag) {
    s21_decimal plus_one = {{1, 0, 0, 0}};
    int value_exp = take_exp(value);
    int remainder = 0;
    SET_ZERO(*result);
    if (value_exp) {
      for (int i = 0; i < value_exp; i++) remainder = exp_reduction(&value);
      if (remainder >= 5) {
        if (CHECK_MINUS(value))
          s21_add(value, plus_one, &value);
        else
          s21_sub(value, plus_one, &value);
      }
    }
    if (verification_zero(value)) set_exp(&value, 0);
    *result = value;
  }
  return flag;
}

int s21_truncate(s21_decimal value, s21_decimal *result) {
  TResult flag = SUCCESS;
  if (result == NULL || check_broken(value)) flag = FAULT;
  if (!flag) {
    int value_exp = take_exp(value);
    SET_ZERO(*result);
    if (value_exp)
      for (int i = 0; i < value_exp; i++) exp_reduction(&value);
    if (verification_zero(value)) set_exp(&value, 0);
    *result = value;
  }
  return flag;
}

int s21_negate(s21_decimal value, s21_decimal *result) {
  TResult flag = SUCCESS;
  if (result == NULL || check_broken(value)) flag = FAULT;
  if (!flag) {
    value.bits[3] ^= MINUS;
    *result = value;
  }
  return flag;
}
