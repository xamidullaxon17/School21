#include "../../s21_string_test.h"

START_TEST(test_strchr_1) {
  char src[] = "Hello World!";
  TEST_STRCHR(src, 'W');
}
END_TEST

START_TEST(test_strchr_2) {
  char src[] = "Hello World!";
  TEST_STRCHR(src, 'Z');
}
END_TEST

START_TEST(test_strchr_3) {
  char src[] = "Hello World!";
  TEST_STRCHR(src, 'o');
}
END_TEST

START_TEST(test_strchr_4) {
  char src[] = "Hello World!";
  TEST_STRCHR(src, '\0');
}
END_TEST

START_TEST(test_strchr_5) {
  char src[] = "Hello World!";
  TEST_STRCHR(src, 0);
}
END_TEST

Suite *strchr_suite(void) {
  Suite *s = suite_create("s21_strchr");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strchr_1);
  tcase_add_test(tc_core, test_strchr_2);
  tcase_add_test(tc_core, test_strchr_3);
  tcase_add_test(tc_core, test_strchr_4);
  tcase_add_test(tc_core, test_strchr_5);

  suite_add_tcase(s, tc_core);
  return s;
}