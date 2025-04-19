#include "../../s21_string_test.h"

START_TEST(test_strncpy_1) {
  char src[] = "Hello";
  char dest[10] = "hi";
  TEST_STRNCPY(dest, src, 10);
}
END_TEST

START_TEST(test_strncpy_2) {
  char src[] = "Hello";
  char dest[3] = {0};
  TEST_STRNCPY(dest, src, 3);
}
END_TEST

START_TEST(test_strncpy_3) {
  char src[] = "Hello";
  char dest[10] = {0};
  TEST_STRNCPY(dest, src, 10);
}
END_TEST

START_TEST(test_strncpy_4) {
  char src[] = "";
  char dest[10] = {0};
  TEST_STRNCPY(dest, src, 10);
}
END_TEST

START_TEST(test_strncpy_5) {
  char src[] = "Hello";
  char dest[10] = "World";
  TEST_STRNCPY(dest, src, 5);
}
END_TEST

Suite *strncpy_suite(void) {
  Suite *s = suite_create("s21_strncpy");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strncpy_1);
  tcase_add_test(tc_core, test_strncpy_2);
  tcase_add_test(tc_core, test_strncpy_3);
  tcase_add_test(tc_core, test_strncpy_4);
  tcase_add_test(tc_core, test_strncpy_5);

  suite_add_tcase(s, tc_core);
  return s;
}