#ifndef FUNCTION_H
#define FUNCTION_H

#include <stdio.h>

#include "getopt.h"
#include "regex.h"
#include "stdlib.h"
#include "string.h"

typedef struct Bayroqlar {
  int e_bayroq;  // -e flagi (bir nechta pattern berish)
  int i_bayroq;  // -i flagi (katta-kichik harflarga farqsiz)
  int v_bayroq;  // -v flagi (mos kelmagan qatorlarni chiqarish)
  int c_bayroq;  // -c flagi (faqat mos kelgan qatorlar sonini chiqarish)
  int l_bayroq;  // -l flagi (faqat fayl nomlarini chiqarish)
  int n_bayroq;  // -n flagi (qator raqamlarini chiqarish)
  int h_bayroq;  // -h flagi (fayl nomini chiqarishni oldini olish)
  int s_bayroq;  // -s flagi (xatoliklarni chiqarishni oldini olish)
  int f_bayroq;  // -f flagi (regexni fayldan olish)
  int o_bayroq;  // -o flagi (faqat mos kelgan qismlarni chiqarish)
} Bayroqlar;

void bayroqlarni_aniqlash(int argc, char **argv, Bayroqlar *bayroqlar,
                          char *regex);
void faylni_chiqarish(int argc, char **argv, Bayroqlar *bayroqlar, char *regex);
int faylni_oqish(char *regex, char *fayl_nomi);
void regexni_topish(Bayroqlar *bayroqlar, char *regex, char *fayl_nomi,
                    int fayllar_soni);
void grep(Bayroqlar *bayroqlar, FILE *fayl, regex_t *comp_regexp,
          char *fayl_nomi, int fayllar_soni);
void bayroqlar_l_c(Bayroqlar *bayroqlar, int line_matches, char *fayl_nomi,
                   int fayllar_soni);
void function_bayroq_n(Bayroqlar *bayroqlar, int fayllar_soni, char *fayl_nomi,
                       int qatorlar_soni, char *matn);
void function_bayroq_v(Bayroqlar *bayroqlar, int fayllar_soni, char *fayl_nomi,
                       char *matn);
void function_bayroq_o(Bayroqlar *bayroqlar, int fayllar_soni, char *fayl_nomi,
                       int qatorlar_soni, regmatch_t *one_match, char *matn);

#endif
