#include "../s21_string.h"

char *s21_strchr(const char *str, int c) {
  while (*str != '\0') {
    if (*str == c) {
      return (char *)str;
    }
    str++;
  }

  if ((char)c == '\0') {
    return (char *)str;
  }

  return s21_NULL;
}