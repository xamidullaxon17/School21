#include "../../s21_string_test.h"

START_TEST(test_memset_1) {
  char src[] = "Hello World!";
  TEST_MEMSET(src + 3, '.', 2 * sizeof(char));
}
END_TEST

START_TEST(test_memset_2) {
  int src[3];
  TEST_MEMSET(src, 0, 3 * sizeof(int));
}
END_TEST

START_TEST(test_memset_3) {
  char src[] = "Hello World!";
  TEST_MEMSET(src + 3, '.', 0);
}
END_TEST

START_TEST(test_memset_4) {
  char src[1000];
  TEST_MEMSET(src, 'G', 1000 * sizeof(char));
}
END_TEST

Suite *memset_suite(void) {
  Suite *s = suite_create("s21_memset");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_memset_1);
  tcase_add_test(tc_core, test_memset_2);
  tcase_add_test(tc_core, test_memset_3);
  tcase_add_test(tc_core, test_memset_4);

  suite_add_tcase(s, tc_core);
  return s;
}