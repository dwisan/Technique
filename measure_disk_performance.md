>งานระบบฐานข้อมูล นอกเหนือจากหน่วยประมวลผล (CPU Core) และหน่วยความจำ (Memory) จะเพียงพอหรือไม่แล้ว
สิ่งหนึ่งที่ควรคำนึงด้วยนั่นคือ disk performance ในการอ่านและเขียนต่อหน่วยเวลาเป็นวินาที หรือที่เรียกกันว่า IOPS
(Input Output Per Second) เนื่องจากระบบฐานข้อมูลที่มีการใช้งานพร้อมๆ กันจำนวนมาก IOPS ของ disk อาจจะ
ไม่เพียงพอต่องานที่เกิดขึ้นได้ ดังนั้นในการจัดทำเซิฟเวอร์สำหรับบริการระบบฐานข้อมูล จำเป็นต้องมีการทดสอบหาความสามารถ
ของ disk เพื่อให้ทราบถึงขีดความสามารถในการรองรับงานด้วย 

[x] fio (flexible I/O tester) สำหรับทดสอบหาค่า IOPS 
[X] ioping ทดสอบหาค่า latency

ref: https://fio.readthedocs.io/en/latest/fio_doc.html

>Install fio
```bash
[x] CentOS,RHEL
# yum install epel-release -y
# yum install fio

[x] Ubuntu
# apt install fio
```
>Testing IOPS with fio
```
[x] RW Performance (Read-Write Testing)

# fio --randrepeat=1 --ioengine=libaio --direct=1 \
--gtod_reduce=1 --name=test --filename=random_read_write.fio \
--bs=4k --iodepth=64 --size=4G --readwrite=randrw  --rwmixread=75

* --direct=1 ใช้ non-buffered I/O (O_DIRECT)
* --filename=random_read_write.fio ชื่อไฟล์
* --size=4G ขนาดไฟล์ที่ต้องการทดสอบ
* --readwrite=randrw กำหนดให้อ่านและเขียนแบบ สุ่ม
* --rwmixread=75 กำหนดอัตราส่วนอ่านและเขียนเป็น 75:25 (อ่าน 75% เขียน 25%)

[x] Random read performance (ReadOnly Testing)

# fio --randrepeat=1 --ioengine=libaio --direct=1 \
--gtod_reduce=1 --name=test --filename=random_read.fio \
--bs=4k --iodepth=64 --size=4G --readwrite=randread

* --readwrite=randread กำหนดให้อ่านอย่างเดียวแบบ สุ่ม

[x] Random write performance (WriteOnly Testing)

# fio --randrepeat=1 --ioengine=libaio --direct=1 \
--gtod_reduce=1 --name=test --filename=random_write.fio \
--bs=4k --iodepth=64 --size=4G --readwrite=randwrite

* --readwrite=randwrite กำหนดให้เขียนอย่างเดียวแบบ สุ่ม
```

examples:
```
**** On 5,400RPM Disk ****

# fio --randrepeat=1 --ioengine=libaio --direct=1 \
 --gtod_reduce=1 --name=test --filename=random_read_write.fio \
 --bs=4k --iodepth=64 --size=4G --readwrite=randrw  --rwmixread=50

result:
read: IOPS=85, BW=340KiB/s (349kB/s)(2049MiB/6165740msec)
write: IOPS=84, BW=340KiB/s (348kB/s)(2047MiB/6165740msec)

สรุปผล: 
   hdd คอมพิวเตอร์ที่มีความเร็ว 5400 รอบต่อนาที 
   จะมีค่า IOPS ในกรณีที่มีการอ่านและเขียนแบบสุ่ม พร้อมกัน ที่อัตราส่วน 50:50
   จะได้ค่า IOPS สำหรับการอ่านอยู่ที่ 85 ครั้งต่อวินาที และ 84 ครั้งต่อวินาทีสำหรับการเขียน 

**** On SATA 7,200RPM Disk (Raid 1 , 2-disk) ****

# fio --randrepeat=1 --ioengine=libaio --direct=1 \
 --gtod_reduce=1 --name=test --filename=random_read_write.fio \
 --bs=4k --iodepth=64 --size=4G --readwrite=randrw  --rwmixread=50

result:
read: IOPS=204, BW=818KiB/s (837kB/s)(2049MiB/2565884msec)
write: IOPS=204, BW=817KiB/s (836kB/s)(2047MiB/2565884msec)

สรุปผล: 
   SATA hdd สำหรับเซิฟเวอร์ที่มีความเร็ว 7200 รอบต่อนาที จำนวน 2 ลูก 
   ที่อยุ่บน hardware raid 1 (mirror)
   จะมีค่า IOPS ในกรณีที่มีการอ่านและเขียนแบบสุ่ม พร้อมกัน ที่อัตราส่วน 50:50
   จะได้ค่า IOPS สำหรับการอ่านอยู่ที่ 204 ครั้งต่อวินาที 
   และ 204 ครั้งต่อวินาที สำหรับการเขียน 
   
**** On SAS 7,200RPM Disk (Raid 1, 8-disk) ****

# fio --randrepeat=1 --ioengine=libaio --direct=1 \
 --gtod_reduce=1 --name=test --filename=random_read_write.fio \
 --bs=4k --iodepth=64 --size=4G --readwrite=randrw  --rwmixread=50

result:
read: IOPS=490, BW=1962KiB/s (2009kB/s)(2049MiB/1069534msec)
write: IOPS=489, BW=1960KiB/s (2007kB/s)(2047MiB/1069534msec)

สรุปผล: 
   (SSCSI)SATA hdd สำหรับเซิฟเวอร์ที่มีความเร็ว 7200 รอบต่อนาที จำนวน 8 ลูก
   ที่อยุ่บน hardware raid 1 (mirror)
   จะมีค่า IOPS ในกรณีที่มีการอ่านและเขียนแบบสุ่ม พร้อมกัน ที่อัตราส่วน 50:50
   จะได้ค่า IOPS สำหรับการอ่านอยู่ที่ 490 ครั้งต่อวินาที และ 489 ครั้งต่อวินาที 
   สำหรับการเขียน 

**** On 3D-NAND SATA SSD ****

# fio --randrepeat=1 --ioengine=libaio --direct=1 \
 --gtod_reduce=1 --name=test --filename=random_read_write.fio \
 --bs=4k --iodepth=64 --size=4G --readwrite=randrw  --rwmixread=50

result:
read: IOPS=2374, BW=9499KiB/s (9727kB/s)(2049MiB/220920msec)
write: IOPS=2371, BW=9487KiB/s (9714kB/s)(2047MiB/220920msec)

สรุปผล: 
   SSD SATA สำหรับคอมพิวเตอร์ทั่วไปยี่ห้อ WD Blue 3D-NAND 
   จะมีค่า IOPS ในกรณีที่มีการอ่านและเขียนแบบสุ่ม พร้อมกัน ที่อัตราส่วน 50:50 
   จะได้ค่า IOPS สำหรับการอ่านอยู่ที่ 2374 ครั้งต่อวินาที และ 2371 ครั้งต่อวินาที
   สำหรับการเขียน 
```
>Latency measures with IOPing
```bash
[x] CentOS,RHEL
# yum install ioping

[x] Ubuntu
# apt install ioping
```
> testing ioping
```
# ioping -c 100 .
```
