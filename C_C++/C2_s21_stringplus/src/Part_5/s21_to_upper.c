#include "../s21_string.h"

void *s21_to_upper(const char *str) {
  if (str == NULL) return s21_NULL;

  s21_size_t len = s21_strlen(str);
  char *result = (char *)malloc((len + 1) * sizeof(char));

  if (result == NULL) return s21_NULL;

  for (s21_size_t i = 0; i < len; i++) {
    if (str[i] >= 'a' && str[i] <= 'z') {
      result[i] = str[i] - 32;  // Convert to uppercase
    } else {
      result[i] = str[i];  // Keep non-lowercase characters as is
    }
  }
  result[len] = '\0';  // Null terminate the string

  return result;
}