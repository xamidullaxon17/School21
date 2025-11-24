#include "../../s21_string_test.h"

START_TEST(test_memchr_1) {
  char str1[] = {0x00, 0x11, 0x22};
  char str2[] = {0x00, 0x11, 0x22};
  TEST_MEMCMP(str1, str2, s21_strlen(str1));
}
END_TEST

START_TEST(test_memchr_2) {
  char str1[] = {0x00, 0x11, 0x22};
  char str2[] = {0x01, 0x11, 0x22};
  TEST_MEMCMP(str1, str2, s21_strlen(str1));
}
END_TEST

START_TEST(test_memchr_3) {
  char str1[] = "HelloWorld";
  char str2[] = "HelloXorld";
  TEST_MEMCMP(str1, str2, s21_strlen(str1));
}
END_TEST

START_TEST(test_memchr_4) {
  char str1[] = {0x00, 0x11, 0x22};
  char str2[] = {0x00, 0x11, 0x22};
  TEST_MEMCMP(str1, str2, 0);
}
END_TEST

START_TEST(test_memchr_5) {
  char str1[] = {0x00, 0x11, 0xFF};
  char str2[] = {0x00, 0x1, 0xFF};
  TEST_MEMCMP(str1, str2, s21_strlen(str1));
}
END_TEST

Suite *memcmp_suite(void) {
  Suite *s = suite_create("s21_memcmp");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_memchr_1);
  tcase_add_test(tc_core, test_memchr_2);
  tcase_add_test(tc_core, test_memchr_3);
  tcase_add_test(tc_core, test_memchr_4);
  tcase_add_test(tc_core, test_memchr_5);

  suite_add_tcase(s, tc_core);
  return s;
}