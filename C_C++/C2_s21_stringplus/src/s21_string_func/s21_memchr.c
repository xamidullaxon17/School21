#include "../s21_string.h"

void *s21_memchr(const void *str, int c, s21_size_t n) {
  void *result = s21_NULL;

  if (str != s21_NULL) {
    const unsigned char *p = str;

    for (s21_size_t i = 0; i < n; i++) {
      if (p[i] == (unsigned char)c) {
        result = (void *)(p + i);
        break;
      }
    }
  }

  return result;
}