"""Update the license_matrix.json using https://tldrlegal.com/ and licenselist.txt.
"""

from difflib import SequenceMatcher
from operator import itemgetter
from pathlib import Path
from time import sleep

import regex
import requests

try:
	import ujson as json
except ImportError:
	import json

# pylint: disable=invalid-name

THISDIR = Path(__file__).resolve().parent
with open(THISDIR / "spdx.json") as spdxFile:
	SPDX = json.load(spdxFile)["licenses"]

license_mat = {}
with open(THISDIR / "licenselist.txt") as licenseList:
	for line in licenseList.readlines():
		# Find the json containing all of the data we need
		r = requests.get(line.strip())
		p = regex.compile(r"<a class=\"btn\" href=\"(.*?)\">View as JSON<\/a>",
		regex.MULTILINE)
		api = p.findall(r.content.decode("utf-8"))
		# Grab the data (incl. tags)
		data = requests.get("https://tldrlegal.com/" + api[0]).json()
		tags = [tag["title"] for tag in data["tags"]]
		modules = data["modules"]
		# Calculate the type of license from tags and the description
		licenseType = None
		if "Permissive" in tags or "permissive" in modules["summary"]["text"].lower(
		):
			licenseType = "Permissive"
		elif "Viral" in tags or "viral" in modules["summary"]["text"].lower():
			licenseType = "Viral"
		elif "Copyleft" in tags or "copyleft" in modules["summary"]["text"].lower():
			licenseType = "Copyleft"
		elif "Public Domain" in tags or "public dom" in modules["summary"][
		"text"].lower():
			licenseType = "Public Domain"
		elif "Weak Copyleft" in tags or "weak copy" in modules["summary"][
		"text"].lower():
			licenseType = "Weak Copyleft"
		# Rules: must, cannot, can
		must = [must["attribute"]["title"] for must in modules["summary"]["must"]]
		cannot = [
		must["attribute"]["title"] for must in modules["summary"]["cannot"]]
		can = [must["attribute"]["title"] for must in modules["summary"]["can"]]
		# Lookup the spdx id
		spdx = None
		similarity = []
		for spdxLicense in SPDX:
			similarity.append((SequenceMatcher(None, data["slug"].replace("-", " "),
			spdxLicense["name"].lower()).ratio(), spdxLicense["licenseId"]))
		spdx = max(similarity, key=itemgetter(0))[1]
		# Append the license data to the python dict
		license_mat[data["slug"]] = {
		"title": data["title"], "short": data["shorthand"]
		if "shorthand" in data else data["slug"], "tags": tags, "must": must,
		"cannot": cannot, "can": can, "type": licenseType, "spdx": spdx}
		# Give the endpoint a chance to breathe
		sleep(2)

# Write to file
json.dump(license_mat, open(THISDIR / "license_matrix.json", "w"))
