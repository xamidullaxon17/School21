#include "../s21_string.h"

char *s21_strncat(char *dest, const char *src, s21_size_t n) {
  if (dest != s21_NULL && src != s21_NULL) {
    char *result = dest;

    while (*result) {
      result++;
    }

    s21_size_t i;
    for (i = 0; i < n && src[i] != '\0'; i++) {
      result[i] = src[i];
    }

    result[i] = '\0';
  }
  return dest;
}