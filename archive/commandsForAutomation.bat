#ensure that the virtualbox additions are installed first!
#take snapshot after logged in (otherwise video mode is readjusted; or keep checking these things)
#Check the following every 30 seconds:

#for each vm:
VBoxManage.exe list vms

#to determine state:
VBoxManage.exe showvminfo victimBO_WindowsXP_SP0 --machinereadable
#check for the following items
	groups="/New group"
	VRDEActiveConnection="off"
	VideoMode="1920,1080,16"@0,0 1
#to tell which is available:
	vrdeproperty[TCP/Ports]="1000"
#most recent snapshot:
#	CurrentSnapshotName="ready"

#if someone connects, it is in a "notAvailable" state:
VBoxManage.exe controlvm victimBO_WindowsXP_SP0 setvideomodehint 1024 768 16

#if group is in restoreState:
VBoxManage.exe controlvm kali-debian-32 poweroff
VBoxManage.exe snapshot kali-debian-32 restorecurrent
VBoxManage.exe startvm kali-debian-32 --type headless

Three buffers will hold "groups" of vms:
availableState: group with no vm with: VRDEActiveConnection="on"
notAvailableState: group with at least one vm with: VRDEActiveConnection="on"
restoreState=group that is in "notAvailableState" and has VRDEActiveConnection="off"
