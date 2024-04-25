import psutil
import platform
from datetime import datetime


def get_size(bytes, suffix='B'):
    factor = 1024
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < factor:
            return f'{bytes:.2f}{unit}{suffix}'
        bytes /= factor


def get_memory_info():
    mem_info = {}
    svmem = psutil.virtual_memory()
    mem_info['Объем'] = get_size(svmem.total)
    mem_info['Доступно'] = get_size(svmem.available)
    mem_info['Используется'] = get_size(svmem.used)
    mem_info['Процент'] = f'{svmem.percent}%'

    swap = psutil.swap_memory()
    swap_info = {}
    swap_info['Объем'] = get_size(swap.total)
    swap_info['Свободно'] = get_size(swap.free)
    swap_info['Используется'] = get_size(swap.used)
    swap_info['Процент'] = f'{swap.percent}%'

    mem_info['Память подкачки'] = swap_info
    return mem_info


def get_disk_info():
    disk_info = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_info = {}
        partition_info['Диск'] = partition.device
        partition_info['Тип файловой системы'] = partition.fstype
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        partition_info['Общий объем'] = get_size(partition_usage.total)
        partition_info['Используется'] = get_size(partition_usage.used)
        partition_info['Свободно'] = get_size(partition_usage.free)
        partition_info['Процент'] = f'{partition_usage.percent}%'
        disk_info.append(partition_info)
    return disk_info


def get_network_info():
    network_info = {}
    if_addrs = psutil.net_if_addrs()
    interfaces = []
    for interface_name, interface_addresses in if_addrs.items():
        interface_info = {'Интерфейс': interface_name}
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                interface_info['IP'] = address.address
                interface_info['Сетевая маска'] = address.netmask
                interface_info['Широковещательный IP-адрес'] = address.broadcast
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                interface_info['MAC-адрес'] = address.address
                interface_info['Сетевая маска'] = address.netmask
                interface_info['Широковещательный MAC-адрес'] = address.broadcast
        interfaces.append(interface_info)
    network_info['Сетевые интерфейсы'] = interfaces

    net_io = psutil.net_io_counters()
    network_info['Отправлено'] = get_size(net_io.bytes_sent)
    network_info['Получено'] = get_size(net_io.bytes_recv)
    network_info['Отправлено пакетов'] = net_io.packets_sent
    network_info['Получено пакетов'] = net_io.packets_recv

    return network_info


class SystemInfo:
    def __init__(self):
        self.uname = platform.uname()

    def __str__(self):

        system_info = f"{'=' * 40} Система: {'=' * 40}\n" \
                      f"Система: {self.uname.system}\nИмя узла: {self.uname.node}" \
                      f"\nВыпуск: {self.uname.release}\nВерсия: {self.uname.version}" \
                      f"\nМашина: {self.uname.machine}\nПроцессор: {self.uname.processor}\n\n"

        cpu_info = f"Физические ядра: {psutil.cpu_count(logical=False)}" \
                   f"\nВсего ядер: {psutil.cpu_count(logical=True)}" \
                   f"\nМаксимальная частота: {psutil.cpu_freq().max / 1000 :.2f}МГц" \
                   f"\nМинимальная частота: {psutil.cpu_freq().min / 1000 :.2f}МГц" \
                   f"\nТекущая частота: {psutil.cpu_freq().current / 1000 :.2f}МГц" \
                   f"\n\n{'=' * 40} Загрузка процессора на ядро:  {'=' * 40}\n"

        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            core_name = f'Ядро {i}'
            cpu_info += f"{core_name}: {percentage}%\n"
        cpu_info += f"{'=' * 40} Общая загруженность процессора:  {'=' * 40}{psutil.cpu_percent()}%\n\n"

        mem_info = f"Объем памяти: {get_memory_info()['Объем']}" \
                   f"\nДоступно памяти: {get_memory_info()['Доступно']}" \
                   f"\nИспользуется памяти: {get_memory_info()['Используется']}" \
                   f"\nПроцент использования памяти: {get_memory_info()['Процент']}" \
                   f"\n\nОбъем памяти подкачки: {get_memory_info()['Память подкачки']['Объем']}" \
                   f"\nСвободно памяти подкачки: {get_memory_info()['Память подкачки']['Свободно']}" \
                   f"\nИспользуется памяти подкачки: {get_memory_info()['Память подкачки']['Используется']}" \
                   f"\nПроцент использования памяти подкачки: {get_memory_info()['Память подкачки']['Процент']}\n\n"

        disk_info = f"{'=' * 40} Диски и разделы: {'=' * 40}\n"
        for i, partition in enumerate(get_disk_info()):
            disk_info += f"{i + 1}. {partition['Диск']}, Тип файловой системы: {partition['Тип файловой системы']}" \
                         f", Общий объем: {partition['Общий объем']},\n Используется: {partition['Используется']}" \
                         f", Свободно: {partition['Свободно']}, Процент использования: {partition['Процент']}\n"
        disk_info += "\n"

        network_info = f"{'=' * 40} Сетевая информация: {'=' * 40}\n"
        for interface in get_network_info()['Сетевые интерфейсы']:
            network_info += f"Интерфейс: {interface['Интерфейс']}\nIP: {interface.get('IP', '-')}" \
                            f"\nСетевая маска: {interface.get('Сетевая маска', '-')}" \
                            f"\nШироковещательный IP-адрес: {interface.get('Широковещательный IP-адрес', '-')}" \
                            f"\nMAC-адрес: {interface.get('MAC-адрес', '-')}" \
                            f"\nШироковещательный MAC-адрес: {interface.get('Широковещательный MAC-адрес', '-')}\n\n"
        network_info += f"Отправлено: {get_network_info()['Отправлено']}" \
                        f"\nПолучено: {get_network_info()['Получено']}" \
                        f"\nОтправлено пакетов: {get_network_info()['Отправлено пакетов']}" \
                        f"\nПолучено пакетов: {get_network_info()['Получено пакетов']}"

        return system_info + cpu_info + mem_info + disk_info + network_info


sys_info = SystemInfo()
print(sys_info.__str__())
