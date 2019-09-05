> Network Subnet Changing
- [x] The Default Bridge (docker0)
```
nano /etc/docker/daemon.json

{
    "bip":"198.18.0.0/16"
}
```
- [x] User generated bridge networks
```
nano /etc/docker/daemon.json

{
  "default-address-pools":
  [
    {"base":"10.10.0.0/16","size":24}
  ]
}
```
- [x] These two
```
{
  "bip": "10.200.0.1/24",
  "default-address-pools":[
    {"base":"10.201.0.0/16","size":24},
    {"base":"10.202.0.0/16","size":24}
  ]
}
```
