import subprocess
import shutil
import xml.etree.ElementTree as ET
import shlex
import time


pathToVirtualBox = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
groupToVms = {}
vmToGroups = {}
availableState = []
notAvailableState = []
restoreState = []
currvms = []
vms = []

itemsOfInterest = ["name", "groups", "VRDEActiveConnection", "VideoMode", "vrdeproperty[TCP/Ports]"]

def makeAvailableToNotAvailable(vmNameList):
	#print "making notAvailable",vmNameList,"\n"
	for vmName in vmNameList:
		availableState.remove(vmName)
		notAvailableState.append(vmName)
		
def makeNotAvailableToRestoreState(vmNameList):
	#print "making notAvailableToRestore:",vmNameList,"\n"
	for vmName in vmNameList:
		notAvailableState.remove(vmName)
		restoreState.append(vmName)
		
def makeRestoreToAvailableState(vmNameList):
	#print "making restoreToAvailable:",vmNameList,"\n"
	for vmName in vmNameList:
#VBoxManage.exe controlvm victimBO_WindowsXP_SP0 poweroff
#VBoxManage.exe snapshot victimBO_WindowsXP_SP0 restorecurrent
#VBoxManage.exe startvm victimBO_WindowsXP_SP0 --type headless
		print "!!!!!!!!!!!!!!!!!!!!!!!!vmGroup for",vmName,":"
	#Need to reload all vms that are in the group of the vm in the "restore" state
		sVmName = vmName.replace("\"","")
		output = subprocess.call([pathToVirtualBox, "controlvm", sVmName, "poweroff"])
		output = subprocess.call([pathToVirtualBox, "snapshot", sVmName, "restorecurrent"])
		output = subprocess.call([pathToVirtualBox, "startvm", sVmName, "--type", "headless"])
		restoreState.remove(vmName)
		availableState.append(vmName)
		
def makeNewToAvailableState(vmNameList):
	#print "making available:",vmNameList,"\n"
	for vmName in vmNameList:
		availableState.append(vmName)

def changeVideoMode(vmNameList):
	for vmName in vmNameList:
#VBoxManage.exe controlvm victimBO_WindowsXP_SP0 setvideomodehint 1024 768 16
		sVmName = vmName.replace("\"","")
		output = subprocess.call([pathToVirtualBox, "controlvm", sVmName, "setvideomodehint","1024","768","16"])

while True:
	currvms = []
	#first get all vms
	getVMsCmd = [pathToVirtualBox, "list", "vms"]
	vmList = subprocess.check_output(getVMsCmd).split("\n")
	
	#for each vm get info and place in state list
	for vm in vmList:
		line = vm.split("\"")
		if len(line) > 2:
			vmName = line[1]
			print vmName
			showVmInfo = subprocess.check_output([pathToVirtualBox, "showvminfo", vmName, "--machinereadable"])
			splitVmInfo = {}
			for line in showVmInfo.split("\n"):
				keyValue=line.rstrip().split("=")
				if keyValue[0] in itemsOfInterest:
					splitVmInfo[keyValue[0]] = keyValue[1]
			
		#parse out values of interest
			
			#Only keep vms that are in a group
			if splitVmInfo["groups"] != "/":
				currvms.append(splitVmInfo)
				#keep track of groups
				groupToVms = {}
				vmToGroups = {}
				if splitVmInfo["groups"] not in groupToVms:
					groupToVms[splitVmInfo["groups"]] = []
				groupToVms[splitVmInfo["groups"]].append(vmName)
	#so we get all at once (may have to create a lock?)
	vms = currvms
	
	########Assign each vm into a state list############
		
		#first look at any "not available" to see if they go into the "restore" state
	nasList = []
	resList = []
	for vm in vms:
		if "VRDEActiveConnection" in vm:
			if vm["VRDEActiveConnection"] == "\"on\"" and vm["name"] in availableState and vm["name"] not in notAvailableState:
				nasList.append(vm["name"])
			elif vm["VRDEActiveConnection"] == "\"off\"" and vm["name"] in notAvailableState and vm["name"] not in restoreState:
				resList.append(vm["name"])
	makeNotAvailableToRestoreState(resList)
	makeAvailableToNotAvailable(nasList)
	
		#next look at restore state and make them available
	makeRestoreToAvailableState(restoreState)
		
		#place any left into the available list
	av = []
	for vm in vms:
		if vm["name"] not in notAvailableState and vm["name"] not in restoreState and vm["name"] not in availableState:
			av.append(vm["name"])
	makeNewToAvailableState(av)

	########Change video mode to 16-bit colors to reduce bandwidth###########
	vidmod = []
	for vm in vms:
		print vm
		if "VideoMode" in vm:
			currMode = vm["VideoMode"].split(",")[2].split("\"")[0]
			if int(currMode) > 16:
				vidmod.append(vm["name"])
	changeVideoMode(vidmod)


	print "status:"
	print "available:",availableState
	print "notAvailable:",notAvailableState
	print "restore:",restoreState
	
	time.sleep(1)
