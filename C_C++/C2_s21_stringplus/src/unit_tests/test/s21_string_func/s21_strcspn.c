#include "../../s21_string_test.h"

START_TEST(test_strcspn_1) {
  char str1[] = "Hello World!";
  char str2[] = "XYZ";
  TEST_STRCSPN(str1, str2);
}
END_TEST

START_TEST(test_strcspn_2) {
  char str1[] = "abcdef";
  char str2[] = "de";
  TEST_STRCSPN(str1, str2);
}
END_TEST

START_TEST(test_strcspn_3) {
  char str1[] = "abcdef";
  char str2[] = "a";
  TEST_STRCSPN(str1, str2);
}
END_TEST

START_TEST(test_strcspn_4) {
  char str1[] = "abcdef";
  char str2[] = "";
  TEST_STRCSPN(str1, str2);
}
END_TEST

START_TEST(test_strcspn_5) {
  char str1[] = "";
  char str2[] = "de";
  TEST_STRCSPN(str1, str2);
}
END_TEST

START_TEST(test_strcspn_6) {
  char str1[] = "";
  char str2[] = "";
  TEST_STRCSPN(str1, str2);
}
END_TEST

START_TEST(test_strcspn_7) {
  char str1[] = "hello world";
  char str2[] = "ow";
  TEST_STRCSPN(str1, str2);
}
END_TEST

Suite *strcspn_suite(void) {
  Suite *s = suite_create("s21_strcspn");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strcspn_1);
  tcase_add_test(tc_core, test_strcspn_2);
  tcase_add_test(tc_core, test_strcspn_3);
  tcase_add_test(tc_core, test_strcspn_4);
  tcase_add_test(tc_core, test_strcspn_5);
  tcase_add_test(tc_core, test_strcspn_6);
  tcase_add_test(tc_core, test_strcspn_7);

  suite_add_tcase(s, tc_core);
  return s;
}