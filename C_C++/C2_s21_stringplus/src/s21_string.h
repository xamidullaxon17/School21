#ifndef S21_STRING_H_
#define S21_STRING_H_
// for s21_sprintf

// for 5_task allocating memory
#include <stdlib.h>

typedef long unsigned s21_size_t;

#define s21_NULL ((void *)0)

void *s21_memchr(const void *str, int c, s21_size_t n);

int s21_memcmp(const void *str1, const void *str2, s21_size_t n);

void *s21_memcpy(void *dest, const void *src, s21_size_t n);

void *s21_memset(void *str, int c, s21_size_t n);

char *s21_strncat(char *dest, const char *src, s21_size_t n);

char *s21_strchr(const char *str, int c);

int s21_strncmp(const char *str1, const char *str2, s21_size_t n);

char *s21_strncpy(char *dest, const char *src, s21_size_t n);

s21_size_t s21_strcspn(const char *str1, const char *str2);

char *s21_strerror(int errnum);

s21_size_t s21_strlen(const char *str);

char *s21_strpbrk(const char *str1, const char *str2);

char *s21_strrchr(const char *str, int c);

char *s21_strstr(const char *haystack, const char *needle);

char *s21_strtok(char *str, const char *delim);

#include <ctype.h>
#include <math.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Structure to store formatting options
typedef struct {
  // Flags
  int minus_flag;  // Left-justify within the field width
  int plus_flag;   // Always include a sign (+ or -)
  int space_flag;  // Prefix non-negative values with a space

  // Width and precision
  int width;          // Minimum field width
  int precision;      // Precision for floating-point or max width for strings
  int precision_set;  // Whether precision was explicitly set

  // Length modifiers
  int length_h;  // Short (for integers)
  int length_l;  // Long (for integers)
} FormatSpecifier;

// Function prototypes
int s21_sprintf(char *str, const char *format, ...);

int parse_format_specifier(const char *format, int *pos, FormatSpecifier *spec);

int process_int(char *str, int *length, va_list args, FormatSpecifier *spec);

int process_float(char *str, int *length, va_list args, FormatSpecifier *spec);

int process_char(char *str, int *length, va_list args, FormatSpecifier *spec);

int process_string(char *str, int *length, va_list args, FormatSpecifier *spec);

int process_unsigned(char *str, int *length, va_list args,
                     FormatSpecifier *spec);

void *s21_to_upper(const char *str);

void *s21_to_lower(const char *str);

void *s21_insert(const char *src, const char *str, size_t start_index);

void *s21_trim(const char *src, const char *trim_chars);

#endif