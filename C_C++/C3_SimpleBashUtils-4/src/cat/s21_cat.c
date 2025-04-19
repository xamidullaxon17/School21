#include <getopt.h>
#include <stdio.h>
#include <string.h>

#include "function.h"

int main(int argc, char **argv) {
  Bayroq bayroqlar = {0, 0, 0, 0, 0, 0};

  bayroqlarni_aniqlash(argc, argv, &bayroqlar);
  if (bayroqlar.b_bayroq == 1) bayroqlar.n_bayroq = 0;

  for (int i = optind; i < argc; i++) {
    faylni_oqish(argv[i], &bayroqlar);
  }

  return 0;
}
