#include "../../s21_string_test.h"

START_TEST(test_memchr_found) {
  char str[] = "Hello, World!";
  TEST_MEMCHR(str, 'W', s21_strlen(str));
}
END_TEST

START_TEST(test_memchr_not_found) {
  char str[] = "Hello, World!";
  TEST_MEMCHR(str, 'Z', s21_strlen(str));
}
END_TEST

START_TEST(test_memchr_outside_length) {
  char str[] = "Hello, World!";
  TEST_MEMCHR(str, 'W', 5);
}
END_TEST

START_TEST(test_memchr_null_char) {
  char str[] = "Hello\0World";
  TEST_MEMCHR(str, '\0', 12);
}
END_TEST

START_TEST(test_memchr_empty_string) {
  char str[] = "";
  TEST_MEMCHR(str, 'A', 0);
}
END_TEST

START_TEST(test_memchr_null_with_zero_length) {
  void *str = NULL;
  TEST_MEMCHR(str, 'A', 0);
}
END_TEST

START_TEST(test_memchr_binary_data) {
  unsigned char data[] = {0x10, 0x20, 0x30, 0x40, 0x50};
  TEST_MEMCHR(data, 0x30, sizeof(data));
}
END_TEST

START_TEST(test_memchr_multiple_occurrences) {
  char str[] = "Hello, Hello, Hello!";
  TEST_MEMCHR(str, 'l', s21_strlen(str));
}
END_TEST

START_TEST(test_memchr_long_string) {
  const s21_size_t length = 10000;
  char *long_str = malloc(length + 1);
  ck_assert_ptr_nonnull(long_str);
  for (s21_size_t i = 0; i < length; i++) {
    long_str[i] = 'A' + (i % 26);
  }
  long_str[length] = '\0';
  long_str[length - 10] = 'Z';
  TEST_MEMCHR(long_str, 'Z', length);
  free(long_str);
}
END_TEST

Suite *memchr_suite(void) {
  Suite *s = suite_create("s21_memchr");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_memchr_found);
  tcase_add_test(tc_core, test_memchr_not_found);
  tcase_add_test(tc_core, test_memchr_outside_length);
  tcase_add_test(tc_core, test_memchr_null_char);
  tcase_add_test(tc_core, test_memchr_empty_string);
  tcase_add_test(tc_core, test_memchr_null_with_zero_length);
  tcase_add_test(tc_core, test_memchr_binary_data);
  tcase_add_test(tc_core, test_memchr_multiple_occurrences);
  tcase_add_test(tc_core, test_memchr_long_string);

  suite_add_tcase(s, tc_core);
  return s;
}
