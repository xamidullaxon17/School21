#include "../../s21_string_test.h"

START_TEST(test_strstr_1) {
  char haystack[] = "Hello World";
  char needle[] = "World";
  TEST_STRSTR(haystack, needle);
}
END_TEST

START_TEST(test_strstr_2) {
  char haystack[] = "Hello World";
  char needle[] = "There";
  TEST_STRSTR(haystack, needle);
}
END_TEST

START_TEST(test_strstr_3) {
  char haystack[] = "Hello World";
  char needle[] = "";
  TEST_STRSTR(haystack, needle);
}
END_TEST

START_TEST(test_strstr_4) {
  char haystack[] = "";
  char needle[] = "World";
  TEST_STRSTR(haystack, needle);
}
END_TEST

START_TEST(test_strstr_5) {
  char haystack[] = "";
  char needle[] = "";
  TEST_STRSTR(haystack, needle);
}
END_TEST

START_TEST(test_strstr_6) {
  char haystack[] = "Test";
  char needle[] = "Test";
  TEST_STRSTR(haystack, needle);
}
END_TEST

Suite *strstr_suite(void) {
  Suite *s = suite_create("s21_strstr");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strstr_1);
  tcase_add_test(tc_core, test_strstr_2);
  tcase_add_test(tc_core, test_strstr_3);
  tcase_add_test(tc_core, test_strstr_4);
  tcase_add_test(tc_core, test_strstr_5);
  tcase_add_test(tc_core, test_strstr_6);

  suite_add_tcase(s, tc_core);
  return s;
}