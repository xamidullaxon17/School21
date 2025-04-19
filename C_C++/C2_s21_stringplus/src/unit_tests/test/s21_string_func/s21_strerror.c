#include "../../s21_string_test.h"

START_TEST(test_strerror_1) {
  int errnum = 0;
  TEST_STRERROR(errnum);
}
END_TEST

START_TEST(test_strerror_2) {
  int errnum = 134;
  TEST_STRERROR(errnum);
}
END_TEST

START_TEST(test_strerror_3) {
  int errnum = -2;
  TEST_STRERROR(errnum);
}
END_TEST

START_TEST(test_strerror_4) {
  int errnum = 133;
  TEST_STRERROR(errnum);
}
END_TEST

START_TEST(test_strerror_5) {
  int errnum = 1;
  TEST_STRERROR(errnum);
}
END_TEST

START_TEST(test_strerror_6) {
  for (int errnum = -3; errnum < 140; errnum++) {
    TEST_STRERROR(errnum);
  }
}
END_TEST

Suite *strerror_suite(void) {
  Suite *s = suite_create("s21_strerror");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strerror_1);
  tcase_add_test(tc_core, test_strerror_2);
  tcase_add_test(tc_core, test_strerror_3);
  tcase_add_test(tc_core, test_strerror_4);
  tcase_add_test(tc_core, test_strerror_5);
  tcase_add_test(tc_core, test_strerror_6);

  suite_add_tcase(s, tc_core);
  return s;
}