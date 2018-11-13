"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm %1 poweroff
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" snapshot %1 restorecurrent
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm %1 --type headless
