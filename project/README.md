# DO1_Linux

## Part 1: OS o'rnatish

1. **Ubuntu versiyasi `cat /etc/issue` komandasi yordamida tekshirildi.**
    ```sh
    cat /etc/issue
    ```
    - Skrinshot: 
    ![Part 1](pictures/part_1.png)


## Part 2: Foydalanuvchi yaratish

1. **O'rnatish jarayonida yaratilgan foydalanuvchidan tashqari yana bir foydalanuvchi yaratildi.**
    ```sh
    sudo adduser user_1
    sudo usermod -aG adm user_1
    ```
    - Skrinshot: 
    ![adm ga qo'shildi](pictures/part_2.1.png)

2. **Yangi foydalanuvchi `cat /etc/passwd` komandasining natijasida ko'rsatilgan.**
    ```sh
    cat /etc/passwd
    ```
    - Skrinshot: 
    ![Natija](pictures/part_2.png)


## Part 3: Tarmoq sozlamalarini o'rnatish

1. **Mashina nomi `user-1` deb o'rnatildi.**
    ```sh
    sudo hostnamectl set-hostname user_1
    ```
    - Skrinshot: 
    ![Mashina nomi o'zgartirildi](pictures/part_3.1.png)

2. **Vaqt zonasi joriy joylashuvingizga mos ravishda sozlandi.**
    ```sh
    sudo timedatectl set-timezone Asia/Tashkent
    ```
    - Skrinshot: 
    ![Vaqt zonasi sozlash](pictures/part_3.2.png)

3. **Tarmoq interfeyslari nomlari konsol komandasidan chiqarildi.**
    ```sh
    ip link
    ```
    - Skrinshot: 
    ![Tarmoq interfeyslari nomlari](pictures/part_3.3.png)

4. **`lo` interfeysining mavjudligi tushuntirildi.**

    `lo` interfeysi - bu "loopback" interfeysi bo'lib, bu interfeys tarmoq qurilmasining o'zi bilan aloqa qilish uchun mo'ljallangan.

5. **Tarmoq qurilmasining ip manzili DHCP serverdan konsol komandasi yordamida olindi.**
    ```sh
    ip addr
    ```
    - Skrinshot: 
    ![DHCP serverdan ip manzili](pictures/part_3.5.png)

6. **DHCP dekodlandi.**

    DHCP (Dynamic Host Configuration Protocol) - bu tarmoq qurilmalariga avtomatik ravishda IP manzillar va boshqa tarmoq sozlamalarini taqdim etish uchun ishlatiladigan protokol.

7. **Shlyuzning tashqi ip manzili (ip) va ichki ip manzili (gw) aniqlandi va ko'rsatildi.**
    ```sh
    ip route
    curl ifconfig.me
    ```
    - Skrinshot: 
    ![Shlyuz ip manzillari](pictures/part_3.6.png)

8. **Statik (DHCP serverdan olinmagan) ip, gw, dns sozlamalari o'rnatildi.**
    ```sh
    sudo nano /etc/netplan/01-netcfg.yaml
    sudo netplan apply
    ```
    - Skrinshot: 
    ![Statik tarmoq sozlamalari](pictures/part_3.7.png)

9. **1.1.1.1 va ya.ru masofaviy hostlari muvaffaqiyatli ping qilindi va komanda natijasi hisobotga qo'shildi. Komanda natijasida "0% packet loss" iborasi ko'rsatilgan.**
    ```sh
    ping -c 4 1.1.1.1
    ping -c 4 ya.ru
    ```
    - Skrinshot: 
    ![Ping natijasi](pictures/part_3.8.png)


## Part 4: OS yangilash

1. **Tizim paketlari eng so'nggi versiyaga yangilandi.**
    ```sh
    sudo apt update
    sudo apt install -y
    sudo apt dist-upgrade -y
    sudo apt autoremove -y
    sudo apt update
    ```
    - Skrinshot: 
    ![sudo apt update && sudo apt upgrade -y](pictures/part_4.png)
  

## Part 5: Sudo komandasi ishlatilishi

1. **Part 2 da yaratilgan foydalanuvchi orqali OS hostname o'zgartirildi.**
    ```sh
    sudo usermod -aG sudo user_1
    sudo hostnamectl set-hostname xamid
    hostnamectl
    ```
    - Skrinshot: 
    ![Hostname o'zgartirilgan](pictures/part_5.png)


## Part 6: Vaqt xizmatini o'rnatish va sozlash

1. **Avtomatik vaqt sinxronizatsiyasi xizmati o'rnatildi va sozlandi.**
    ```sh
    sudo apt update
    sudo apt istall systemd-timesynd -y

    sudo systemctl enable systemd-timesyncd
    sudo systemctl start systemd-timesyncd

    sudo systemctl status systemd-timesyncd
    ```

2. **Hozirgi joylashuvingiz bo'yicha vaqt zonasi vaqti chiqarildi.**
    ```sh
    sudo timedatectl set-timezone Asia/Tashkent
    timedatectl
    ```
    - Skrinshot: 
    ![Vaqt zonasi vaqti](pictures/part_6.png)

3. **`timedatectl show` komandasi natijasi.**
    ```sh
    timedatectl show
    ```
    - Skrinshot: 
    ![timedatectl show](pictures/part_6.1.png)


## Part 7: 

## Matn muharrirlarini o'rnatish va ishlatish

1. **VIM, NANO, va MCEDIT matn muharrirlari o'rnatildi.**
    ```sh
    sudo apt update
    sudo apt install vim nano joe -y
    ```

2. **Har bir muharrirda test_X.txt fayli yaratildi va nik kiritildi, keyin fayl saqlandi.**
    - VIM muharririda fayl:
      - Komanda: vim test_emperora.txt
      - Insert rejimiga o'tish: i
      - Nickname yozish: emperora
      - Command rejimiga qaytish: Esc
      - Faylni saqlash va chiqish: :wq
    - Skrinshot: 
    ![emperora fayli](pictures/part_7.1_vim.png)

    - NANO muharririda fayl:
      - Komanda: nano test_emperora.txt
      - Matnni yozish: emperora
      - Saqlash va chiqish: Ctrl+O, Enter, Ctrl+X
    - Skrinshot: 
    ![emperora fayli](pictures/part_7.4_nano.png)

    - MCEDIT muharririda fayl:
      - Komanda: mcedit test_empeora.txt
      - Matnni yozish: emperora
      - Saqlash va chiqish: F2, F10
    - Skrinshot: 
    ![emperora fayli](pictures/part_7.7_mcedit.png)

3. **Har bir muharrirda faylni tahrirlash va "21 School 21" qatoriga almashtirish, keyin faylni saqlamasdan chiqish amalga oshirildi.**
    - VIM muharririda fayl:
      - Komanda: vim test_emperora.txt
      - Insert rejimiga o'tish: i
      - Matnni o'zgartirish: emperora dan 21 School 21 ga o'zgartirish.
      - Command rejimiga qaytish: Esc
      - Saqlamasdan chiqish: :q!
    - Skrinshot: 
    ![emperora tahrirlangan](pictures/part_7.2_vim.png)

    - NANO muharririda fayl:
      - Komanda: nano test_emperora.txt
      - Matnni o'zgartirish: emperora dan 21 School 21 ga o'zgartirish.
      - Saqlamasdan chiqish: Ctrl+X, N
    - Skrinshot: 
    ![emperora tahrirlangan](pictures/part_7.6_nano.png)

    - MCEDIT muharririda fayl:
      - Komanda: mcedit test_emperora.txt
      - Matnni o'zgartirish: emperora dan 21 School 21 ga o'zgartirish.
      - Saqlamasdan chiqish: F10, N
      - O'zgartirilgan matn: 21 School 21
    - Skrinshot: 
    ![emperora tahrirlangan](pictures/part_7.8_mcedit.png)

4. **Har bir muharrirda fayl ichidagi so'zlarni qidirish va almashtirish funksiyalari o'rganildi va amalga oshirildi.**
    - VIM muharririda qidirish va almashtirish:
      - Komanda: vim test_emperora.txt
      - Qidirish rejimi: /emperora
      - Almashtirish: :%s/emperora/xamidullaxon/g
      - Screenshot:
      - Qidirilgan so'z: emperora
      - Almashtirilgan so'z: xamidullaxon
    - Skrinshot: 
    ![VIM so'z almashtirish](pictures/part_7.3_vim.png)

    - NANO muharririda qidirish va almashtirish:
      - Komanda: nano test_emperora.txt
      - Qidirish: Ctrl+W, your_nickname
      - Almashtirish: Ctrl+\, emperora, enter, xamidullaxon
      - Qidirilgan so'z: emperora
      - Almashtirilgan so'z: xamidullaxon
    - Skrinshot: 
    ![NANO so'z almashtirish](pictures/part_7.5_nano.png)

    - MCEDIT muharririda qidirish va almashtirish:
      - Komanda: mcedit test_emperora.txt
      - Qidirish: F7, emperora, Enter
      - Almashtirish: F4, emperora, xamidullaxon, Enter
      - Qidirilgan so'z: emperora
      - Almashtirilgan so'z: xamidullaxon
    - Skrinshot: 
    ![MCEDIT so'z almashtirish](pictures/part_7.9_mcedit.png)


## Part 8: SSHD xizmatini o'rnatish va asosiy sozlash

1. **SSHD xizmati o'rnatildi va tizim yuklanishida avtomatik ishga tushirilishi qo'shildi.**
    - SSHD xizmati o'rnatilishi:
      ```sh
      sudo apt update
      sudo apt install openssh-server
      sudo systemctl enable ssh
      ```

2. **SSHD xizmatining porti 2022 ga o'zgartirildi.**
    - Buning uchun `/etc/ssh/sshd_config` fayli tahrir qilindi va `Port 2022` qatori qo'shildi:
      ```sh
      sudo nano /etc/ssh/sshd_config
      ```
    - O'zgartirishlar saqlandi va SSHD xizmati qayta ishga tushirildi:
      ```sh
      sudo systemctl restart ssh
      ```

3. **PS komandasidan foydalangan holda SSHD jarayonining mavjudligi ko'rsatildi.**
      ```sh
      ps aux | grep sshd
      ```

4. **PS komandasining va har bir kalitning ma'nosi tushuntirildi.**
    - `ps`: Jarayonlarni ko'rsatish.
    - `aux`: Har qanday foydalanuvchi (a), uy vazifalari (u), kengaytirilgan formatda (x).

5. **`netstat -tan` komandasi natijasi quyidagi satrni o'z ichiga olishi kerak:**
    - `tcp 0 0.0.0.0:2022 0.0.0.0:* LISTEN`
      ```sh
      netstat -tan
      ```
    - Skrinshot: 
    ![netstat natijasi](pictures/part_8.png)

6. **`-tan` kalitlarining ma'nosi va chiqish ustunlarining qiymatlari tushuntirildi.**
    - `-t`: TCP protokoli.
    - `-a`: Barcha portlar.
    - `-n`: Port nomlari o'rniga raqamlarni ko'rsatish.
    - Ustunlar:
      - `tcp`: Protokol turi.
      - `0 0.0.0.0:2022`: Mahalliy manzil va port.
      - `0.0.0.0:*`: Uzoq manzil va port.
      - `LISTEN`: Holat.
      - `0.0.0.0`: Har qanday IP manzildan ulanishni qabul qilish.


## Part 9: Top va htop utilitilarini o'rnatish va ishlatish

1. **Top va htop utilitilari o'rnatildi va ishga tushirildi.**
    ```sh
    sudo apt update
    sudo apt install procps -y
    sudo apt install htop -y
    ```

2. **Top komandasining natijasidan quyidagilar aniqlandi:**
    - Uptime (tizim ish vaqti)
    - Foydalanuvchilar soni
    - O'rtacha tizim yuklanishi
    - Umumiy jarayonlar soni
    - CPU yuklanishi
    - Xotira yuklanishi
    - Eng ko'p xotira foydalanayotgan jarayon PIDi
    - Eng ko'p CPU vaqti olgan jarayon PIDi

    Skrinshotlar:
    - Uptime va boshqa ma'lumotlar ko'rsatilgan: 
    ![Top natijasi](pictures/part_9_top.png)

3. **Htop komandasining natijasi quyidagi shartlarga mos keladi:**
    Skrinshotlar:
    - PID bo'yicha saralash: 
    ![Htop natijasi - PID](pictures/part_9_PID.png)
    - CPU foizi bo'yicha saralash: 
    ![Htop natijasi - CPU](pictures/part_9_CPU.png)
    - Xotira foizi bo'yicha saralash: 
    ![Htop natijasi - MEM](pictures/part_9_MEM.png)
    - Vaqt bo'yicha saralash: 
    ![Htop natijasi - TIME](pictures/part_9_TIME.png)
    - sshd jarayoni uchun filtrlangan: 
    ![Htop natijasi - SSHD](pictures/part_9_sshd.png)
    - Syslog jarayoni qidirilgan: 
    ![Htop natijasi - SYSLOG](pictures/part_9_syslog.png)
    - Tizim nomi, soat va uptime chiqarilgan: 
    ![Htop natijasi - HOSTNAME](pictures/part_9_hostname_time_uptime.png)


## Part 10: Fdisk utilitidan foydalanish

1. **Fdisk utilitidan foydalanib, qattiq disk haqida ma'lumot olindi.**
    ```sh
    sudo fdisk -l
    ```
    - **Hard disk:** `/dev/sda`
    - **Capacity:** `25 GB`
    - **Sectors:** `52428800`
    - **Swap size:** `25 GB` or `0`
    - Skrinshot: 
    ![Fdisk natijasi](pictures/part_10.png)


## Part 11: df utilitidan foydalanish

1. **df komandasini ishga tushirish:**
    ```sh
    df -h
    ```
    **Root bo'limi (`/`) bo'yicha ma'lumotlar:**
    - **Size:** 25G
    - **Used:** 3.2G
    - **Avail:** 20G
    - **Used:** 14%
    - **Measure:** Gigabayt (G)
    - **Mounted:** on

2. **df -Th komandasini ishga tushirish:**
    ```sh
    df -Th /
    ```
    **Root bo'limi (`/`) bo'yicha ma'lumotlar:**
    - **Size:** 25G
    - **Used:** 3.2G
    - **Free:** 20G
    - **Used %:** 14%
    - **File System Type:** ext4
    - **Mounted** on


## Part 12: ## du utilitidan foydalanish

1. **du komandasini ishga tushirish:**

2. **/home, /var, /var/log papkalarining hajmi (baytlarda, inson tomonidan o'qilishi mumkin formatda):**
    ```sh
    du -sh /home /var /var/log
    ```
    - Skrinshot: 
    ![du natijasi - asosiy papkalar](pictures/part_12.png)

3. **/var/log papkasidagi barcha tarkib hajmi (umumiy emas, har bir kirish elementining hajmi):**
    ```sh
    sudo du -sh /var/log/*
    ```
    - Skrinshot: 
    ![du natijasi - var log](pictures/part_12.png)


## Part 13: ncdu utilitidan foydalanish

1. **ncdu utiliti o'rnatildi va ishga tushirildi.**
    ```sh
    sudo apt update
    sudo apt install ncdu
    ```

2. **/home, /var, /var/log papkalarining hajmi aniqlandi.**
    ```sh
    ncdu /home
    ncdu /var
    ncdu /var/log
    ```
    - Skrinshot: 
    ![ncdu natijasi - home](pictures/part_13.1.png)
    ![ncdu natijasi - var](pictures/part_13.2.png)
    ![ncdu natijasi - var log](pictures/part_13.3.png)


## Part 14: Tizim loglari bilan ishlash

1. **/var/log/dmesg, /var/log/syslog va /var/log/auth.log fayllari ko'rib chiqildi.**
    ```sh
    sudo less /var/log/dmesg
    sudo less /var/log/syslog
    sudo less /var/log/auth.log
    ```

2. **Oxirgi muvaffaqiyatli login vaqti, foydalanuvchi nomi va login usuli yozildi:**
    - **Login time:** 2024-12-25T15:02:32.310667+00:00
    - **User name:** xamidullaxon
    - **login method:** TTY=tty1

3. **SSHD xizmati qayta ishga tushirildi.**
    ```sh
      sudo systemctl restart ssh
    ```
    - Skrinshot: 
    ![SSHD qayta ishga tushirilishi](pictures/part_14.png)


## Part 15: CRON job rejalashtirgichidan foydalanish

1. **Job rejalashtirgich yordamida har 2 daqiqada `uptime` komandasini ishga tushirish sozlandi.**
    - Buning uchun cron ishlarini tahrirlash:
      ```sh
      crontab -e
      ```
    - Quyidagi qator qo'shildi:
      ```sh
      */2 * * * * /usr/bin/uptime >> /home/user1/uptime.log
      ```
    - Skrinshot:
    ![CRON bajarilish qatorlari](pictures/part_15.1.png)

2. **Job rejalashtirgichdan barcha ishlar olib tashlandi:**
    - CRON joriy ishlar ro'yxati:
      ```sh
      crontab -l
      ``` 
    - crontabni barcha qatorlarni o'chirish:
      ```sh
      crontab -r
      ```

    - Skrinshot:
    ![Bo'sh CRON joriy ishlar ro'yxati](pictures/part_15.2.png)