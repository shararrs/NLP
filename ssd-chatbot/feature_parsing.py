import re
import parsing
import json
from csv_parser import SSD, capacity_gb_to_str


class SSDRequirements:
    """SSD Specs desired by the user"""

    def __init__(self):
        self.capacity_requirement = 0
        self.read_speed_requirement = 0
        self.write_speed_requirement = 0
        self.nn_requirements: dict[str, str] = {}
        self.dram_requirement = 0

    def set_capacity_requirement(self, capacity_gb):
        self.capacity_requirement = capacity_gb

    def set_read_speed_requirement(self, read_speed_mbps):
        self.read_speed_requirement = read_speed_mbps

    def set_write_speed_requirement(self, write_speed_mbps):
        self.write_speed_requirement = write_speed_mbps

    def set_dram_requirement(self, should_have_dram: bool):
        self.dram_requirement = "Yes" if should_have_dram else "No"

    def set_nn_requirement(self, *, key="category", value):
        self.nn_requirements[key.lower()] = value.lower()

    def filter(self, ssds: list[SSD]):
        """Given a list of SSDs, return a list of only those which meet the requirements"""
        return [
            ssd
            for ssd in ssds
            if ssd.capacity >= self.capacity_requirement and
               ssd.read_speed_mbps >= self.read_speed_requirement and
               ssd.write_speed_mbps >= self.write_speed_requirement and
               (not self.dram_requirement or ssd.dram == self.dram_requirement) and
               all((
                   value.lower() in ssd.get_nn_specs()[key.lower()].lower()
                   for key, value in self.nn_requirements.items()
               ))
        ]

    def __str__(self):
        requirements = []
        if self.capacity_requirement:
            requirements.append(f"Capacity of {capacity_gb_to_str(self.capacity_requirement)}")
        if self.read_speed_requirement:
            requirements.append(f"Read speed of {self.read_speed_requirement} MBps")
        if self.write_speed_requirement:
            requirements.append(f"Write speed of {self.write_speed_requirement} MBps")
        if self.dram_requirement:
            requirements.append(f"DRAM: {self.dram_requirement}")
        for key, value in self.nn_requirements.items():
            requirements.append(f"{key}: {value}")
        return '; '.join(requirements)


def try_parse_float(s: str):
    try:
        return float(s)
    except:
        return 0


# Regular expressions for parsing speed, size, nand
SPEED_REGEX = '([0-9\.]+)\s*(?:(kb|mb|gb|tb|kil.byte|meg.byte|gig+.byte|ter+.byte|gig|megabit|kilobit|gigabit)s? *(per|a|\/|p)\s*(s(ec(ond)?)?))'
SIZE_REGEX = '([0-9\.]+)\s*(gb|tb|gig+abyte|ter+abyte|gig)s?'
NAND_TYPE_REGEX = '[t|q]lc'


# Preprocess by substituting speed, size, and NAND expressions
def feature_preprocessor(query: str, value_dict=None) -> str:
    query = query.lower()

    if value_dict is None:
        value_dict = {}

    speed_result = re.search(SPEED_REGEX, query)
    if speed_result:
        query = re.sub(SPEED_REGEX, '$speed', query)
        speed, unit = try_parse_float(speed_result.group(1)), speed_result.group(2)
        value_dict['$speed'] = speed * (1000 if unit.startswith('g') else 1)

    size_result = re.search(SIZE_REGEX, query)
    if size_result:
        query = re.sub(SIZE_REGEX, '$size', query)
        size, unit = try_parse_float(size_result.group(1)), size_result.group(2)
        value_dict['$size'] = size * (1000 if unit.startswith('t') else 1)

    # finding nand type (QLC or TLC)
    nand_type = re.search(NAND_TYPE_REGEX, query)
    if nand_type:
        query = re.sub(NAND_TYPE_REGEX, '$nand', query)
        type = nand_type.group(0)
        value_dict['$nand'] = type


    parsing.main_preprocessor(query)
    return query


# Train the intent extractor for SSD features
feature_intent_extractor = parsing.IntentExtractor(feature_preprocessor)
with open('feature-queries.json', 'r') as feature_queries_file:
    feature_intents = json.loads(feature_queries_file.read())
    for intent, queries in feature_intents.items():
        feature_intent_extractor.add_intent(intent, queries)
feature_intent_extractor.train()


