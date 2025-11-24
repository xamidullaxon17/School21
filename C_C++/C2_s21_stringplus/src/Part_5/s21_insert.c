#include "../s21_string.h"

void *s21_insert(const char *src, const char *str, size_t start_index) {
  if (src == NULL || str == NULL) return s21_NULL;

  s21_size_t src_len = s21_strlen(src);
  s21_size_t str_len = s21_strlen(str);

  if (start_index > src_len) return s21_NULL;

  s21_size_t new_len = src_len + str_len;
  char *result = (char *)malloc((new_len + 1) * sizeof(char));

  if (result == NULL) return s21_NULL;

  for (s21_size_t i = 0; i < start_index; i++) {
    result[i] = src[i];
  }

  for (s21_size_t i = 0; i < str_len; i++) {
    result[start_index + i] = str[i];
  }

  for (s21_size_t i = start_index; i < src_len; i++) {
    result[str_len + i] = src[i];
  }

  result[new_len] = '\0';
  return result;
}