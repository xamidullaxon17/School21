CFLAGS = -Wall -Werror -Wextra -std=c11
CFILES = $(wildcard s21_*.c)
OFILES = $(patsubst %.c,%.o, ${CFILES})
TESTS_CFILES = tests/*.c

LIB_FLAGS = -lcheck -lsubunit -lm
OPEN = xdg-open
CHMOD = chmod -R +777 ./report/

all: s21_matrix.a

s21_matrix.a: ${CFILES}
	gcc -c $(CFLAGS) $(LIB_FLAGS) $(CFILES)
	ar rcs $@ $(OFILES)
	ranlib s21_matrix.a
	-rm -rf *.o

test: s21_matrix.a
	gcc $(CFLAGS) -o test $(TESTS_CFILES) s21_matrix.a $(LIB_FLAGS) 
	./test

gcov_report:${CFILES}
	gcc --coverage ${CFILES} ${TESTS_CFILES} -o test $(LIB_FLAGS)
	./test
	gcov ${CFILES}
	lcov -t "s21_test" -o s21_test.info -c -d .
	genhtml -o report s21_test.info
	$(CHMOD)
	$(OPEN) ./report/index.html

clean:
	-rm -rf *.o *.gcda *.gcno *.gcov *result coverage.info s21_test.info s21_matrix.a test report

git_prepare: clang_i s21_matrix.a test valg clean

clang_i:
	clang-format -i -style=Google ${CFILES} ${TESTS_CFILES} *.h

clang_n:
	clang-format -i -style=Google ${CFILES} ${TESTS_CFILES} *.h

clean_gcov:
	-rm -rf *.o *.gcda *.gcno *.gcov *result coverage.info s21_test.info s21_matrix.a test

valg:
	valgrind --tool=memcheck --leak-check=yes --track-origins=yes --leak-check=full --show-leak-kinds=all -s ./test

.PHONY: all s21_matrix.a test gcov_report clean
