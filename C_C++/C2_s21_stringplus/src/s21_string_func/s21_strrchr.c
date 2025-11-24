#include "../s21_string.h"

char *s21_strrchr(const char *str, int c) {
  char *last = s21_NULL;
  const char ch = (char)c;

  if (str != s21_NULL) {
    while (*str != '\0') {
      if (*str == ch) {
        last = (char *)str;
      }
      str++;
    }

    if (ch == '\0') {
      last = (char *)str;
    }
  }

  return last;
}