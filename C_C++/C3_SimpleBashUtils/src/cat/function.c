#include "function.h"

void bayroqlarni_aniqlash(int argc, char **argv, Bayroq *bayroqlar) {
  int bayroq;
  static struct option options[] = {{"number-nonblank", 0, 0, 'b'},
                                    {"number", 0, 0, 'n'},
                                    {"squeeze-blank", 0, 0, 's'}};
  while ((bayroq = getopt_long(argc, argv, "benstvET", options, NULL)) != -1) {
    if (bayroq == 'b') bayroqlar->b_bayroq = 1;
    if (bayroq == 'E') bayroqlar->e_bayroq = 1;
    if (bayroq == 'n') bayroqlar->n_bayroq = 1;
    if (bayroq == 's') bayroqlar->s_bayroq = 1;
    if (bayroq == 'T') bayroqlar->t_bayroq = 1;
    if (bayroq == 'v') bayroqlar->v_bayroq = 1;
    if (bayroq == 'e') {
      bayroqlar->e_bayroq = 1;
      bayroqlar->v_bayroq = 1;
    }
    if (bayroq == 't') {
      bayroqlar->t_bayroq = 1;
      bayroqlar->v_bayroq = 1;
    }
  }
}

void faylni_oqish(char *fayl_nomi, Bayroq *bayroqlar) {
  FILE *fayl = fopen(fayl_nomi, "r");

  if (fayl != NULL) {
    int sanash = 1;
    int bosh_qator = 0;
    int oxirgi_char = '\n';
    int ch;

    while ((ch = fgetc(fayl)) != EOF) {
      if (bayroqlar->s_bayroq && ch == '\n' && oxirgi_char == '\n') {
        bosh_qator++;
        if (bosh_qator > 1) {
          continue;
        }
      } else {
        bosh_qator = 0;
      }
      if (oxirgi_char == '\n' &&
          ((bayroqlar->b_bayroq && ch != '\n') || bayroqlar->n_bayroq))
        printf("%6d\t", sanash++);
      if (bayroqlar->e_bayroq && ch == '\n') printf("%c", '$');
      if (bayroqlar->t_bayroq && ch == '\t') {
        printf("%c", '^');
        ch = 'I';
      }
      if (bayroqlar->v_bayroq) {
        if (ch < 32 && ch != '\n' && ch != '\t') {
          printf("^");
          ch += 64;
        }
        if (ch == 127) {
          printf("^");
          ch = '?';
        }
        if (ch > 127) {
          printf("M-");
          ch -= 128;
        }
      }
      printf("%c", ch);
      oxirgi_char = ch;
    }
    fclose(fayl);
  } else {
    fprintf(stderr, "cat: %s: Bu fayl topilmadi\n", fayl_nomi);
  }
}
