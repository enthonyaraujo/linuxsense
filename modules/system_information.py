import subprocess  

def systemconf():

    system_info = 'hostnamectl | grep "System" | cut -d: -f2 | xargs'
    system_output = subprocess.check_output(system_info, shell=True, text=True).strip()
        
    firmware_info = 'hostnamectl | grep "Version" | head -n1 | cut -d: -f2 | xargs'
    firmware_output = subprocess.check_output(firmware_info, shell=True, text=True).strip()
        
    vendor_info = 'hostnamectl | grep "Vendor" | cut -d: -f2 | xargs'
    vendor_output = subprocess.check_output(vendor_info, shell=True, text=True).strip()

    model_info = 'hostnamectl | grep "Model" | cut -d: -f2 | xargs'
    model_output = subprocess.check_output(model_info, shell=True, text=True).strip()
    
    info = (
        f"Manufacturer: {vendor_output}\n"
        f"Model: {model_output}\n"
        f"Firmware version: {firmware_output}\n"
        f"Operating System: {system_output}\n"
    )
    return info