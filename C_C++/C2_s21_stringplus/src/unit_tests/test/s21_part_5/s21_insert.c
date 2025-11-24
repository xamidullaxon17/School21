#include "../../s21_string_test.h"

START_TEST(test_insert_basic) {
  char str[] = "Hello World";
  char src[] = "Beautiful ";
  char *result = s21_insert(str, src, 6);
  ck_assert_str_eq(result, "Hello Beautiful World");
  free(result);
}
END_TEST

START_TEST(test_insert_beginning) {
  char str[] = "World";
  char src[] = "Hello ";
  char *result = s21_insert(str, src, 0);
  ck_assert_str_eq(result, "Hello World");
  free(result);
}
END_TEST

START_TEST(test_insert_end) {
  char str[] = "Hello";
  char src[] = " World";
  char *result = s21_insert(str, src, 5);
  ck_assert_str_eq(result, "Hello World");
  free(result);
}
END_TEST

START_TEST(test_insert_empty_src) {
  char str[] = "Hello World";
  char src[] = "";
  char *result = s21_insert(str, src, 5);
  ck_assert_str_eq(result, "Hello World");
  free(result);
}
END_TEST

START_TEST(test_insert_empty_str) {
  char str[] = "";
  char src[] = "Hello";
  char *result = s21_insert(str, src, 0);
  ck_assert_str_eq(result, "Hello");
  free(result);
}
END_TEST

START_TEST(test_insert_null_str) {
  char *str = NULL;
  char src[] = "Hello";
  char *result = s21_insert(str, src, 0);
  ck_assert_ptr_eq(result, NULL);
}
END_TEST

START_TEST(test_insert_null_src) {
  char str[] = "Hello";
  char *src = NULL;
  char *result = s21_insert(str, src, 0);
  ck_assert_ptr_eq(result, NULL);
}
END_TEST

START_TEST(test_insert_invalid_position) {
  char str[] = "Hello";
  char src[] = "World";
  char *result = s21_insert(str, src, 10);
  ck_assert_ptr_eq(result, NULL);
}
END_TEST

START_TEST(test_insert_special_chars) {
  char str[] = "Hello!@#";
  char src[] = "$%^&";
  char *result = s21_insert(str, src, 5);
  ck_assert_str_eq(result, "Hello$%^&!@#");
  free(result);
}
END_TEST

Suite *insert_suite(void) {
  Suite *s = suite_create("s21_insert");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_insert_basic);
  tcase_add_test(tc_core, test_insert_beginning);
  tcase_add_test(tc_core, test_insert_end);
  tcase_add_test(tc_core, test_insert_empty_src);
  tcase_add_test(tc_core, test_insert_empty_str);
  tcase_add_test(tc_core, test_insert_null_str);
  tcase_add_test(tc_core, test_insert_null_src);
  tcase_add_test(tc_core, test_insert_invalid_position);
  tcase_add_test(tc_core, test_insert_special_chars);

  suite_add_tcase(s, tc_core);
  return s;
}
