CC=gcc
FLAGS= -std=c11 -Wall -Werror -Wextra

all: clean s21_cat

s21_cat:
	$(CC) $(FLAGS) s21_cat.c -o s21_cat function.c

style:
	clang-format --style=Google  -i *.c *.h

clean:
	rm -rf s21_cat
rebuild: style all
.PHONY: all clean rebuild