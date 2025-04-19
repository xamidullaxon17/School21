#include "../s21_string.h"

int s21_strncmp(const char *str1, const char *str2, s21_size_t n) {
  if (str1 && str2) {
    while (n > 0) {
      if (*str1 != *str2) {
        return (*(unsigned char *)str1 - *(unsigned char *)str2);
      }
      str1++;
      str2++;
      n--;
    }
  }
  return 0;
}