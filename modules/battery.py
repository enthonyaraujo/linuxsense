import os

def check_battery_support():

    power_supply_path = "/sys/class/power_supply/"
    
    if not os.path.exists(power_supply_path):
        return False, "Diretório de power_supply não encontrado"
    
    battery_devices = [d for d in os.listdir(power_supply_path) if d.startswith(('BAT', 'bat'))]
    
    if not battery_devices:
        return False, "Nenhum dispositivo de bateria encontrado"
    
    required_files = ['capacity', 'status']
    for device in battery_devices:
        device_path = os.path.join(power_supply_path, device)
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(device_path, f))]
        
        if not missing_files:
            return True, device  # Retorna True e o dispositivo encontrado
    
    return False, f"Arquivos necessários não encontrados em {battery_devices}"

def get_battery_status():

    supported, message = check_battery_support()
    if not supported:
        return "N/A", message  
    
    battery_device = message  
    battery_path = os.path.join("/sys/class/power_supply/", battery_device)
    
    try:
       
        with open(os.path.join(battery_path, "capacity"), "r") as f:
            percent = f.read().strip() + "%"
        
        status_file = "status"
        if not os.path.exists(os.path.join(battery_path, status_file)):
            status_file = "POWER_SUPPLY_STATUS"
        
        with open(os.path.join(battery_path, status_file), "r") as f:
            status = f.read().strip().lower()
            
            if status in ['charging', 'full']:
                status_pt = "Carregando"
            elif status == 'discharging':
                status_pt = "Descarregando"
            else:
                status_pt = f"Status desconhecido ({status})"
        
        return percent, status_pt
    
    except PermissionError:
        return "N/A", "Permissão negada (execute como root?)"
    except Exception as e:
        return "N/A", f"Erro ao ler dados: {str(e)}"
