#include "../../s21_string_test.h"

START_TEST(test_sprintf_1) { TEST_SPRINTF("Value: %d, Text: %s", 42, "Hello"); }
END_TEST

START_TEST(test_sprintf_2) { TEST_SPRINTF("Num: %6d, Float: %.2f", 7, 3.1415); }
END_TEST

START_TEST(test_sprintf_3) { TEST_SPRINTF("Result: %+d", -10); }
END_TEST

START_TEST(test_sprintf_4) { TEST_SPRINTF("100%% sure"); }
END_TEST

START_TEST(test_sprintf_5) {
  TEST_SPRINTF("Int: %d, Float: %.1f, String: %s, Char: %c", 123, 4.56, "Test",
               'A');
}
END_TEST

START_TEST(test_sprintf_6) { TEST_SPRINTF("123456789"); }
END_TEST

START_TEST(test_sprintf_7) { TEST_SPRINTF("abcdef"); }
END_TEST

START_TEST(test_sprintf_8) {
  const char *format = "Unknown spec: %q";
  TEST_SPRINTF(format, 123);
}
END_TEST

START_TEST(test_sprintf_9) { TEST_SPRINTF("Unsigned: %u", 300); }
END_TEST

START_TEST(test_sprintf_10) { TEST_SPRINTF("|%-5d|", 42); }
END_TEST

START_TEST(test_sprintf_11) { TEST_SPRINTF("|%+d|", 42); }
END_TEST

START_TEST(test_sprintf_12) { TEST_SPRINTF("|%5d|", 42); }
END_TEST

START_TEST(test_sprintf_13) { TEST_SPRINTF("|%.2f|", 3.14159); }
END_TEST

START_TEST(test_sprintf_14) { TEST_SPRINTF("|%.3s|", "Hello"); }
END_TEST

START_TEST(test_sprintf_15) { TEST_SPRINTF("|%.5d|", 42); }
END_TEST

START_TEST(test_sprintf_16) { TEST_SPRINTF("|%hd|", (short)12345); }
END_TEST

START_TEST(test_sprintf_17) { TEST_SPRINTF("|%ld|", (long)1234567890); }
END_TEST

START_TEST(test_sprintf_18) { TEST_SPRINTF("|%lf|", 3.14); }
END_TEST

START_TEST(test_sprintf_19) {
  TEST_SPRINTF("Int: %+5d, Float: %-8.3f, Str: %.4s, Unsigned: %u", 42, 3.14159,
               "Hello", 300);
}
END_TEST

Suite *sprintf_suite(void) {
  Suite *s = suite_create("s21_sprintf");
  TCase *tc_core = tcase_create("Core");

  tcase_add_test(tc_core, test_sprintf_1);
  tcase_add_test(tc_core, test_sprintf_2);
  tcase_add_test(tc_core, test_sprintf_3);
  tcase_add_test(tc_core, test_sprintf_4);
  tcase_add_test(tc_core, test_sprintf_5);
  tcase_add_test(tc_core, test_sprintf_6);
  tcase_add_test(tc_core, test_sprintf_7);
  tcase_add_test(tc_core, test_sprintf_8);
  tcase_add_test(tc_core, test_sprintf_9);
  tcase_add_test(tc_core, test_sprintf_10);
  tcase_add_test(tc_core, test_sprintf_11);
  tcase_add_test(tc_core, test_sprintf_12);
  tcase_add_test(tc_core, test_sprintf_13);
  tcase_add_test(tc_core, test_sprintf_14);
  tcase_add_test(tc_core, test_sprintf_15);
  tcase_add_test(tc_core, test_sprintf_16);
  tcase_add_test(tc_core, test_sprintf_17);
  tcase_add_test(tc_core, test_sprintf_18);
  tcase_add_test(tc_core, test_sprintf_19);

  suite_add_tcase(s, tc_core);
  return s;
}