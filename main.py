# Load Gtk
import subprocess
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk, GdkPixbuf, cairo

from modules.gpu import get_gpu_info
from modules.cpu import get_cpu_info
from modules.system_information import systemconf
from modules.rpm_cpu import rpm_cpu
from modules.rpm_gpu import rpm_gpu

css = b"""
label {
    font-size: 20px;  
}
headerbar {
    min-height: 28px;     
    padding: 0 6px;        
}

headerbar.title {
    font-size: 14px;       
}


"""

style_provider = Gtk.CssProvider()
style_provider.load_from_data(css)

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

class FanWidget(Gtk.DrawingArea):
    def __init__(self, image_path):
        super().__init__()
        self.angle = 0
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
        self.set_size_request(self.pixbuf.get_width(), self.pixbuf.get_height())
        self.connect("draw", self.on_draw)

    def set_speed(self, rpm):
        self.angle += rpm / 200.0
        self.angle %= 2 * 3.1416
        self.queue_draw()

    def on_draw(self, widget, cr):
        area_w = widget.get_allocated_width()
        area_h = widget.get_allocated_height()
        pix_w = self.pixbuf.get_width()
        pix_h = self.pixbuf.get_height()
        scale = min(area_w / pix_w, area_h / pix_h)
        cr.save()
        cr.translate(area_w / 2, area_h / 2)
        cr.scale(scale, scale)
        cr.rotate(self.angle)
        cr.translate(-pix_w / 2, -pix_h / 2)
        Gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 0, 0)
        cr.paint()
        cr.restore()


def on_custom_scale_value_changed(scale, builder):
    fan_custom = builder.get_object("fan-custom")
    if fan_custom.get_active():  
        fan_custom_scale_cpu = builder.get_object("fan_custom_scale_cpu")
        fan_custom_scale_gpu = builder.get_object("fan_custom_scale_gpu")
        
        valor_cpu = int(fan_custom_scale_cpu.get_value())
        valor_gpu = int(fan_custom_scale_gpu.get_value())

        comando = f"echo {valor_cpu},{valor_gpu} | sudo tee /sys/module/linuwu_sense/drivers/platform:acer-wmi/acer-wmi/nitro_sense/fan_speed"
        subprocess.run(comando, shell=True)

        atualizar_label_modo_fan(builder)
        print(f"Custom Scale atualizado - CPU: {valor_cpu}, GPU: {valor_gpu}")
 
def ler_modo_fan():
    try:
        with open("/sys/module/linuwu_sense/drivers/platform:acer-wmi/acer-wmi/nitro_sense/fan_speed", "r") as f:
            modo = f.read().strip()
            if modo == "0,0":
                modo = "Auto"
            elif modo == "100,100":
                modo = "Max"
            else:
                modo = "Custom"
        return modo
    except:
        return "unknown"
    
def atualizar_label_modo_fan(builder):
    label_modo_fan = builder.get_object("modo-ativado-fan")
    modo = ler_modo_fan()  
    label_modo_fan.set_text(f"Modo ativado: {modo}")

def ler_modo_power():
    try:
        with open("/sys/firmware/acpi/platform_profile", "r") as f:
            modo = f.read().strip()
            if modo == "quiet":
                modo = "Quiet"
            elif modo == "balanced":
                modo = "Balanced"
            elif modo == "balanced-performance":
                modo = "Performance"
        return modo
    except:
        return "unknown"  
    
def atualizar_label_modo_power(builder):
    label_modo_power = builder.get_object("modo-ativado-power")
    modo = ler_modo_power()  
    label_modo_power.set_text(f"Mode activated: {modo}")
  
def on_fan_auto_clicked(toggle_button,builder):
    fan_custom_scale_cpu = builder.get_object("fan_custom_scale_cpu")
    fan_custom_scale_gpu = builder.get_object("fan_custom_scale_gpu")
    fan_custom_scale_cpu.set_visible(False)
    fan_custom_scale_gpu.set_visible(False)
        
    fan_custom = builder.get_object("fan-custom")
    fan_max = builder.get_object("fan-max")
    fan_max.set_active(False)
    fan_custom.set_active(False)
    comando = "echo 0,0 | sudo tee /sys/module/linuwu_sense/drivers/platform:acer-wmi/acer-wmi/nitro_sense/fan_speed"
    subprocess.run(comando,shell=True)
    atualizar_label_modo_fan(builder)
    print("botao auto clicado")
    
