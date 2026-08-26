"""
Generates Prusawire profiles from the Voron Switchwire profiles.
The only major difference between the Voron Switchwire and Prusawire is the max build height.
Some additional properties are set based on the Prusa MK4S, such as matching temperatures and disabling skirts.

Usage: python3 generate-profiles-prusaslicer.py
"""

import configparser
import os
import tempfile
import urllib.request

# URL of the source Voron profiles to generate from.
# Make sure this URL starts with "raw.githubusercontent", otherwise it might download an HTML page.
sourceUrl = "https://raw.githubusercontent.com/prusa3d/PrusaSlicer-settings-non-prusa-fff/refs/heads/main/Voron/3.0.0.ini"

# Keys are strings to find (section names, section values). Values are the strings to replace with.
# In dictionaries, order is not guaranteed. Be careful of replaced values disrupting other keys!
replaceStrings = {
    "VORON Switchwire": "Prusawire",
    "Voron": "Prusawire",
    "VORON_SWITCHWIRE": "PRUSAWIRE",
    ":VS_MK52": ":Prusawire",
    "@SWITCHWIRE": "@PRUSAWIRE",
    "@VORON2": "@VORON2_PRUSAWIRE_INHERITED", # Must be different to import, otherwise they are duplicates.
    "printer_model=~/(V2_250|V2_300|V2_350|VT_250|VT_300|VT_350|V0_120|VS_MK52)/ and ": "",
}

# Keys are the profiles names. Values are dictionaries with the property names to set with the given values.
# They will always be set, even if it isn't present otherwise.
# The profile names must be the section name in the final name (ex: printer:Prusawire, not printer:VORON Switchwire)
replacePropertiesBySection = {
    "printer_model:Prusawire": {
        "bed_model": "prusawire_build_plate.stl",
        "bed_texture": "prusawire_texture.svg",
        "thumbnail": "thumbnail_prusawire.png",
    },
    "print:*common*": {
        "skirts": "0",
    },
    "printer:*VSW_COMMON*": {
        "max_print_height": "180",
    },
    "printer:Prusawire - 0.4mm Nozzle (High Flow)": {
        "printer_model": "Prusawire",
    },
    "printer:Prusawire - 0.25mm Nozzle": {
        "printer_model": "Prusawire",
    },
    "filament:*PETG*": {
        "first_layer_temperature": "250",
        "temperature": "250",
        "first_layer_bed_temperature": "85",
        "bed_temperature": "90",
    },
    "filament:*PLA*": {
        "first_layer_temperature": "230",
        "temperature": "225",
        "first_layer_bed_temperature": "60",
        "bed_temperature": "60",
    },
}


def replaceString(source: str) -> str:
    """Replaces parts of the given string with new values.

    :param source: Source string to replace.
    :return: Replaced string.
    """

    for replaceString in replaceStrings.keys():
        source = source.replace(replaceString, replaceStrings[replaceString])
    return source


# Download the source profiles file.
sourceProfilesLocation = os.path.join(tempfile.gettempdir(), "VoronPrusaSlicerProfiles_" + os.path.basename(sourceUrl))
targetProfilesLocation = os.path.join(os.path.dirname(__file__), "..", "Slicer Profiles", "PrusaSlicer", "prusaslicer_config_bundle.ini")
if not os.path.exists(sourceProfilesLocation):
    request = urllib.request.Request(sourceUrl)
    sourceProfilesData = urllib.request.urlopen(request).read() # Fetched before opening file to avoid creating an empty file on error.
    with open(sourceProfilesLocation, "wb") as file:
        file.write(sourceProfilesData)

# Read the profiles file.
profiles = configparser.ConfigParser(interpolation=None)
profiles.read(sourceProfilesLocation)

# Create the initial nodes of the graph for what references what.
# Sections are able to reference (inherit) other sections.
# This makes it easier to determine what is needed instead of doing many iterations.
referencedSections = {}
for sectionName in profiles.sections():
    referencedSections[sectionName] = {
        "references": set(),
        "referenced": set(),
    }

# Add the referenced sections.
for sectionName in profiles.sections():
    sectionType = sectionName.split(":")[0]
    section = profiles[sectionName]

    # Add inherited sections.
    if "inherits" in section.keys():
        for inheritedSection in section["inherits"].split(";"):
            fullInheritedSection = sectionType + ":" + inheritedSection.strip()
            referencedSections[sectionName]["references"].add(fullInheritedSection)
            referencedSections[fullInheritedSection]["referenced"].add(sectionName)

    # Add printer models.
    if "printer_model" in section.keys():
        printerModelSection = "printer_model:" + section["printer_model"]
        referencedSections[sectionName]["references"].add(printerModelSection)
        referencedSections[printerModelSection]["referenced"].add(sectionName)

    # Add filaments.
    # This doesn't properly evaluate the expression, but currently, it is a check if the printer model is in the set.
    if "compatible_printers_condition" in section.keys():
        printerModelSection = "printer_model:VS_MK52"
        if "VS_MK52" not in section["compatible_printers_condition"] and "VORON_SWITCHWIRE" not in section["compatible_printers_condition"]:
            continue
        referencedSections[sectionName]["references"].add(printerModelSection)
        referencedSections[printerModelSection]["referenced"].add(sectionName)

# Determine the sections to keep.
# This is done by starting at VS_MK52 (base for the Switchwire) going down, and then going up for anything referenced.
# Both directions aren't done at once due to going up to common sections and back down to unrelated printers (V0, V2, Trident).
sectionNamesToKeep = set()
sectionNamesToCheck = ["printer_model:VS_MK52"]
while len(sectionNamesToCheck) > 0:
    sectionNameToCheck = sectionNamesToCheck.pop()
    sectionNamesToKeep.add(sectionNameToCheck)

    for referencedSectionName in referencedSections[sectionNameToCheck]["referenced"]:
        sectionNamesToCheck.append(referencedSectionName)

sectionNamesToCheck = list(sectionNamesToKeep)
while len(sectionNamesToCheck) > 0:
    sectionNameToCheck = sectionNamesToCheck.pop()
    sectionNamesToKeep.add(sectionNameToCheck)

    for referencedSectionName in referencedSections[sectionNameToCheck]["references"]:
        sectionNamesToCheck.append(referencedSectionName)

# Recreate the config with the sections to keep.
outputProfiles = configparser.ConfigParser(interpolation=None)
for sectionName in profiles.sections():
    # Add the section.
    if sectionName not in sectionNamesToKeep:
        continue
    newSectionName = replaceString(sectionName)
    outputProfiles.add_section(newSectionName)

    # Get the properties to replace for the section.
    replaceProperties = {}
    if newSectionName in replacePropertiesBySection.keys():
        replaceProperties = replacePropertiesBySection[newSectionName]

    # Populate the section.
    section = profiles[sectionName]
    for key in section.keys():
        if key in replaceProperties.keys():
            outputProfiles[newSectionName][key] = replaceProperties[key]
        else:
            outputProfiles[newSectionName][key] = replaceString(section[key])
    for key in replaceProperties.keys():
        if key not in section.keys():
            outputProfiles[newSectionName][key] = replaceProperties[key]

# Write the profiles.
with open(targetProfilesLocation, "w", encoding="utf8") as file:
    outputProfiles.write(file)
