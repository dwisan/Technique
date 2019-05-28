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
--bs=4k --iodepth=64 --size=4G --readwrite=randrw --rwmixread=75

[x] Random read performance
# fio --randrepeat=1 --ioengine=libaio --direct=1 \
--gtod_reduce=1 --name=test --filename=random_read.fio \
--bs=4k --iodepth=64 --size=4G --readwrite=randread

[x] Random write performance
# fio --randrepeat=1 --ioengine=libaio --direct=1 \
--gtod_reduce=1 --name=test --filename=random_write.fio \
--bs=4k --iodepth=64 --size=4G --readwrite=randwrite
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
