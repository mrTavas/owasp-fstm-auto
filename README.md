# OWASP-FSTM-Auto
![Python 3.6](https://img.shields.io/badge/Python-3.6-green.svg?style=plastic)
![OS](https://img.shields.io/badge/OS-GNU%2FLinux-000000.svg?style=plastic)
[![OWASP Flagship](https://img.shields.io/badge/OWASP-FSTM-blue.svg?style=plastic)](https://scriptingxss.gitbook.io/firmware-security-testing-methodology/)

Цель данного проекта - повысить эффективность методологии выявления уязвимостей в прошивках IoT устройств [OWASP FSTM](https://scriptingxss.gitbook.io/firmware-security-testing-methodology/) путем ее оптимизации и автоматизации.

---
### Этапы 1, 2. Сбор информации и получение прошивки
1. Сбор информации. На данном этапе изучается техническая документация, инструкции.

2. Получение прошивки. Прошивка может быть получена следующими способами: от команды разработчиков или клиента, может быть собрана с нуля, с использованием инструкции от производителя, может быть получена  с сайта производителя, может быть извлечена напрямую из аппаратного обеспечения через UART, JTAG, PICit и т.д. 

Данные этапы не затрагиваются.

---
### Этапы 3 и 4. Анализ прошивки и ее извлечение

Анализ прошивки устройства подразумевает определение процессорной архитектуры, определение типа файловой системы, а также проверку энтропии файла прошивки. За автоматизацию этого процесса отвечет [данный модуль](https://github.com/mrTavas/owasp-fstm-auto/blob/main/stage3_Analyzing_firmware.py).

Для извлечения файловой системы OWASP рекомендует использовать [Binwalk](https://github.com/ReFirmLabs/binwalk) или [Firmware Mod Kit](https://github.com/rampageX/firmware-mod-kit/wiki). Для определения наиболее оптимального инструмента был проведен эксперемент по сравнению данных инструментов.


| Filesystem     | Architecture |        Firmware                                    |  Binwalk |Firmware mod kit |
|:--------------:|:------------:|:--------------------------------------------------:|:--------:|:---------------:|
|Squashfs        | ARM          |Damn Vulnerable Router Firmware(DVRF)v0.3           | 0m 11,2s | 0m 33,8s
|Squashfs        | MIPS         |DLink-DIR 823A1 v1.00                               | 0m 9,8s  | 0m 20,9s
|Squashfs        | ARM          | DLink-DIR 629 A1-FWv1.03(for DCN)                  | 0m 9,7s  | 0m 10,9s
|Squashfs        | ARM          | DLink-DIR 816 A2_FWv1.10(for DCN)                  | 0m 9,2s  | 0m 10,9s
|Squashfs        | ARM          | DLink-DIR 859 A3-FWv1.05                           | 0m 11,5s | 0m 13,1s
|Squashfs        | ARM          | DLink-DIR 629 B1-FWv2.01                           | 0m 9,9s  | 0m 13,1s
|Squashfs        | ARM          | TP-Link wr941nv4 en_3_12_8_up (110117)             | 0m 11,2s | 0m 28,1s
|Squashfs        | MIPS         | TP-Link wr940nv4 us_3_16_9_up_boot (160617)        | 0m 10,1s |0m 19,1s
|Romfs           | ARM          | IP-камера Foscam-FI8908W(lr_cmos_11_14_1_46)       | 0m 9, 2s | No supported
|Romfs           | ARM          | Go Pro-Hero7(black-1.9-firmware)                   | 8m 35,6s | No supported
|Jffs2           | MIPS         | Netgear-DGN2200v4-V1.0.0.116_1.0.116               | 1m 2,9s  | 1m 17,9s
|Jffs2           | MIPS         | Netgear-DGN2200M-V1.0.0.26                         | 0m 45,1s | 0m 49,8s
|Ubifs           | ARM          | Openwrt-19.07.7 oxnas-ox820 akitio mycloud         | 0m 25,5s | No supported
|Ubifs           | ARM          | 8devices-Rambutan(factory-to-ddwrt)                | 2m 49,5s | No supported
|Cramfs          | ARM          | Hangzhou Xiongmai DVR-MBD6016E-E_V4                | 0m 5,7s  | 0m 14,6s
|Cramfs          | ARM          | Polyvision PVDR (16WDS2_revD_AHB7016T LM_V4.02)    | 0m 6,1s  | 0m 14,9s
|Cramfs          | ARM          | Optimus NBD6308T (PL_V4.02)                        | 0m 5,6s  | 0m 14,4s

- По результатом очевидно, что использование binwalk наиболее оптимально. Также при ошибке автоматического извлечения файловой системы был реализован алгоритм альтернативного способа извлечения.

![Иллюстрация к проекту](https://github.com/mrTavas/owasp-fstm-auto/blob/main/artwork/Extr-filesys.png?raw=true)

- За автоматизацию извлечения файловой сисмемы отвечает [данный модуль](https://github.com/mrTavas/owasp-fstm-auto/blob/main/stage4_Extracting_filesystem.py). 

---
### Этап 5. Анализ файловой системы

В ходе этапа анализа файловой системы необходимо автоматизировать поиск устаревших небезопасных сервисов, поиск в CVE-базах и Exploit-базах по версиям найденных сервисов, поиск жестко закодированных учетных данных (имена пользователей, пароли, ключи API, ключи SSH), функционал обновления прошивки, который может использоваться в качестве точки входа.

---
### Этап 6. Эмуляция прошивки

Для полной эмуляции прошивок, OWASP рекомендует использовать Firmware-analysis-toolkit, Arm-x или Qiling. По результатам проведенных в данном проекте исследованиям, для прошивок с arm архитектурой оптимально использовать Arm-x, а для Mips оптимальнее эмулятор Qiling. Ниже представлена таблица с результатами эксперимента.

| Firmware       | Architecture |        FAT %CPU  |  ARM-X %CPU | Qiling %CPU |
|:--------------:|:------------:|:----------------:|:-----------:|:---------------:|
| Tenda AC15 Wi-Fi Router(V15.03.05.18_multi_TD01) | arm (armel) | 49,7 | 32,5 | 49,6
| ARcher C9 Wi-Fi Router(V5_190403) | arm (armel) | 50,2 | 29,9 | 48,7
| IP Camera Trivision NC-277 WF(V4.50B20140101) | arm (armel) | 43,8 | 29,1 | 44,9
| Asus RT-AC1900P(3.0.0.4_384_32738-gc9a116a) | arm (armel) | 57,5 | 40,3 | 58,4
| RV160W Wireless-AC VPN-Router | arm (armel) | 63,1 | 41,7 | 64
| IoTGoat-raspberry-pi2(v1.0) | arm (armel) | 41,2 | 30,9 | 40,3
| IP-камера Foscam FI8908W(lr_cmos_11_14_1_46) | arm (armel) | 38,7 | 29,8 | 38
| TP-Link TL-WR941ND v4_en_3_12_8_up) | mips (mipseb) | 24,7 | null | 25,9
| Netgear DGN2200(v4-V1.0.0.116_1.0.116) | mips (mipseb) | 30,8 | null | 29,3
| DLink DIR-823(A1-v1.00) | mips (mipseb) | 32,8 | null | 30,6
| Netgear Wnap320(Version 2.0.3) | mips (mipseb) | 23,5 | null | 20,4
| IP Camera DLink-DCS-5010(L-1.13.05) | mips (mipseb) | 24,3 | null | 20,1
| Linksys E1200(v2.0.7) | mips (mipsel) | 39,4 | null | 38,9
| Keenetic Start KN-1111(stable_3.04.C.12.0-0) | mips (mipsel) | 28,2 | null | 26,8

##### Визуализация (Arm):
![Иллюстрация к проекту](https://github.com/mrTavas/owasp-fstm-auto/blob/main/artwork/Emul-Arm.png?raw=true)
##### Визуализация (Mips):
![Иллюстрация к проекту](https://github.com/mrTavas/owasp-fstm-auto/blob/main/artwork/Emul-Mips.png?raw=true)

---
### Этап 7. Динамический анализ

Для фаззинг тестирования прикладных сервисов OWASP рекомендует использовать следующие фаззеры:
- American fuzzy lop
- FIRM-AFL
- Firmcorn

В целях оптимизации, был проведен эксперимент для определения наиболее оптимального решения для прошивок IoT устройств. Результаты эксперимента представленны в таблице ниже. По полученным данным, наиболее оптимальным решением является Firmcorn, который в среднем может обечпечить увеличение скорости фаззинг тестирования на 13-20%.

| Firmware       | Service      |   Vulnerability  |  AFL (qemu mode) | Firm-AFL | Firmcorn
|:--------------:|:------------:|:----------------:|:-----------:|:---------------:|:------:|
| TP-Link WR940N(V4) | httpd | Buffer Overflow | >24h | >24h | 7h 31m
| TP-Link WR941N(V4) | httpd | Buffer Overflow | >24h | 20h 41m | 8h 05m
| DLink DIR-850L(V1.03) | hnap | Buffer Overflow | 7h 52m | 3h 14m | 2h 33m
| IP Camera Trendnet TV-IP110WN(V.1.2.2) | video.cgi | Buffer Overflow | 7h 59m | 4h 39m | 4h 28m
| D-Link DIR-825(V2.02) | httpd | Buffer Overflow | >24h | 22h 57m | 18h 44m
| D-Link DAP-2695(V1.11) | httpd | Buffer Overflow | 3h 09m | 2h 46m | 3h 17m
| IP CameraTrendnet TV-IP110WN(V.1.2.2) | network.cgi | Buffer Overflow | 20h 40m | 8h 19m | 7h 50m


##### Визуализация:
![Иллюстрация к проекту](https://github.com/mrTavas/owasp-fstm-auto/blob/main/artwork/Dyn-Fuzzers.png?raw=true)
