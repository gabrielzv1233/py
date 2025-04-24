#!/usr/bin/env python3
import platform
import subprocess
import json

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    for unit in ['KB', 'MB', 'GB', 'TB', 'PB']:
        size_bytes /= 1024.0
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"

def scan_windows():
    try:
        import wmi
    except ImportError:
        print("wmi module not installed. Install it with 'pip install wmi'")
        exit(1)

    c = wmi.WMI()
    drives = []
    
    for disk in c.Win32_DiskDrive():
        size = int(disk.Size)
        model = disk.Model.strip()
        drive_type = "Unknown"
        
        # Determine drive type
        if disk.MediaType:
            if "Removable" in disk.MediaType:
                drive_type = "thumbdrive"
            elif "Fixed" in disk.MediaType:
                drive_type = "SSD" if "SSD" in disk.Model.upper() else "HDD"
        else:
            if disk.InterfaceType.upper() == "USB":
                drive_type = "thumbdrive"
            else:
                drive_type = "SSD" if "SSD" in disk.Model.upper() else "HDD"
        
        # Get drive letter(s) and volume names
        partitions = disk.associators("Win32_DiskDriveToDiskPartition")
        volumes = []
        primary_letter = None
        for partition in partitions:
            logical_disks = partition.associators("Win32_LogicalDiskToPartition")
            for logical_disk in logical_disks:
                drive_letter = logical_disk.DeviceID
                volume_name = logical_disk.VolumeName if logical_disk.VolumeName else "Unknown"
                volume_size = format_size(int(logical_disk.Size)) if logical_disk.Size else "Unknown"
                volumes.append(f"{volume_name}:{volume_size}")
                
                # Use the first found drive letter as the primary one
                if primary_letter is None:
                    primary_letter = drive_letter

        volume_str = ", ".join(volumes) if volumes else "No Volume"
        primary_letter = primary_letter + "\\" if primary_letter else "No Drive Letter"

        drives.append(f"{primary_letter} ({drive_type}) {model} {{{volume_str}}}")

    for drive in sorted(drives):
        print(drive)

def scan_linux():
    result = subprocess.run(["lsblk", "-J", "-b"], capture_output=True, text=True)
    if result.returncode != 0:
        print("lsblk command failed")
        exit(1)
    
    data = json.loads(result.stdout)
    drives = []
    
    for device in data["blockdevices"]:
        size = int(device["size"])
        model = device.get("model", "Unknown").strip()
        drive_type = "Unknown"
        
        if device.get("rm") in [True, 1, "1"]:
            drive_type = "thumbdrive"
        else:
            if "rota" in device:
                drive_type = "SSD" if device["rota"] == 0 else "HDD"
            else:
                drive_type = "disk"
        
        # Get partitions and their mount points
        volumes = []
        primary_mount = None
        if "children" in device:
            for partition in device["children"]:
                mountpoint = partition.get("mountpoint", "No Mountpoint")
                partition_size = format_size(int(partition["size"]))
                volumes.append(f"{mountpoint}:{partition_size}")
                
                # Use the first found mountpoint as the primary one
                if primary_mount is None and mountpoint != "No Mountpoint":
                    primary_mount = mountpoint

        volume_str = ", ".join(volumes) if volumes else "No Volume"
        primary_mount = primary_mount if primary_mount else "/dev/" + device["name"]

        drives.append(f"{primary_mount} ({drive_type}) {model} {{{volume_str}}}")

    for drive in sorted(drives):
        print(drive)

def main():
    system = platform.system()
    if system == "Windows":
        scan_windows()
    elif system == "Linux":
        scan_linux()
    else:
        print("Platform not supported.")

if __name__ == "__main__":
    main()
