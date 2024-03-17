"""Update the pypi_classifiers.json."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from operator import itemgetter
from pathlib import Path

# pylint: disable=invalid-name

THISDIR = Path(__file__).resolve().parent
SPDX = json.loads(Path(THISDIR / "spdx.json").read_text(encoding="utf-8"))["licenses"]

classifiers = {}

# Grab licenses from pypiclassifiers
for line in Path(THISDIR / "pypiclassifiers.txt").read_text(encoding="utf-8").splitlines(False):
	line = line.strip()
	spdx = None
	similarity = []
	parts = line.lower().split(" :: ")
	r = re.compile(r".*?\((.*?)\)")
	pypiShortName = r.findall(parts[-1])
	altNames = (
		[parts[-1]]
		+ ([" :: ".join(parts[1:])] if len(parts) > 2 else [])
		+ ([pypiShortName[0]] if len(pypiShortName) > 0 else [])
	)
	for spdxLicense in SPDX:
		similarity.append(
			(
				SequenceMatcher(None, parts[-1], spdxLicense["name"].lower()).ratio(),
				spdxLicense["licenseId"],
			)
		)
	spdx = max(similarity, key=itemgetter(0))[1]
	# Append the license data to the python dict
	if spdx in classifiers:  # If this happens then manual checking required
		classifiers[spdx + "_CHK"] = classifiers[spdx]
		classifiers[spdx + "_CHK"]["altnames"].extend(altNames)
		classifiers.pop(spdx)
	else:
		classifiers[spdx] = {"spdx": spdx, "name": line, "altnames": altNames}

Path(THISDIR / "pypi_classifiers.json").write_text(
	json.dumps(classifiers, indent="\t"), encoding="utf-8"
)
