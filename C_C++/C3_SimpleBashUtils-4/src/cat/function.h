#ifndef FUNCTION_H
#define FUNCTION_H
#include <getopt.h>
#include <stdio.h>
#include <string.h>

typedef struct Bayroq {
  int b_bayroq;
  int e_bayroq;
  int n_bayroq;
  int s_bayroq;
  int t_bayroq;
  int v_bayroq;
} Bayroq;

void bayroqlarni_aniqlash(int argc, char **argv, Bayroq *bayroqlar);
void faylni_oqish(char *fayl_nomi, Bayroq *bayroqlar);

#endif