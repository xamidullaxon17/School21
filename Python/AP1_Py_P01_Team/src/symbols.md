# Rogue 1980 — Belgilar Ma'lumotnomasi

## O'yinchi va Muhit

| Belgi | Nomi | Ta'rif |
|-------|------|--------|
| `@` | O'yinchi | Siz boshqaradigan qahramon |
| `#` | Devor | O'tib bo'lmaydi |
| `.` | Pol | Erkin yurish mumkin |
| `>` | Chiqish | Shu belgiga bossangiz keyingi levelga o'tasiz |
| ` ` | Koridor | Xonalarni bog'laydi, yurish mumkin |

## Buyumlar (Items)

| Belgi | Nomi | Nima qiladi | Qanday ishlatiladi |
|-------|------|-------------|-------------------|
| `%` | Ovqat (Food) | HPni tiklaydi (+20..50) | `J` tugmasi |
| `!` | Eliksir | Vaqtincha DEX/STR/MaxHP oshiradi (10 turn) | `K` tugmasi |
| `?` | Scroll | Doimiy ravishda DEX/STR/MaxHP oshiradi | `E` tugmasi |
| `/` | Qurol | Hujum kuchini oshiradi | `H` tugmasi |
| `$` | Xazina | Avtomatik yig'iladi, skorga qo'shiladi | Tegilganda |
| `k` | Kalit | Rangli eshikni ochadi | Tegilganda inventarga tushadi, eshikka borsangiz avtomatik ishlatiladi |

### `%` — Ovqat batafsil
- Ustiga bossangiz **inventarga tushadi**
- `J` tugmasini bosib roʻyxatdan tanlaysiz
- Joriy HP + `health_value` qo'shiladi, lekin `max_health` dan oshib ketmaydi
- Ovqat **sarf bo'ladi** (inventardan yo'qoladi)

## Eshiklar (Bonus Task 6)

| Belgi | Rang | Nima kerak |
|-------|------|-----------|
| `+` (qizil) | Qizil eshik | Qizil kalit `k` |
| `+` (yashil) | Yashil eshik | Yashil kalit `k` |
| `+` (ko'k) | Ko'k eshik | Ko'k kalit `k` |
| `+` (sariq) | Sariq eshik | Sariq kalit `k` |
| `_` | Ochiq eshik | O'tish mumkin |

- Kalit yo'q bo'lsa eshik **bloklanadi** va xabar chiqadi
- Kalit topilsa eshikka borganingizda **avtomatik sarflanadi** va eshik ochiladi

## Dushmanlar

| Belgi | Nomi | Rang | Xususiyati |
|-------|------|------|-----------|
| `z` | Zombie | Yashil | Sekin, baland HP, o'rtacha kuch |
| `v` | Vampire | Qizil | Birinchi zarba doim miss; HP o'g'irlaydi |
| `g` | Ghost | Oq | Tez, ba'zan ko'rinmas bo'ladi |
| `o` | Ogre | Sariq | Xonada 2 qadam/turn; hujumdan keyin 1 turn dam oladi |
| `s` | Snake Mage | Oq | Diagonal harakatlanadi; 30% ehtimol bilan uyutadi |
| `m` | Mimic | Oq | Dastlab `!` ko'rinishida yashirinadi; yaqinlashganda `m` ga aylanadi |

## Boshqaruv

| Tugma | Harakat |
|-------|---------|
| `W A S D` | Harakat (2D) |
| `H` | Qurol tanlash |
| `J` | Ovqat tanlash |
| `K` | Eliksir tanlash |
| `E` | Scroll tanlash |
| `I` | Inventar ko'rish |
| `TAB` | 2D ↔ 3D rejim |
| `ESC` | Menyu (o'yin saqlanadi) |

### 3D rejimda
| Tugma | Harakat |
|-------|---------|
| `W` | Oldinga yur |
| `S` | Orqaga yur |
| `A` | Chapga buril |
| `D` | O'ngga buril |

## Level Ko'tarilish Sharti

`>` belgisi ustiga bossangiz keyingi levelga o'tasiz.  
Level 21 dan o'tsa — **g'alaba**.  
HP 0 ga tushsa — **game over**, natija leaderboardga yoziladi.
