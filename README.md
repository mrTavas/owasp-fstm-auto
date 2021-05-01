# OWASP-FSTM-Auto
![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg?style=plastic)

Цель данного проекта - повысить эффективность методологии выявления уязвимостей в прошивках IoT устройств [OWASP FSTM](https://scriptingxss.gitbook.io/firmware-security-testing-methodology/) путем ее оптимизации и автоматизации.

---
### Этапы 1, 2. Сбор информации и получение прошивки
1. Сбор информации. На данном этапе изучается техническая документация, инструкции.

2. Получение прошивки. Прошивка может быть получена следующими способами: от команды разработчиков или клиента, может быть собрана с нуля, с использованием инструкции от производителя, может быть получена  с сайта производителя, может быть извлечена напрямую из аппаратного обеспечения через UART, JTAG, PICit и т.д. 

Данные этапы не затрагиваются.

---
### Этапы 3 и 4. Анализ прошивки и ее извлечение

Анализ прошивки устройства подразуменвать определение процессорной архитектуры, определение типа файловой системы, а также проверку энтропии файла прошивки. За автоматизацию этого процесса отвечет [данный модуль](https://github.com/mrTavas/owasp-fstm-auto/blob/main/stage3_Analyzing_firmware.py).

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





