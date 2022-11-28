import urllib.request
import re
from googlesearch import get_google_results


# extracts website name from an url
def get_domain_name(url):
    text = url
    try:
        found = re.search('www.([A-Za-z]+).com', text).group(1)
    except AttributeError:
        found = 'default'  # error handled by making ir return default
    return found


# Parses html file to find the ssd spec requirements
def ssd_type(filename):
    # 3 Types of ssd, also the search terms "NVMe (PCIe Gen 4 x4)", "NVMe (PCIe Gen 3 x4)","Sata 2.5\""

    with open(filename, 'r') as data:
        for line in data.readlines():
            if "NVMe (PCIe Gen 4 x4)" in line:
                return "x4 PCIe 4.0/NVMe", "M.2"
            elif "NVMe (PCIe Gen 3 x4)" in line:
                return "x4 PCIe 3.0/NVMe", "M.2"
        return "SATA/AHCI", "2.5\""


# This creates a copy (Only html) of the crucial site containing the specification
def get_laptop_spec_from_url(url):
    filename = get_domain_name(url) + '.txt'
    urllib.request.urlretrieve(url, filename)
    ssd = ssd_type(filename)
    return ssd


def get_laptop_spec(model):
    """google search to get the ssd info."""

    for url in get_google_results(model + " storage specs crucial"):
        if get_domain_name(url) != "crucial":
            continue
        interface, form_factor = get_laptop_spec_from_url(url)
        return interface, form_factor

    return 'SATA/AHCI', '2.5"'
