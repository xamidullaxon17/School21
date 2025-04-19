#include "../../s21_string_test.h"

START_TEST(test_strpbrk_1) {
  char str1[] = "Hello world";
  char str2[] = "ow";
  TEST_STRPBRK(str1, str2);
}
END_TEST

START_TEST(test_strpbrk_2) {
  char str1[] = "Hello world";
  char str2[] = "xyz";
  TEST_STRPBRK(str1, str2);
}
END_TEST

START_TEST(test_strpbrk_3) {
  char str1[] = "Hello world";
  char str2[] = "";
  TEST_STRPBRK(str1, str2);
}
END_TEST

START_TEST(test_strpbrk_4) {
  char str1[] = "";
  char str2[] = "abc";
  TEST_STRPBRK(str1, str2);
}
END_TEST

START_TEST(test_strpbrk_5) {
  char str1[] = "";
  char str2[] = "";
  TEST_STRPBRK(str1, str2);
}
END_TEST

START_TEST(test_strpbrk_6) {
  char str1[] = "Hello world";
  char str2[] = "eee";
  TEST_STRPBRK(str1, str2);
}
END_TEST

Suite *strpbrk_suite(void) {
  Suite *s = suite_create("s21_strpbrk");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strpbrk_1);
  tcase_add_test(tc_core, test_strpbrk_2);
  tcase_add_test(tc_core, test_strpbrk_3);
  tcase_add_test(tc_core, test_strpbrk_4);
  tcase_add_test(tc_core, test_strpbrk_5);
  tcase_add_test(tc_core, test_strpbrk_6);

  suite_add_tcase(s, tc_core);
  return s;
}