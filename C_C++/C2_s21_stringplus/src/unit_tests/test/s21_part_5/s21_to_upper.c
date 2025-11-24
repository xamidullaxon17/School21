#include "../../s21_string_test.h"

START_TEST(test_to_upper_basic) {
  char str[] = "hello";
  char *result = s21_to_upper(str);
  ck_assert_str_eq(result, "HELLO");
  free(result);
}
END_TEST

START_TEST(test_to_upper_mixed) {
  char str[] = "HeLLo WoRLD";
  char *result = s21_to_upper(str);
  ck_assert_str_eq(result, "HELLO WORLD");
  free(result);
}
END_TEST

START_TEST(test_to_upper_numbers) {
  char str[] = "hello123";
  char *result = s21_to_upper(str);
  ck_assert_str_eq(result, "HELLO123");
  free(result);
}
END_TEST

START_TEST(test_to_upper_special) {
  char str[] = "hello!@#$%";
  char *result = s21_to_upper(str);
  ck_assert_str_eq(result, "HELLO!@#$%");
  free(result);
}
END_TEST

START_TEST(test_to_upper_empty) {
  char str[] = "";
  char *result = s21_to_upper(str);
  ck_assert_str_eq(result, "");
  free(result);
}
END_TEST

START_TEST(test_to_upper_null) {
  char *str = NULL;
  char *result = s21_to_upper(str);
  ck_assert_ptr_eq(result, NULL);
}
END_TEST

START_TEST(test_to_upper_all_lower) {
  char str[] = "abcdefghijklmnopqrstuvwxyz";
  char *result = s21_to_upper(str);
  ck_assert_str_eq(result, "ABCDEFGHIJKLMNOPQRSTUVWXYZ");
  free(result);
}
END_TEST

START_TEST(test_to_upper_only_spaces) {
  char str[] = "   ";
  char *result = s21_to_upper(str);
  ck_assert_str_eq(result, "   ");
  free(result);
}
END_TEST

Suite *to_upper_suite(void) {
  Suite *s = suite_create("s21_to_upper");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_to_upper_basic);
  tcase_add_test(tc_core, test_to_upper_mixed);
  tcase_add_test(tc_core, test_to_upper_numbers);
  tcase_add_test(tc_core, test_to_upper_special);
  tcase_add_test(tc_core, test_to_upper_empty);
  tcase_add_test(tc_core, test_to_upper_null);
  tcase_add_test(tc_core, test_to_upper_all_lower);
  tcase_add_test(tc_core, test_to_upper_only_spaces);

  suite_add_tcase(s, tc_core);
  return s;
}
