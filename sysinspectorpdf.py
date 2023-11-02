import os
import platform
import psutil
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
import datetime

# Función para obtener el uso global de la CPU
def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    return sum(cpu_percent) / len(cpu_percent)

# Función para obtener la lista de programas en ejecución
def get_running_processes_info():
    processes_info = []

    for process in psutil.process_iter(attrs=['pid', 'name', 'username', 'memory_info']):
        try:
            process_info = process.info
            processes_info.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return processes_info

# Crear un informe en PDF
def create_report():
    doc = SimpleDocTemplate(generate_report_name(), pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Obtener información del sistema
    user_name = os.getlogin()
    cpu_info = platform.processor()
    memory_info = psutil.virtual_memory()
    os_info = platform.platform()

    # Obtener información de los programas en ejecución
    processes_info = get_running_processes_info()

    # Fecha y hora actual
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    # Agregar información al informe
    elements.append(Paragraph(f"Informe de Especificaciones Técnicas de la Computadora de {user_name}", styles['Title']))
    elements.append(Paragraph(f"Fecha y Hora de Generación: {current_datetime}", styles['Normal']))
    elements.append(Paragraph(f"Nombre de Usuario: {user_name}", styles['Normal']))
    elements.append(Paragraph(f"Procesador: {cpu_info}", styles['Normal']))
    elements.append(Paragraph(f"Memoria RAM: {memory_info.total / (1024 ** 3):.2f} GB", styles['Normal']))
    elements.append(Paragraph(f"Uso de RAM: {memory_info.percent:.2f}%", styles['Normal']))
    elements.append(Paragraph(f"Sistema Operativo y Versión: {os_info}", styles['Normal']))

    # Obtener el uso global de la CPU
    cpu_usage = get_cpu_usage()
    elements.append(Paragraph(f"Uso de CPU: {cpu_usage:.2f}%", styles['Normal']))

    # Crear una tabla con la lista de programas en ejecución
    table_data = [["PID", "Nombre del Programa", "Usuario", "Memoria (MB)"]]
    for process_info in processes_info:
        pid = process_info['pid']
        name = process_info['name'] if process_info['name'] else "N/A"
        username = process_info['username'] if process_info['username'] else "N/A"
        memory_used = process_info['memory_info'].rss / (1024 * 1024) if process_info['memory_info'] else 0
        table_data.append([pid, name, username, memory_used])

    table = Table(table_data, repeatRows=1, hAlign='CENTER')
    elements.append(table)

    # Créditos
    elements.append(Paragraph("Credito: <a href='http://www.jairuribe.lat'>Jair Uribe</a>", styles['Normal']))

    # Generar el PDF
    doc.build(elements)

def generate_report_name():
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f"Informe_{current_datetime}.pdf"

if __name__ == "__main__":
    create_report()
    print("Informe generado con éxito.")
