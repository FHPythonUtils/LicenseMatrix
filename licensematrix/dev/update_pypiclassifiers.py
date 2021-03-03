"""Update the pypi_classifiers.json.
"""

from difflib import SequenceMatcher
from operator import itemgetter
from pathlib import Path
from time import sleep

import regex
import requests
import requests_cache

try:
	import ujson as json
except ImportError:
	import json

# pylint: disable=invalid-name

# Give the endpoint a chance to breathe
requests_cache.install_cache("update_matrix", "sqlite", 60 * 60 * 24)

THISDIR = Path(__file__).resolve().parent
with open(THISDIR / "spdx.json") as spdxFile:
	SPDX = json.load(spdxFile)["licenses"]

classifiers = {}

# Grab ~50 licenses from tldrlegal
with open(THISDIR / "pypiclassifiers.txt") as licenseList:
	for line in licenseList.readlines():
		line = line.strip()
		spdx = None
		similarity = []
		parts = line.lower().split(" :: ")
		r = regex.compile(r".*?\((.*?)\)")
		pypiShortName = r.findall(parts[-1])
		altNames = [parts[-1]] + ([" :: ".join(parts[1:])] if len(parts) > 2 else
		[]) + ([pypiShortName[0]] if len(pypiShortName) > 0 else [])
		for spdxLicense in SPDX:
			similarity.append((SequenceMatcher(None,
			parts[-1],
			spdxLicense["name"].lower()).ratio(),
			spdxLicense["licenseId"]))
		spdx = max(similarity, key=itemgetter(0))[1]
		# Append the license data to the python dict
		if spdx in classifiers: # If this happens then manual checking required
			classifiers[spdx + "_CHK"] = classifiers[spdx]
			classifiers[spdx + "_CHK"]["altnames"].extend(altNames)
			classifiers.pop(spdx)
		else:
			classifiers[spdx] = {"spdx": spdx, "name": line, "altnames": altNames}

json.dump(classifiers, open(THISDIR / "pypi_classifiers.json", "w"))
