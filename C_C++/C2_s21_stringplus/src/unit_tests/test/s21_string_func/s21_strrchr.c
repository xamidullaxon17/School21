#include "../../s21_string_test.h"

START_TEST(test_strrchr_1) {
  char str[] = "Hello world";
  char c = 'l';
  TEST_STRRCHR(str, c);
}
END_TEST

START_TEST(test_strrchr_2) {
  char str[] = "Hello world";
  char c = 'z';
  TEST_STRRCHR(str, c);
}
END_TEST

START_TEST(test_strrchr_3) {
  char str[] = "Hello world";
  char c = '\0';
  TEST_STRRCHR(str, c);
}
END_TEST

START_TEST(test_strrchr_4) {
  char str[] = "";
  char c = 'a';
  TEST_STRRCHR(str, c);
}
END_TEST

START_TEST(test_strrchr_5) {
  char str[] = "A";
  char c = 'A';
  TEST_STRRCHR(str, c);
}
END_TEST

Suite *strrchr_suite(void) {
  Suite *s = suite_create("s21_strrchr");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strrchr_1);
  tcase_add_test(tc_core, test_strrchr_2);
  tcase_add_test(tc_core, test_strrchr_3);
  tcase_add_test(tc_core, test_strrchr_4);
  tcase_add_test(tc_core, test_strrchr_5);

  suite_add_tcase(s, tc_core);
  return s;
}