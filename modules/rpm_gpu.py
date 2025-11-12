import glob

def rpm_gpu():
    arquivos = sorted(glob.glob("/sys/class/hwmon/hwmon*/fan*_input"))
    if len(arquivos) >= 2:
        try:
            with open(arquivos[1], 'r') as f:
                rpm = f.read().strip()
                return int(rpm)
        except:
            return None
    else:
        return None


