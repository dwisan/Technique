Installing software
sudo apt-get -y install vsftpd

/etc/vsftpd.conf
local_enable=YES
write_enable=YES


sudo apt-get install libpam-radius-auth -y
/etc/pam_radius_auth.conf

# server[:port] shared_secret      timeout (s)
172.18.111.19   secret-1       3
172.18.111.20   secret-2       3

/etc/pam.d/vsftpd
/etc/pam.d/sshd

auth sufficient /lib/security/pam_radius_auth.so
@include common-auth

/var/www/html/config/config.php

  'user_backends' => array(
    array(
        'class' => 'OC_User_FTP',
        'arguments' => array('127.0.0.1'),
    ),
  ),

useradd -m -b /home -s /usr/sbin/nologin
