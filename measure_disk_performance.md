>งานระบบฐานข้อมูล นอกเหนือจากหน่วยประมวลผล (CPU Core) และหน่วยความจำ (Memory) จะเพียงพอหรือไม่แล้ว
สิ่งหนึ่งที่ควรคำนึงด้วยนั่นคือ disk performance ในการอ่านและเขียนต่อหน่วยเวลาเป็นวินาที หรือที่เรียกกันว่า IOPS
(Input Output Per Second) เนื่องจากระบบฐานข้อมูลที่มีการใช้งานพร้อมๆ กันจำนวนมาก IOPS ของ disk อาจจะ
ไม่เพียงพอต่องานที่เกิดขึ้นได้ ดังนั้นในการจัดเซิฟเวอร์สำหรับบริการฐานข้อมูลจำเป็นต้อง ทดสอบความสามารถของ disk 
เพื่อให้ทราบถึงขีดความสามารถของ disk ด้วย ซึ่งในการทดสอบจะใช้เครื่องมือชื่อ fio และ ioping

>Install fio
```bash
[x] CentOS,RHEL
# wget https://mirrors.n-ix.net/fedora-epel/epel-release-latest-7.noarch.rpm
# yum localinstall epel-release-latest-7.noarch.rpm
# yum install fio

[x] Ubuntu
# apt install fio
```
>Testing IOPS with fio
```
[x] RW Performance
# fio --randrepeat=1 --ioengine=libaio --direct=1 \
--gtod_reduce=1 --name=test --filename=random_read_write.fio \
--bs=4k --iodepth=64 --size=4G --readwrite=randrw  --rwmixread=75

* --filename=random_read_write.fio ชื่อไฟล์
* --size=4G ขนาดไฟล์ที่ต้องการทดสอบ
* --readwrite=randrw กำหนดให้อ่านเขียนแบบ สุ่ม
* --rwmixread=75 กำหนดอัตราส่วนอ่านและเขียนเป็น 25:75 %

[x] Random read performance
# fio --randrepeat=1 --ioengine=libaio --direct=1 \
--gtod_reduce=1 --name=test --filename=random_read.fio \
--bs=4k --iodepth=64 --size=4G --readwrite=randread

* --readwrite=randread กำหนดให้อ่านอย่างเดียวแบบ สุ่ม

[x] Random write performance
# fio --randrepeat=1 --ioengine=libaio --direct=1 \
--gtod_reduce=1 --name=test --filename=random_write.fio \
--bs=4k --iodepth=64 --size=4G --readwrite=randwrite

* --readwrite=randwrite กำหนดให้เขียนอย่างเดียวแบบ สุ่ม
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
