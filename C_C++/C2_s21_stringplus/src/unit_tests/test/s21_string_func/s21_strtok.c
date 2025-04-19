#include "../../s21_string_test.h"

START_TEST(test_strtok_1) {
  char str[] = "Hello, world! This is strtok.";
  char delim[] = " ,.!";
  TEST_STRTOK(str, delim);
}
END_TEST

START_TEST(test_strtok_2) {
  char str[] = "";
  char delim[] = " ,.!";
  TEST_STRTOK(str, delim);
}
END_TEST

START_TEST(test_strtok_3) {
  char str[] = "Hello world This is strtok";
  char delim[] = ",.!";
  TEST_STRTOK(str, delim);
}
END_TEST

START_TEST(test_strtok_4) {
  char str[] = " ,.!";
  char delim[] = " ,.!";
  TEST_STRTOK(str, delim);
}
END_TEST

START_TEST(test_strtok_5) {
  char str[] = ",,Hello,,World,,";
  char delim[] = ",";
  TEST_STRTOK(str, delim);
}
END_TEST

START_TEST(test_strtok_6) {
  char str[] = "Hello World";
  char delim[] = ",";
  TEST_STRTOK(str, delim);
}
END_TEST

Suite *strtok_suite(void) {
  Suite *s = suite_create("s21_strtok");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_strtok_1);
  tcase_add_test(tc_core, test_strtok_2);
  tcase_add_test(tc_core, test_strtok_3);
  tcase_add_test(tc_core, test_strtok_4);
  tcase_add_test(tc_core, test_strtok_5);
  tcase_add_test(tc_core, test_strtok_6);

  suite_add_tcase(s, tc_core);
  return s;
}