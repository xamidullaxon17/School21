CC=gcc
FLAGS= -std=c11  -Wall -Werror -Wextra

all: clean s21_grep

s21_grep:
	$(CC) $(FLAGS) s21_grep.c -o s21_grep function.c

style:
	clang-format --style=Google -i *.c *.h

clean:
	rm -rf s21_grep
rebuild: style all
.PHONY: all clean rebuild