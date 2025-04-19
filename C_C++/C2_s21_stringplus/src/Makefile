CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c11 -g
LDFLAGS = -lcheck -lsubunit -pthread -lrt -lm

GCOV_FLAGS = -fprofile-arcs -ftest-coverage
GCOV_LIBS = -lgcov

SRC_DIR = s21_string_func
TASK5_DIR = 5_task
TEST_DIR = unit_tests
TEST_SUBDIR = unit_tests/test/s21_string_func
TEST_SPRINTF_DIR = unit_tests/test/s21_sprintf
TEST_PART_FIVE_DIR = unit_tests/test/s21_part_5
HEADER = s21_string.h

SRC = $(wildcard $(SRC_DIR)/*.c)
TASK5_SRC = $(wildcard $(TASK5_DIR)/*.c)
TEST_MAIN = $(TEST_DIR)/s21_string_test.c
TEST_SRC_SUBFOLDER = $(wildcard $(TEST_SUBDIR)/*.c)
TEST_SPRINTF = $(wildcard $(TEST_SPRINTF_DIR)/*.c)
TEST_PART_FIVE = $(wildcard $(TEST_PART_FIVE_DIR)/*.c)

ALL_SRC = $(SRC) $(TASK5_SRC) $(TEST_MAIN) $(TEST_SRC_SUBFOLDER) $(TEST_SPRINTF) $(TEST_PART_FIVE)

SRC_OBJ = $(SRC:.c=.o)
TASK5_OBJ = $(TASK5_SRC:.c=.o)


%.o: %.c $(HEADER)
	$(CC) $(CFLAGS) -c $< -o $@

s21_string.a: $(SRC_OBJ) $(TASK5_OBJ)
	ar rcs $@ $^
	ranlib $@

all: s21_string.a

test_runner: $(ALL_SRC)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

test: test_runner
	./test_runner

GCOV_DIR = gcov
GCOV_OBJ = $(patsubst %.c,$(GCOV_DIR)/%.o,$(ALL_SRC))

$(GCOV_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(GCOV_FLAGS) -c $< -o $@

gcov_build: $(GCOV_OBJ)
	$(CC) $(CFLAGS) $(GCOV_FLAGS) $^ -o $(GCOV_DIR)/test_runner_gcov $(LDFLAGS) $(GCOV_LIBS)

run_gcov: gcov_build
	./$(GCOV_DIR)/test_runner_gcov


gcov_report: run_gcov
	@mkdir -p $(GCOV_DIR)/report
	lcov --capture --directory $(GCOV_DIR) --output-file $(GCOV_DIR)/coverage.info
	lcov --remove $(GCOV_DIR)/coverage.info '/usr/*' --output-file $(GCOV_DIR)/coverage_filtered.info --ignore-errors unused
	genhtml -o $(GCOV_DIR)/report $(GCOV_DIR)/coverage_filtered.info
	@echo "HTML report generated in $(GCOV_DIR)/report"
	@echo "Open $(GCOV_DIR)/report/index.html in your browser to view it"

gcov_clean:
	rm -rf $(GCOV_DIR)

clean: gcov_clean
	rm -f test_runner
	rm -f $(SRC_OBJ) $(TASK5_OBJ)
	rm -f s21_string.a

.PHONY: all clean test s21_string.a gcov_build run_gcov gcov_report gcov_clean
