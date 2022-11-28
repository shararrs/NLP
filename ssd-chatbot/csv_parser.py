import csv


def capacity_gb_to_str(capacity_gb: float):
    """Convert flaot(1200) -> 1.2 TB"""
    if capacity_gb >= 1000:
        return f"{capacity_gb / 1000}TB"
    else:
        return f"{capacity_gb}GB"


def get_capacity_gb(capacity_str):
    """Convert 1.2 TB -> flaot(1200)"""
    unit = capacity_str[-2:]
    if unit == 'GB':
        return float(capacity_str[:-2])
    else:
        return float(capacity_str[:-2]) * 1000


class SSD:
    """Model of a SSD"""
    def __init__(self,
                 *,
                 brand,
                 model,
                 interface,
                 form_factor,
                 capacity,
                 controller,
                 dram,
                 nand_brand,
                 nand_type,
                 read_speed_mbps,
                 write_speed_mbps,
                 categories
                 ):
        self.brand = brand
        self.model = model
        self.interface = interface
        self.form_factor = form_factor
        self.capacity = capacity
        self.controller = controller
        self.dram = dram
        self.nand_brand = nand_brand
        self.nand_type = nand_type
        self.read_speed_mbps = read_speed_mbps
        self.write_speed_mbps = write_speed_mbps
        self.categories = categories

    def __str__(self):
        return f"{self.brand} {self.model}, {capacity_gb_to_str(self.capacity)}"

    def get_nn_specs(self):
        return {
            'brand': self.brand,
            'model': self.model,
            'interface': self.interface,
            'form factor': self.form_factor,
            'controller': self.controller,
            'nand brand': self.nand_brand,
            'nand type': self.nand_type,
            'category': self.categories
        }


# Parse the CSV File

def get_max_capacity(capacity_range_str: str):
    if '-' in capacity_range_str:
        min_capacity_str, max_capacity_str = row['Capacities'].split('-')
    else:
        max_capacity_str = row['Capacities']

    return get_capacity_gb(max_capacity_str)


with open('SSDs_Master_List.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    ssd_list = []
    for row in reader:
        try:
            max_capacity = get_max_capacity(row['Capacities'])
            read_speed, write_speed = (float(x) for x in row['R/W (Up to, in MB/s)'].split('/'))
            ssd = SSD(
                brand=row['Brand'],
                model=row['Model'],
                interface=row['Interface'],
                form_factor=row['Form Factor'],
                capacity=max_capacity,
                controller=row['Controller'],
                dram=row['DRAM'],
                nand_brand=row['NAND Brand'],
                nand_type=row['NAND Type'],
                read_speed_mbps=read_speed,
                write_speed_mbps=write_speed,
                categories=row['Categories']
            )
            ssd_list.append(ssd)
        except Exception:
            pass