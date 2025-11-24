#include "../../s21_string_test.h"

START_TEST(test_memcpy_1) {
  char dest[] = "hello";
  char src[] = " world";
  TEST_MEMCPY(dest, src, s21_strlen(src));
}
END_TEST

START_TEST(test_memcpy_2) {
  char dest[] = "hello";
  char src[] = " world";
  TEST_MEMCPY(dest, src, 0);
}
END_TEST

START_TEST(test_memcpy_3) {
  char dest[] = "hello";
  char src[] = " world";
  TEST_MEMCPY(dest, src, 1);
}
END_TEST

START_TEST(test_memcpy_4) {
  char dest[] = {0x00, 0x11, 0xFF};
  char src[] = {0x00, 0x11, 0xFF};
  TEST_MEMCPY(dest, src, s21_strlen(src));
}
END_TEST

START_TEST(test_memcpy_5) {
  const s21_size_t length = 10000;
  char *dest = malloc(length + 1);
  ck_assert_ptr_nonnull(dest);
  for (s21_size_t i = 0; i < length; i++) {
    dest[i] = 'A' + (i % 26);
  }
  dest[length] = '\0';
  char *src = "hello";
  TEST_MEMCPY(dest, src, s21_strlen(src));
  free(dest);
}
END_TEST

Suite *memcpy_suite(void) {
  Suite *s = suite_create("s21_memcpy");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_memcpy_1);
  tcase_add_test(tc_core, test_memcpy_2);
  tcase_add_test(tc_core, test_memcpy_3);
  tcase_add_test(tc_core, test_memcpy_4);
  tcase_add_test(tc_core, test_memcpy_5);

  suite_add_tcase(s, tc_core);
  return s;
}