def on_fan_custom_clicked(toggle_button,builder):
    fan_auto = builder.get_object("fan-auto")
    fan_max = builder.get_object("fan-max")
    fan_max.set_active(False)
    fan_auto.set_active(False)
    
    fan_custom_scale_cpu = builder.get_object("fan_custom_scale_cpu")
    fan_custom_scale_cpu.set_visible(True)
   
    fan_custom_scale_gpu = builder.get_object("fan_custom_scale_gpu")
    fan_custom_scale_gpu.set_visible(True)   
    
    valor_cpu = int(fan_custom_scale_cpu.get_value())
    valor_gpu = int(fan_custom_scale_gpu.get_value())
    comando = f"echo {valor_cpu},{valor_gpu} | sudo tee /sys/module/linuwu_sense/drivers/platform:acer-wmi/acer-wmi/nitro_sense/fan_speed"
    subprocess.run(comando,shell=True) 
    
    atualizar_label_modo_fan(builder)
    print("botao custom clicado")
    
def on_fan_max_clicked(toggle_button,builder):
    fan_custom_scale_cpu = builder.get_object("fan_custom_scale_cpu")
    fan_custom_scale_gpu = builder.get_object("fan_custom_scale_gpu")
    fan_custom_scale_cpu.set_visible(False)
    fan_custom_scale_gpu.set_visible(False)
    
    
    fan_auto = builder.get_object("fan-auto")
    fan_custom = builder.get_object("fan-custom")
    fan_auto.set_active(False)
    fan_custom.set_active(False)
    comando = "echo 100,100 | sudo tee /sys/module/linuwu_sense/drivers/platform:acer-wmi/acer-wmi/nitro_sense/fan_speed"
    subprocess.run(comando,shell=True)
    atualizar_label_modo_fan(builder)
    print("botao max clicado")

def balance_clicked(toggle_button,builder):
    power_safe = builder.get_object("quiet")  
    performance = builder.get_object("performance")
    power_safe.set_active(False)
    performance.set_active(False)  
    comando = "echo balanced | sudo tee /sys/firmware/acpi/platform_profile"
    subprocess.run(comando, shell=True) 
    atualizar_label_modo_power(builder)
    print("botao balanciado clidado")
    
def permomance_clicked(toggle_button,builder):
    power_safe = builder.get_object("quiet")  
    balance = builder.get_object("balance")
    power_safe.set_active(False)
    balance.set_active(False) 
    comando = "echo balanced-performance | sudo tee /sys/firmware/acpi/platform_profile"
    subprocess.run(comando, shell=True) 
    atualizar_label_modo_power(builder)
    print("botao performance clicado")

def safe_clicked(toggle_button,builder):
    balance = builder.get_object("balance")
    performance = builder.get_object("performance")
    balance.set_active(False)
    performance.set_active(False) 
    comando = "echo quiet | sudo tee /sys/firmware/acpi/platform_profile"
    subprocess.run(comando, shell=True)
    atualizar_label_modo_power(builder)
    print("botao safe clicado")
    
def on_limitador_bateria_toggled(checkbox):
    if checkbox.get_active():
        print("checkbox ativado")
        comando = "echo 1 | sudo tee /sys/module/linuwu_sense/drivers/platform:acer-wmi/acer-wmi/nitro_sense/battery_limiter"
    else:
        print("checkbox desativado")
        comando = "echo 0 | sudo tee /sys/module/linuwu_sense/drivers/platform:acer-wmi/acer-wmi/nitro_sense/battery_limiter"
    subprocess.run(comando, shell=True)

