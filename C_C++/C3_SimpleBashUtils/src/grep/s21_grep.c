#include "function.h"

int main(int argc, char **argv) {
  Bayroqlar bayroqlar = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  char regexp[4096] = {0};
  bayroqlarni_aniqlash(argc, argv, &bayroqlar, regexp);

  if (argc >= 3) {
    faylni_chiqarish(argc, argv, &bayroqlar, regexp);
  }
  return 0;
}
