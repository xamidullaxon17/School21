#include "../../s21_string_test.h"

START_TEST(test_strncat_1) {
  char dest[20] = "Hello ";
  char src[] = "World";
  TEST_STRNCAT(dest, src, s21_strlen(src));
}
END_TEST

START_TEST(test_strncat_2) {
  char dest[] = "Hello ";
  char src[] = "";
  TEST_STRNCAT(dest, src, s21_strlen(src));
}
END_TEST

START_TEST(test_strncat_3) {
  char dest[] = "";
  char src[] = "";
  TEST_STRNCAT(dest, src, s21_strlen(src));
}
END_TEST

START_TEST(test_strncat_4) {
  char dest[] = "abcdef";
  char src[] = "abcdef";
  TEST_STRNCAT(dest, src, s21_strlen(src) - 2);
}
END_TEST

START_TEST(test_strncat_5) {
  char dest[] = "abcdef";
  char src[] = "abcdef";
  TEST_STRNCAT(dest, src, 0);
}
END_TEST

Suite *strncat_suite(void) {
  Suite *s = suite_create("s21_strncat");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strncat_1);
  tcase_add_test(tc_core, test_strncat_2);
  tcase_add_test(tc_core, test_strncat_3);
  tcase_add_test(tc_core, test_strncat_4);
  tcase_add_test(tc_core, test_strncat_5);

  suite_add_tcase(s, tc_core);
  return s;
}