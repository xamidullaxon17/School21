#include "../s21_string.h"

char *s21_strtok(char *str, const char *delim) {
  static char *next_token = s21_NULL;
  char *token_start;

  if (str != s21_NULL) {
    next_token = str;
  }

  if (next_token == s21_NULL) {
    return s21_NULL;
  }

  while (*next_token && s21_strchr(delim, *next_token) != s21_NULL) {
    next_token++;
  }

  if (*next_token == '\0') {
    next_token = s21_NULL;
    return s21_NULL;
  }

  token_start = next_token;

  while (*next_token && s21_strchr(delim, *next_token) == s21_NULL) {
    next_token++;
  }

  if (*next_token != '\0') {
    *next_token = '\0';
    next_token++;
  } else {
    next_token = s21_NULL;
  }

  return token_start;
}