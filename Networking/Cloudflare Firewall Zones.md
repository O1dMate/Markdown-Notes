# CloudFlare Firewall Zones 

### Add these to Firewall (CentOS blocks all by default)
```text
firewall-cmd --zone=public --permanent --add-source=173.245.48.0/20
firewall-cmd --zone=public --permanent --add-source=103.21.244.0/22
firewall-cmd --zone=public --permanent --add-source=103.22.200.0/22
firewall-cmd --zone=public --permanent --add-source=103.31.4.0/22
firewall-cmd --zone=public --permanent --add-source=141.101.64.0/18
firewall-cmd --zone=public --permanent --add-source=108.162.192.0/18
firewall-cmd --zone=public --permanent --add-source=190.93.240.0/20
firewall-cmd --zone=public --permanent --add-source=188.114.96.0/20
firewall-cmd --zone=public --permanent --add-source=197.234.240.0/22
firewall-cmd --zone=public --permanent --add-source=198.41.128.0/17
firewall-cmd --zone=public --permanent --add-source=162.158.0.0/15
firewall-cmd --zone=public --permanent --add-source=104.16.0.0/12
firewall-cmd --zone=public --permanent --add-source=172.64.0.0/13
firewall-cmd --zone=public --permanent --add-source=131.0.72.0/22
```