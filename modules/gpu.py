import subprocess

def get_gpu_info():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,temperature.gpu", "--format=csv,noheader"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return "NVIDIA não detectada", "0%", "N/A"
        
        gpu_data = result.stdout.strip().split(", ")
        gpu_name = gpu_data[0]
        gpu_usage = gpu_data[1].strip()
        gpu_temp = f"{gpu_data[2].strip()}°C"
        
        return gpu_name, gpu_usage, gpu_temp
    except FileNotFoundError:
        return "nvidia-smi não instalado", "0%", "N/A"

