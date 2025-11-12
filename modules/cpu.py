def get_cpu_name():
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read()
        model_line = [line for line in cpuinfo.split("\n") if "model name" in line][0]
        return model_line.split(":")[1].strip()
    except:
        return "CPU Desconhecida"

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000  
        return f"{temp:.0f}°C"
    except:
        return "N/A"

def read_cpu_usage():
    with open("/proc/stat", "r") as f:
        stats = f.readline().split()[1:]
    stats = [int(x) for x in stats]
    total = sum(stats)
    idle = stats[3]
    return total, idle

last_total, last_idle = read_cpu_usage()

def get_cpu_usage():
    global last_total, last_idle
    total, idle = read_cpu_usage()
    usage = ((total - last_total) - (idle - last_idle)) / (total - last_total) * 100 if (total - last_total) else 0
    last_total, last_idle = total, idle
    return usage

def get_cpu_info():
    cpu_name = get_cpu_name()
    cpu_temp = get_cpu_temp()
    cpu_usage = get_cpu_usage()
    return {
        "Nome": cpu_name,
        "Uso": f"{cpu_usage:.1f}%",
        "Temperatura": cpu_temp
    }