# Quando o aplicativo for iniciado…
def on_activate(app):
    builder = Gtk.Builder()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    interface_path = os.path.join(script_dir, "ui", "interface.glade")
    builder.add_from_file(interface_path)


    window = builder.get_object("main_window") 
    notebook = builder.get_object("notebook")
    
    window.connect("destroy", Gtk.main_quit)
    header = Gtk.HeaderBar(title="LinuxSense")
    header.set_show_close_button(True)
    header.set_name("linuxsense_header")
    window.set_titlebar(header)


    fan_cpu_area = builder.get_object("fan_cpu")  
    fan_cpu_area.set_size_request(60, 60)
    
    fan_gpu_area = builder.get_object("fan_gpu")  
    fan_gpu_area.set_size_request(60, 60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "assets", "fan.png")
    
    fan_cpu_widget = FanWidget(img_path)
    fan_cpu_area.connect("draw", fan_cpu_widget.on_draw)
    
    fan_gpu_widget = FanWidget(img_path)
    fan_gpu_area.connect("draw", fan_gpu_widget.on_draw)

    def atualizar_fan_cpu():
        rpm_cpu_value = rpm_cpu()
        rpm_gpu_value = rpm_gpu()
        fan_cpu_widget.set_speed(rpm_cpu_value if rpm_cpu_value is not None else 0)
        fan_gpu_widget.set_speed(rpm_gpu_value if rpm_gpu_value is not None else 0)
        return True

    GLib.timeout_add(16, atualizar_fan_cpu)
        
    checkbox = builder.get_object("limitador_bateria")
    fan_custom_scale_cpu = builder.get_object("fan_custom_scale_cpu")
    fan_custom_scale_gpu = builder.get_object("fan_custom_scale_gpu")

    fan_custom_scale_cpu.connect("value-changed", lambda s: on_custom_scale_value_changed(s, builder))
    fan_custom_scale_gpu.connect("value-changed", lambda s: on_custom_scale_value_changed(s, builder)) 

    # aqui abaixo le o arquivo e verifica se esta com 1 ou 0, caso 1 ele ativa o checkbox caso contrario desativa
    try:
        with open("/sys/module/linuwu_sense/drivers/platform:acer-wmi/acer-wmi/nitro_sense/battery_limiter", "r") as f:
            val = f.read().strip()
        checkbox.set_active(val == "1")
    except Exception as e:
        print("Erro ao ler arquivo do limitador:", e)
        checkbox.set_active(False)    
    
    #####################
    ###### BUTTONS ######
    #####################
    
    builder.connect_signals({
        "on_fan_auto_clicked": lambda btn: on_fan_auto_clicked(btn, builder),
        "on_fan_custom_clicked": lambda btn: on_fan_custom_clicked(btn, builder),
        "on_fan_max_clicked": lambda btn: on_fan_max_clicked(btn, builder),
        "safe_clicked": lambda btn: safe_clicked(btn, builder),
        "balance_clicked": lambda btn: balance_clicked(btn, builder),
        "permomance_clicked": lambda btn: permomance_clicked(btn, builder),
        "on_limitador_bateria_toggled": on_limitador_bateria_toggled,

    })
    
    ####################
    ###### LABELS ######
    ####################
    
    def atualizar_labels_rpm():
        rpm_cpu_value = rpm_cpu()
        label_rpm_cpu.set_text(f"CPU FAN RPM: {rpm_cpu_value if rpm_cpu_value is not None else 'N/A'}")
        
        rpm_gpu_value = rpm_gpu()
        label_rpm_gpu.set_text(f"GPU FAN RPM: {rpm_gpu_value if rpm_gpu_value is not None else 'N/A'}")
        
        return True  
    
    label_rpm_cpu = builder.get_object("rpm-cpu")
    label_rpm_gpu = builder.get_object("rpm-gpu")

    GLib.timeout_add(1000, atualizar_labels_rpm)
   
    label_system_information = builder.get_object("system-information")
    system_information = systemconf()
    label_system_information.set_text(system_information)
    
    label_modo_fan = builder.get_object("modo-ativado-fan")
    modo = ler_modo_fan()
    label_modo_fan.set_text(f"Mode activated: {modo}")
    
    label_modo_power = builder.get_object("modo-ativado-power")
    modo = ler_modo_power()
    label_modo_power.set_text(f"Mode activated: {modo}")
    
    label_cpu_info = builder.get_object("cpu-info")
    
    def update_label_cpu_info():
        cpu_data = get_cpu_info()
        label_cpu_info.set_text(f"{cpu_data['Nome']}\nUsage: {cpu_data['Uso']}\nTemperatura: {cpu_data['Temperatura']}")
        return True  
    
    label_gpu_info = builder.get_object("gpu-info")
    
    def update_label_gpu_info():
        gpu_name, gpu_usage, gpu_temp = get_gpu_info()
        label_gpu_info.set_text(f"{gpu_name}\nUsage: {gpu_usage}\nTemperature: {gpu_temp}")
        return True  

    GLib.timeout_add(1000, update_label_gpu_info)  
    GLib.timeout_add(1000, update_label_cpu_info)  
    
    if not window:
        
        window = Gtk.ApplicationWindow(application=app)

    
    window.show_all()
    fan_custom_scale_cpu.set_visible(False)
    fan_custom_scale_gpu.set_visible(False)

    window.set_application(app)
    window.present()

# Criar um novo aplicativo
app = Gtk.Application(application_id='com.enthonyaraujo.linuxsense')
app.connect('activate', on_activate)

# Execute o aplicativo
app.run(None)
