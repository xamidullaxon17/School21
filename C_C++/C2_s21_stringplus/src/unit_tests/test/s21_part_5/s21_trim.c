#include "../../s21_string_test.h"

START_TEST(test_trim_basic) {
  char str[] = "   hello   ";
  char trim_chars[] = " ";
  char *result = s21_trim(str, trim_chars);
  ck_assert_str_eq(result, "hello");
  free(result);
}
END_TEST

START_TEST(test_trim_multiple_chars) {
  char str[] = "...hello...";
  char trim_chars[] = ".";
  char *result = s21_trim(str, trim_chars);
  ck_assert_str_eq(result, "hello");
  free(result);
}
END_TEST

START_TEST(test_trim_no_trim_needed) {
  char str[] = "hello";
  char trim_chars[] = " ";
  char *result = s21_trim(str, trim_chars);
  ck_assert_str_eq(result, "hello");
  free(result);
}
END_TEST

START_TEST(test_trim_empty_string) {
  char str[] = "";
  char trim_chars[] = " ";
  char *result = s21_trim(str, trim_chars);
  ck_assert_str_eq(result, "");
  free(result);
}
END_TEST

START_TEST(test_trim_all_trimchars) {
  char str[] = "   ";
  char trim_chars[] = " ";
  char *result = s21_trim(str, trim_chars);
  ck_assert_str_eq(result, "");
  free(result);
}
END_TEST

START_TEST(test_trim_null_str) {
  char *str = NULL;
  char trim_chars[] = " ";
  char *result = s21_trim(str, trim_chars);
  ck_assert_ptr_eq(result, NULL);
}
END_TEST

START_TEST(test_trim_null_trim_chars) {
  char str[] = "hello";
  char *trim_chars = NULL;
  char *result = s21_trim(str, trim_chars);
  ck_assert_ptr_eq(result, NULL);
}
END_TEST

START_TEST(test_trim_multiple_different_chars) {
  char str[] = "...###@@@hello...###@@@";
  char trim_chars[] = ".#@";
  char *result = s21_trim(str, trim_chars);
  ck_assert_str_eq(result, "hello");
  free(result);
}
END_TEST

START_TEST(test_trim_no_matching_chars) {
  char str[] = "...hello...";
  char trim_chars[] = " @#$";
  char *result = s21_trim(str, trim_chars);
  ck_assert_str_eq(result, "...hello...");
  free(result);
}
END_TEST

START_TEST(test_trim_empty_trim_chars) {
  char str[] = "   hello   ";
  char trim_chars[] = "";
  char *result = s21_trim(str, trim_chars);
  ck_assert_str_eq(result, "   hello   ");
  free(result);
}
END_TEST

Suite *trim_suite(void) {
  Suite *s = suite_create("s21_trim");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_trim_basic);
  tcase_add_test(tc_core, test_trim_multiple_chars);
  tcase_add_test(tc_core, test_trim_no_trim_needed);
  tcase_add_test(tc_core, test_trim_empty_string);
  tcase_add_test(tc_core, test_trim_all_trimchars);
  tcase_add_test(tc_core, test_trim_null_str);
  tcase_add_test(tc_core, test_trim_null_trim_chars);
  tcase_add_test(tc_core, test_trim_multiple_different_chars);
  tcase_add_test(tc_core, test_trim_no_matching_chars);
  tcase_add_test(tc_core, test_trim_empty_trim_chars);

  suite_add_tcase(s, tc_core);
  return s;
}
