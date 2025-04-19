#include "../../s21_string_test.h"

START_TEST(test_to_lower_basic) {
  char str[] = "HELLO";
  char *result = s21_to_lower(str);
  ck_assert_str_eq(result, "hello");
  free(result);
}
END_TEST

START_TEST(test_to_lower_mixed) {
  char str[] = "HeLLo WoRLD";
  char *result = s21_to_lower(str);
  ck_assert_str_eq(result, "hello world");
  free(result);
}
END_TEST

START_TEST(test_to_lower_numbers) {
  char str[] = "HELLO123";
  char *result = s21_to_lower(str);
  ck_assert_str_eq(result, "hello123");
  free(result);
}
END_TEST

START_TEST(test_to_lower_special) {
  char str[] = "HELLO!@#$%";
  char *result = s21_to_lower(str);
  ck_assert_str_eq(result, "hello!@#$%");
  free(result);
}
END_TEST

START_TEST(test_to_lower_empty) {
  char str[] = "";
  char *result = s21_to_lower(str);
  ck_assert_str_eq(result, "");
  free(result);
}
END_TEST

START_TEST(test_to_lower_null) {
  char *str = NULL;
  char *result = s21_to_lower(str);
  ck_assert_ptr_eq(result, NULL);
}
END_TEST

START_TEST(test_to_lower_all_upper) {
  char str[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  char *result = s21_to_lower(str);
  ck_assert_str_eq(result, "abcdefghijklmnopqrstuvwxyz");
  free(result);
}
END_TEST

START_TEST(test_to_lower_only_spaces) {
  char str[] = "   ";
  char *result = s21_to_lower(str);
  ck_assert_str_eq(result, "   ");
  free(result);
}
END_TEST

Suite *to_lower_suite(void) {
  Suite *s = suite_create("s21_to_lower");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_to_lower_basic);
  tcase_add_test(tc_core, test_to_lower_mixed);
  tcase_add_test(tc_core, test_to_lower_numbers);
  tcase_add_test(tc_core, test_to_lower_special);
  tcase_add_test(tc_core, test_to_lower_empty);
  tcase_add_test(tc_core, test_to_lower_null);
  tcase_add_test(tc_core, test_to_lower_all_upper);
  tcase_add_test(tc_core, test_to_lower_only_spaces);

  suite_add_tcase(s, tc_core);
  return s;
}
