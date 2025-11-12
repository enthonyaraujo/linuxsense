import glob

def rpm_cpu():
    arquivos = glob.glob("/sys/class/hwmon/hwmon*/fan*_input")
    for arquivo in sorted(arquivos):
        try:
            with open(arquivo, 'r') as f:
                rpm = f.read().strip()
                return int(rpm)
        except Exception as e:
            pass
    return None  

