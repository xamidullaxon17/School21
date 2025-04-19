#include "../../s21_string_test.h"

START_TEST(test_strncmp_1) {
  char str1[] = "Hello World";
  char str2[] = "Hello World";
  TEST_STRNCMP(str1, str2, s21_strlen(str1));
}
END_TEST

START_TEST(test_strncmp_2) {
  char str1[] = "Apple";
  char str2[] = "Banana";
  TEST_STRNCMP(str1, str2, s21_strlen(str1));
}
END_TEST

START_TEST(test_strncmp_3) {
  char str1[] = "HelloWorld";
  char str2[] = "HelloThere";
  TEST_STRNCMP(str1, str2, s21_strlen(str1));
}
END_TEST

START_TEST(test_strncmp_4) {
  char str1[] = "Hi";
  char str2[] = "High";
  TEST_STRNCMP(str1, str2, s21_strlen(str2));
}
END_TEST

START_TEST(test_strncmp_5) {
  char str1[] = "Hello World";
  char str2[] = "Hello World";
  TEST_STRNCMP(str1, str2, 0);
}
END_TEST

Suite *strncmp_suite(void) {
  Suite *s = suite_create("s21_strncmp");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strncmp_1);
  tcase_add_test(tc_core, test_strncmp_2);
  tcase_add_test(tc_core, test_strncmp_3);
  tcase_add_test(tc_core, test_strncmp_4);
  tcase_add_test(tc_core, test_strncmp_5);

  suite_add_tcase(s, tc_core);
  return s;
}