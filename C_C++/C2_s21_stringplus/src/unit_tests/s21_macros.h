#ifndef TEST_MACROS_H_
#define TEST_MACROS_H_

#include <check.h>
#include <stdlib.h>
#include <string.h>

#include "../s21_string.h"

#define TEST_MEMCHR(str, c, n)                  \
  {                                             \
    void *expected = memchr((str), (c), (n));   \
    void *result = s21_memchr((str), (c), (n)); \
    ck_assert_ptr_eq(result, expected);         \
  }

#define TEST_MEMCMP(str1, str2, n)                \
  do {                                            \
    int expected = memcmp((str1), (str2), (n));   \
    int result = s21_memcmp((str1), (str2), (n)); \
    ck_assert_int_eq(result, expected);           \
  } while (0)

#define TEST_MEMCPY(dest, src, n)                        \
  do {                                                   \
    void *expected = memcpy((dest), (src), (n));         \
    void *result = s21_memcpy((dest), (src), (n));       \
    ck_assert_mem_eq(result, expected, strlen(src) + 1); \
  } while (0)

#define TEST_MEMSET(src, c, n)                  \
  do {                                          \
    void *expected = memset((src), (c), (n));   \
    void *result = s21_memset((src), (c), (n)); \
    ck_assert_ptr_eq(result, expected);         \
  } while (0)

#define TEST_STRCHR(src, c)                \
  do {                                     \
    char *expected = strchr((src), (c));   \
    char *result = s21_strchr((src), (c)); \
    ck_assert_ptr_eq(result, expected);    \
  } while (0)

#define TEST_STRCSPN(str1, str2)                     \
  do {                                               \
    s21_size_t expected = strcspn((str1), (str2));   \
    s21_size_t result = s21_strcspn((str1), (str2)); \
    ck_assert_uint_eq(result, expected);             \
  } while (0)

#define TEST_STRERROR(errnum)              \
  do {                                     \
    char *expected = strerror((errnum));   \
    char *result = s21_strerror((errnum)); \
    ck_assert_str_eq(result, expected);    \
  } while (0)

#define TEST_STRNCAT(dest, src, n)                  \
  do {                                              \
    char *expected = strncat((dest), (src), (n));   \
    char *result = s21_strncat((dest), (src), (n)); \
    ck_assert_str_eq(result, expected);             \
  } while (0)

#define TEST_STRNCMP(str1, str2, n)                \
  do {                                             \
    int expected = strncmp((str1), (str2), (n));   \
    int result = s21_strncmp((str1), (str2), (n)); \
    ck_assert_int_eq(result, expected);            \
  } while (0)

#define TEST_STRNCPY(dest, src, n)                  \
  do {                                              \
    char *expected = strncpy((dest), (src), (n));   \
    char *result = s21_strncpy((dest), (src), (n)); \
    ck_assert_ptr_eq(result, expected);             \
  } while (0)

#define TEST_STRPBRK(str1, str2)                \
  do {                                          \
    char *expected = strpbrk((str1), (str2));   \
    char *result = s21_strpbrk((str1), (str2)); \
    ck_assert_ptr_eq(result, expected);         \
  } while (0)

#define TEST_STRRCHR(str, c)                \
  do {                                      \
    char *expected = strrchr((str), (c));   \
    char *result = s21_strrchr((str), (c)); \
    ck_assert_ptr_eq(result, expected);     \
  } while (0)

#define TEST_STRSTR(haystack, needle)                \
  do {                                               \
    char *expected = strstr((haystack), (needle));   \
    char *result = s21_strstr((haystack), (needle)); \
    ck_assert_ptr_eq(result, expected);              \
  } while (0)

#define TEST_STRTOK(str, delim)                   \
  do {                                            \
    char expected_buf[256];                       \
    char result_buf[256];                         \
    strcpy(expected_buf, str);                    \
    strcpy(result_buf, str);                      \
    char *expected = strtok(expected_buf, delim); \
    char *result = s21_strtok(result_buf, delim); \
    while (expected != NULL && result != NULL) {  \
      ck_assert_str_eq(result, expected);         \
      expected = strtok(NULL, delim);             \
      result = s21_strtok(NULL, delim);           \
    }                                             \
    ck_assert_ptr_eq(result, expected);           \
  } while (0)

#define TEST_SPRINTF(format, ...)                                \
  {                                                              \
    char expected[1024] = {0};                                   \
    char result[1024] = {0};                                     \
    int expected_len = sprintf(expected, format, ##__VA_ARGS__); \
    int result_len = s21_sprintf(result, format, ##__VA_ARGS__); \
    ck_assert_str_eq(result, expected);                          \
    ck_assert_int_eq(result_len, expected_len);                  \
  }

#endif