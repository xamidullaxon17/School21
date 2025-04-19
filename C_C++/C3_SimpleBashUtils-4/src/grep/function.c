#include "function.h"

void bayroqlarni_aniqlash(int argc, char **argv, Bayroqlar *bayroqlar,
                          char *regexp) {
  int bayroq;

  while ((bayroq = getopt(argc, argv, "e:ivclnhsf:o")) != -1) {
    if (bayroq == 'e') {
      bayroqlar->e_bayroq = 1;
      if (*regexp != '\0') {
        strcat(regexp, "|");
      }
      strcat(regexp, optarg);
    }
    if (bayroq == 'i') bayroqlar->i_bayroq = 1;
    if (bayroq == 'v') bayroqlar->v_bayroq = 1;
    if (bayroq == 'c') bayroqlar->c_bayroq = 1;
    if (bayroq == 'l') bayroqlar->l_bayroq = 1;
    if (bayroq == 'n') bayroqlar->n_bayroq = 1;
    if (bayroq == 'h') bayroqlar->h_bayroq = 1;
    if (bayroq == 's') bayroqlar->s_bayroq = 1;
    if (bayroq == 'f') {
      bayroqlar->f_bayroq = 1;
      faylni_oqish(regexp, optarg);
    }
    if (bayroq == 'o') bayroqlar->o_bayroq = 1;
  }
}

void faylni_chiqarish(int argc, char **argv, Bayroqlar *bayroqlar,
                      char *regex) {
  if (!bayroqlar->f_bayroq && !bayroqlar->e_bayroq)
    sprintf(regex, "%s", argv[optind++]);
  int fayllar_soni = argc - optind;
  for (int i = optind; i < argc; i++) {
    if ((bayroqlar->v_bayroq && bayroqlar->o_bayroq &&
         (bayroqlar->c_bayroq || bayroqlar->l_bayroq)) ||
        !(bayroqlar->v_bayroq && bayroqlar->o_bayroq)) {
      regexni_topish(bayroqlar, regex, argv[i], fayllar_soni);
    }
  }
}

int faylni_oqish(char *regex, char *fayl_nomi) {
  FILE *fayl = fopen(fayl_nomi, "r");
  if (*regex != '\0') {
    strcat(regex, "|");
  }
  int index = strlen(regex);
  if (fayl != NULL) {
    int c;
    while ((c = fgetc(fayl)) != EOF) {
      if (c == 13 || c == 10) regex[index++] = '|';
      if (c != 13 && c != 10) regex[index++] = c;
    }

    if (regex[index - 1] == '|') regex[index - 1] = '\0';
    fclose(fayl);
  }
  return index + 1;
}

void regexni_topish(Bayroqlar *bayroqlar, char *regex, char *fayl_nomi,
                    int fayllar_soni) {
  int regcomp_bayroqlar =
      (bayroqlar->i_bayroq) ? REG_ICASE | REG_EXTENDED : REG_EXTENDED;
  regex_t comp_regexp;
  FILE *fayl = fopen(fayl_nomi, "r");
  if (fayl != NULL) {
    regcomp(&comp_regexp, regex, regcomp_bayroqlar);
    grep(bayroqlar, fayl, &comp_regexp, fayl_nomi, fayllar_soni);
    regfree(&comp_regexp);
    fclose(fayl);
  }
}

void grep(Bayroqlar *bayroqlar, FILE *fayl, regex_t *comp_regexp,
          char *fayl_nomi, int fayllar_soni) {
  char matn[4097] = {0};
  regmatch_t one_match[1];
  int line_matches = 0, qatorlar_soni = 1;

  while (fgets(matn, 4096 - 1, fayl) != NULL) {
    int status = regexec(comp_regexp, matn, 1, one_match, 0);
    int match = 0;
    int uzunlik = strlen(matn);
    if (matn[uzunlik - 1] != '\n') {
      matn[uzunlik] = '\n';
      matn[uzunlik + 1] = '\0';
    }
    if (status == 0 && !bayroqlar->v_bayroq) match = 1;
    if (status == REG_NOMATCH && bayroqlar->v_bayroq) match = 1;
    if (match) {
      function_bayroq_n(bayroqlar, fayllar_soni, fayl_nomi, qatorlar_soni,
                        matn);
      function_bayroq_v(bayroqlar, fayllar_soni, fayl_nomi, matn);
      function_bayroq_o(bayroqlar, fayllar_soni, fayl_nomi, qatorlar_soni,
                        one_match, matn);
    }
    line_matches += match;
    qatorlar_soni++;
  }
  bayroqlar_l_c(bayroqlar, line_matches, fayl_nomi, fayllar_soni);
}

void bayroqlar_l_c(Bayroqlar *bayroqlar, int line_matches, char *fayl_nomi,
                   int fayllar_soni) {
  if (bayroqlar->l_bayroq && line_matches > 0) printf("%s\n", fayl_nomi);
  if (bayroqlar->c_bayroq && !bayroqlar->l_bayroq) {
    if (fayllar_soni > 1 && !bayroqlar->h_bayroq) {
      printf("%s:%d\n", fayl_nomi, line_matches);
    } else {
      printf("%d\n", line_matches);
    }
  }
}

void function_bayroq_n(Bayroqlar *bayroqlar, int fayllar_soni, char *fayl_nomi,
                       int qatorlar_soni, char *matn) {
  if (!bayroqlar->l_bayroq && !bayroqlar->c_bayroq && !bayroqlar->o_bayroq &&
      bayroqlar->n_bayroq) {
    if (fayllar_soni > 1 && !bayroqlar->h_bayroq) {
      printf("%s:", fayl_nomi);
    }
    printf("%d:%s", qatorlar_soni, matn);
  }
}

void function_bayroq_v(Bayroqlar *bayroqlar, int fayllar_soni, char *fayl_nomi,
                       char *matn) {
  if (!bayroqlar->l_bayroq && !bayroqlar->c_bayroq && !bayroqlar->n_bayroq &&
      !bayroqlar->o_bayroq) {
    if (fayllar_soni > 1 && !bayroqlar->h_bayroq && !bayroqlar->o_bayroq) {
      printf("%s:", fayl_nomi);
    }
    printf("%s", matn);
  }
}

void function_bayroq_o(Bayroqlar *bayroqlar, int fayllar_soni, char *fayl_nomi,
                       int qatorlar_soni, regmatch_t *one_match, char *matn) {
  if (bayroqlar->o_bayroq && !bayroqlar->c_bayroq) {
    if (fayllar_soni > 1 && !bayroqlar->h_bayroq) {
      printf("%s:", fayl_nomi);
    }
    if (bayroqlar->n_bayroq) {
      printf("%d:", qatorlar_soni);
    }
    for (int i = one_match[0].rm_so; i < one_match[0].rm_eo; i++) {
      printf("%c", matn[i]);
    }
    printf("\n");
  }
}