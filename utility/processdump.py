import psutil
import subprocess

output_file = "processes_and_services.txt"

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            process_info = {
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'exe': proc.info['exe'] or "N/A"
            }
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def get_running_services():
    try:
        output = subprocess.check_output("sc query state= all", shell=True, text=True)
        services = []
        current_service = {}

        for line in output.splitlines():
            line = line.strip()
            if line.startswith("SERVICE_NAME"):
                current_service = {'SERVICE_NAME': line.split(':')[1].strip()}
            elif line.startswith("DISPLAY_NAME"):
                current_service['DISPLAY_NAME'] = line.split(':')[1].strip()
            elif line.startswith("STATE"):
                current_service['STATE'] = line.split(':')[1].strip()
                services.append(current_service)

        return services
    except Exception as e:
        return [f"Error retrieving services: {str(e)}"]

def write_to_file(processes, services):
    with open(output_file, 'w') as file:
        file.write("Running Processes:\n")
        file.write("PID\tExecutable Path\tProcess Name\n")
        file.write("-" * 80 + "\n")
        for proc in processes:
            file.write(f"{proc['pid']}\t{proc['exe']}\t{proc['name']}\n")

        file.write("\nRunning Services:\n")
        file.write("SERVICE_NAME\tDISPLAY_NAME\tSTATE\n")
        file.write("-" * 80 + "\n")
        for svc in services:
            if isinstance(svc, dict):
                file.write(f"{svc['SERVICE_NAME']}\t{svc['DISPLAY_NAME']}\t{svc['STATE']}\n")
            else:
                file.write(svc + "\n")

if __name__ == "__main__":
    processes = get_running_processes()
    services = get_running_services()
    write_to_file(processes, services)
    print(f"Processes and services information written to {output_file}")
