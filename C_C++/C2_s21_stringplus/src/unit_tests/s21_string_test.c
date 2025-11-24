#include "s21_string_test.h"

int main(void) {
  int number_failed;
  SRunner *sr = srunner_create(memchr_suite());
  srunner_add_suite(sr, memcmp_suite());
  srunner_add_suite(sr, memcpy_suite());
  srunner_add_suite(sr, memset_suite());
  srunner_add_suite(sr, strchr_suite());
  srunner_add_suite(sr, strcspn_suite());
  srunner_add_suite(sr, strerror_suite());
  srunner_add_suite(sr, strncat_suite());
  srunner_add_suite(sr, strncmp_suite());
  srunner_add_suite(sr, strncpy_suite());
  srunner_add_suite(sr, strpbrk_suite());
  srunner_add_suite(sr, strrchr_suite());
  srunner_add_suite(sr, strstr_suite());
  srunner_add_suite(sr, strtok_suite());
  srunner_add_suite(sr, sprintf_suite());

  srunner_add_suite(sr, to_upper_suite());
  srunner_add_suite(sr, to_lower_suite());
  srunner_add_suite(sr, trim_suite());
  srunner_add_suite(sr, insert_suite());

  srunner_run_all(sr, CK_VERBOSE);
  number_failed = srunner_ntests_failed(sr);
  srunner_free(sr);

  return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}
