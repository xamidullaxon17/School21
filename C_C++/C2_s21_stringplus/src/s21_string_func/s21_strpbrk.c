#include "../s21_string.h"

char *s21_strpbrk(const char *str1, const char *str2) {
  while (*str1) {
    const char *temp = str2;
    while (*temp) {
      if (*str1 == *temp) {
        return (char *)str1;
      }
      temp++;
    }
    str1++;
  }
  return s21_NULL;
}
