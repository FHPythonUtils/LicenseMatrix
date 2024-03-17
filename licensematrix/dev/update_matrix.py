"""Update the license_matrix.json using https://tldrlegal.com/ and licenselist.txt."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from operator import itemgetter
from pathlib import Path
from time import sleep

import requests
import requests_cache

# pylint: disable=invalid-name

# Give the endpoint a chance to breathe
requests_cache.install_cache("update_matrix", "sqlite", 60 * 60 * 24)

THISDIR = Path(__file__).resolve().parent
SPDX = json.loads(Path(THISDIR / "spdx.json").read_text(encoding="utf-8"))["licenses"]

licenseMat = {}

# Grab ~50 licenses from tldrlegal
for line in Path(THISDIR / "licenselist.txt").read_text(encoding="utf-8").splitlines(False):
	# Find the json containing all of the data we need
	r = requests.get(line.strip())
	p = re.compile(r"<a class=\"btn\" href=\"(.*?)\">View as JSON<\/a>", re.MULTILINE)
	api = p.findall(r.content.decode("utf-8"))
	# Grab the data (incl. tags)
	data = requests.get("https://tldrlegal.com/" + api[0]).json()
	tags = [tag["title"] for tag in data["tags"]]
	modules = data["modules"]
	# Calculate the type of license from tags and the description
	licenseType = None
	if "Permissive" in tags or "permissive" in modules["summary"]["text"].lower():
		licenseType = "Permissive"
	elif "Viral" in tags or "viral" in modules["summary"]["text"].lower():
		licenseType = "Viral"
	elif "Weak Copyleft" in tags or "weak copy" in modules["summary"]["text"].lower():
		licenseType = "Weak Copyleft"
	elif "Public Domain" in tags or "public dom" in modules["summary"]["text"].lower():
		licenseType = "Public Domain"
	elif "Weak Copyleft" in tags or "copyleft" in modules["summary"]["text"].lower():
		licenseType = "Copyleft"
	# Rules: must, cannot, can
	must = [mod["attribute"]["title"] for mod in modules["summary"]["must"]]
	cannot = [mod["attribute"]["title"] for mod in modules["summary"]["cannot"]]
	can = [mod["attribute"]["title"] for mod in modules["summary"]["can"]]
	# Lookup the spdx id
	spdx = None
	similarity = []
	for spdxLicense in SPDX:
		similarity.append(
			(
				SequenceMatcher(
					None, data["slug"].replace("-", " "), spdxLicense["name"].lower()
				).ratio(),
				spdxLicense["licenseId"],
			)
		)
	spdx = max(similarity, key=itemgetter(0))[1]
	# Append the license data to the python dict
	if spdx in licenseMat:  # If this happens then manual checking required
		licenseMat[spdx + "_CHK"] = licenseMat[spdx]
		licenseMat.pop(spdx)
		spdx += "_CHK_DUP"
	licenseMat[spdx] = {
		"name": data["title"],
		"altnames": [data["slug"]] + ([data["shorthand"]] if "shorthand" in data else []),
		"tags": tags,
		"must": must,
		"cannot": cannot,
		"can": can,
		"type": licenseType,
		"spdx": spdx,
	}
	# Give the endpoint a chance to breathe
	sleep(0)

# Enrich with licenses from embarkStudios
r = re.compile(r"\(.*?\"(.*?)\",.*?r#\"(.*?)\"#,(.*?)\),", re.S)
licenseList = r.findall(Path(THISDIR / "embarkStudios.rb").read_text(encoding="utf-8"))

for lice in licenseList:
	if lice[0] not in licenseMat:
		tags = lice[2].strip().split("|")
		_ = tags.remove("0x0,") if "0x0," in tags else None
		_ = tags.remove("0x0") if "0x0" in tags else None
		tag_map = {
			"IS_OSI_APPROVED": "OSI-Approved",
			"IS_FSF_LIBRE": "FSF-Libre",
			"IS_DEPRECATED": "Deprecated",
			"IS_COPYLEFT": "Copyleft",
			"IS_GNU": "GNU",
		}
		newTags = []
		for tag in tags:
			newTags.append(tag_map[tag.strip().replace(",", "")])
		if "Copyleft" not in newTags:
			newTags.append("Permissive")
		typeIn = "Permissive" if "Permissive" in newTags else "Copyleft"
		if lice[0].lower().startswith("lgpl"):
			typeIn = "Weak Copyleft"
		licenseMat[lice[0]] = {
			"name": lice[1],
			"altnames": [],
			"tags": newTags,
			"must": None,
			"cannot": None,
			"can": None,
			"type": typeIn,
			"spdx": lice[0],
		}

# Enrich with pypi classifiers
CLASSIFIERS = json.loads(Path(THISDIR / "pypi_classifiers.json").read_text(encoding="utf-8"))

for spdx, value in licenseMat.items():
	if spdx in CLASSIFIERS:
		value["altnames"].extend(CLASSIFIERS[spdx]["altnames"] + [CLASSIFIERS[spdx]["name"]])

# Write to file
Path(THISDIR / "license_matrix.json").write_text(
	json.dumps(licenseMat, indent="\t"), encoding="utf-8"
)
