"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm kali-debian-32 poweroff
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" snapshot kali-debian-32 restorecurrent
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" showvminfo kali-debian-32 --machinereadable >> out.txt
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm kali-debian-32 --type headless
