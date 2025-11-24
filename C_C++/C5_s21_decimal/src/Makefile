# Targets: all, clean, test, s21_decimal.a, gcov_report, valgrind, clang, style, main

GCC = gcc
CFLAGS = -Wall -Werror -Wextra -std=c11
SOURCES = *.c
TESTS_SOURCES = tests/*.c
OBJECTS = $(SOURCES:.c=.o)

# Linux specific flags
CHECKFLAGS = -lcheck -lm -lpthread -lrt -lsubunit
OPEN = xdg-open

all: clean s21_decimal.a

s21_decimal.a:
	$(GCC) $(CFLAGS) $(SOURCES) -c
	ar rcs s21_decimal.a $(OBJECTS)

test: clean s21_decimal.a
	$(GCC) $(CFLAGS) $(TESTS_SOURCES) s21_decimal.a $(CHECKFLAGS) -o s21_decimal
	./s21_decimal

gcov_report: clean s21_decimal.a
	$(GCC) $(CFLAGS) $(TESTS_SOURCES) $(SOURCES) s21_decimal.a $(CHECKFLAGS) -fprofile-arcs -ftest-coverage -lgcov -o s21_decimal
	./s21_decimal
	lcov -t "./s21_decimal" -o report.info --no-external -c -d .
	genhtml -o report report.info
	chmod -R +777 ./report
	$(OPEN) ./report/index.html 2>/dev/null || true

clean:
	rm -rf s21_decimal *.a $(OBJECTS) a.out *.gcno *.gcda report report.info *.dSYM .vscode .clang-format

valgrind: clean test
	valgrind --tool=memcheck --leak-check=yes ./s21_decimal

clang:
	clang-format -n -style=google $(SOURCES) *.h tests/*.c tests/*.h

style:
	cp ../materials/linters/.clang-format .
	clang-format -i -style=google $(SOURCES) *.h tests/*.c tests/*.h

main: clean
	$(GCC) $(CFLAGS) $(SOURCES) $(CHECKFLAGS) -o s21_decimal
	./s21_decimal
