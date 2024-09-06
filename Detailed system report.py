import os
import platform
import psutil
import datetime

def get_system_info():
    system_info = {
        'os': platform.system(),
        'version': platform.version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'ram': f"{round(psutil.virtual_memory().total/1024.**3)} GB",
        'uptime': str(datetime.timedelta(seconds=psutil.boot_time()))
    }
    return system_info

def get_disk_info():
    disk_info = []
    for disk in psutil.disk_partitions(all=True):
        if os.name == 'nt':
            if 'cdrom' in disk.opts or disk.fstype == '':
                continue
        usage = psutil.disk_usage(disk.mountpoint)
        disk_info.append({
            'device': disk.device,
            'mountpoint': disk.mountpoint,
            'file_system': disk.fstype,
            'total': f"{usage.total/1024.**3:.2f} GB",
            'used': f"{usage.used/1024.**3:.2f} GB",
            'free': f"{usage.free/1024.**3:.2f} GB",
            'usage_percent': f"{usage.percent}%"
        })
    return disk_info

def get_network_info():
    network_adapters = []
    for (interface_name, interface_addresses) in psutil.net_if_addrs().items():
        for address in interface_addresses:
            if address.family == psutil.AF_LINK:
                network_adapters.append({
                    'name': interface_name,
                    'mac': address.address
                })
                break
    return network_adapters

def get_process_info():
    process_info = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time']):
        try:
            process = proc.info
            process_info.append({
                'pid': process['pid'],
                'name': process['name'],
                'user': process['username'],
                'start_time': datetime.datetime.fromtimestamp(process['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return process_info

def get_startup_programs():
    startup_programs = []
    if platform.system() == 'Windows':
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
            for i in range(winreg.QueryInfoKey(key)[1]):
                value_name, value_data, _ = winreg.EnumValue(key, i)
                startup_programs.append({
                    'name': value_name,
                    'path': value_data
                })
        except WindowsError:
            pass
    return startup_programs

def generate_report():
    system_info = get_system_info()
    disk_info = get_disk_info()
    network_adapters = get_network_info()
    process_info = get_process_info()
    startup_programs = get_startup_programs()

    report = f'''
<!DOCTYPE html>
<html>
<head>
    <title>System Information Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .report-section {{
            margin-bottom: 40px;
        }}
        .report-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="report-section">
        <div class="report-title">System Information</div>
        <table>
            <tr>
                <th>OS</th>
                <td>{system_info["os"]}</td>
            </tr>
            <tr>
                <th>Version</th>
                <td>{system_info["version"]}</td>
            </tr>
            <tr>
                <th>Architecture</th>
                <td>{system_info["architecture"]}</td>
            </tr>
            <tr>
                <th>Processor</th>
                <td>{system_info["processor"]}</td>
            </tr>
            <tr>
                <th>RAM</th>
                <td>{system_info["ram"]}</td>
            </tr>
            <tr>
                <th>Uptime</th>
                <td>{system_info["uptime"]}</td>
            </tr>
        </table>
    </div>

    <div class="report-section">
        <div class="report-title">Disk Information</div>
        <table>
            <tr>
                <th>Device</th>
                <th>Mountpoint</th>
                <th>File System</th>
                <th>Total</th>
                <th>Used</th>
                <th>Free</th>
                <th>Usage</th>
            </tr>
            '''
    for disk in disk_info:
        report += f"""
            <tr>
                <td>{disk["device"]}</td>
                <td>{disk["mountpoint"]}</td>
                <td>{disk["file_system"]}</td>
                <td>{disk["total"]}</td>
                <td>{disk["used"]}</td>
                <td>{disk["free"]}</td>
                <td>{disk["usage_percent"]}</td>
            </tr>
        """
    report += '\n        </table>\n    </div>\n\n    <div class="report-section">\n        <div class="report-title">Network Adapters</div>\n        <table>\n            <tr>\n                <th>Name</th>\n                <th>MAC Address</th>\n            </tr>\n    '
    for adapter in network_adapters:
        report += f"""
            <tr>
                <td>{adapter["name"]}</td>
                <td>{adapter["mac"]}</td>
            </tr>
        """
    report += '\n        </table>\n    </div>\n\n    <div class="report-section">\n        <div class="report-title">Running Processes</div>\n        <table>\n            <tr>\n                <th>PID</th>\n                <th>Name</th>\n                <th>User</th>\n                <th>Start Time</th>\n            </tr>\n    '
    for process in process_info:
        report += f"""
            <tr>
                <td>{process["pid"]}</td>
                <td>{process["name"]}</td>
                <td>{process["user"]}</td>
                <td>{process["start_time"]}</td>
            </tr>
        """
    report += '\n        </table>\n    </div>\n\n    <div class="report-section">\n        <div class="report-title">Startup Programs</div>\n        <table>\n            <tr>\n                <th>Name</th>\n                <th>Path</th>\n            </tr>\n    '
    for program in startup_programs:
        report += f"""
            <tr>
                <td>{program["name"]}</td>
                <td>{program["path"]}</td>
            </tr>
        """
    report += f'''
        </table>
    </div>

    <div class="report-section">
        Report generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </div>
</body>
</html>
'''
    with open('system_info_report.html', 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == '__main__':
    generate_report()