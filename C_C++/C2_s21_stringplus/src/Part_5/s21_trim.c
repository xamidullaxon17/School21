#include "../s21_string.h"

void *s21_trim(const char *src, const char *trim_chars) {
  if (src == NULL || trim_chars == NULL) return s21_NULL;

  s21_size_t src_len = s21_strlen(src);
  if (src_len == 0) {
    // Handle empty source string
    char *empty = (char *)malloc(1);
    if (empty) empty[0] = '\0';
    return empty;
  }

  s21_size_t start = 0;
  while (start < src_len) {
    int found = 0;
    for (s21_size_t i = 0; trim_chars[i] != '\0'; i++) {
      if (src[start] == trim_chars[i]) {
        found = 1;
        break;
      }
    }
    if (!found) break;
    start++;
  }

  s21_size_t end = src_len - 1;
  while (end > start) {
    int found = 0;
    for (s21_size_t i = 0; trim_chars[i] != '\0'; i++) {
      if (src[end] == trim_chars[i]) {
        found = 1;
        break;
      }
    }
    if (!found) break;
    end--;
  }

  s21_size_t new_len = (start > end) ? 0 : end - start + 1;
  char *result = (char *)malloc((new_len + 1) * sizeof(char));
  if (result == NULL) return s21_NULL;

  for (s21_size_t i = 0; i < new_len; i++) {
    result[i] = src[start + i];
  }
  result[new_len] = '\0';
  return result;
}