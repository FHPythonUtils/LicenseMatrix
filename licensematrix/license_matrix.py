"""Make a list of Licenses from a json file."""

from __future__ import annotations

import json
from difflib import SequenceMatcher
from operator import itemgetter
from pathlib import Path

from licensematrix.license_type import License

THISDIR = Path(__file__).resolve().parent


class LicenseMatrix:
	"""Make a list of Licenses from a json file."""

	__slots__ = ["licenses"]

	def __init__(self) -> None:
		"""Make a list of Licenses from a json file."""
		self.licenses = self.buildLicenses()

	def buildLicenses(self, fileName: str = str(THISDIR / "license_matrix.json")) -> list[License]:
		"""Generate a list of licenses from a specified license_matrix...

		Use license_matrix.json (part of the project) by default. Json format is:

		```json
		"MIT": {
			"name": "MIT License (Expat)",
			"altnames": [
				"mit-license",
				"mit",
				"mit license",
				"osi approved :: mit license",
				"License :: OSI Approved :: MIT License"
			],
			"tags": [
				"Open Source",
				"OSI-Approved",
				"Permissive"
			],
			"must": [
				"Include Copyright",
				"Include License"
			],
			"cannot": [
				"Hold Liable"
			],
			"can": [
				"Commercial Use",
				"Modify",
				"Distribute",
				"Sublicense",
				"Private Use"
			],
			"type": "Permissive",
			"spdx": "MIT"
		},
		```

		Args:
		----
			fileName (str, optional): the file path to process. Defaults to THISDIR+"/license_matrix.json".

		Returns:
		-------
			list[License]: list of Licenses

		"""
		matrixDict = json.loads(Path(fileName).read_text(encoding="utf-8"))
		return [License(matrixDict[lice]["name"], fromDict=matrixDict[lice]) for lice in matrixDict]

	def licenseFromSPDX(self, spdx: str) -> License | None:
		"""Get the license from a spdx id.

		Args:
		----
			spdx (str): spdx id to lookup

		Returns:
		-------
			Optional[License]: license

		"""
		for lice in self.licenses:
			if spdx.lower() == lice.spdx.lower():
				return lice
		return None

	def licenseFromName(self, name: str) -> License | None:
		"""Get the license from a name.

		Args:
		----
			name (str): name to lookup

		Returns:
		-------
			Optional[License]: license

		"""
		for lice in self.licenses:
			if name.lower() == lice.name.lower():
				return lice
		return None

	def licenseFromAltName(self, altName: str) -> License | None:
		"""Get the license from an altName.

		Args:
		----
			altName (str): altName to lookup

		Returns:
		-------
			Optional[License]: license

		"""
		for lice in self.licenses:
			for name in lice.altNames:
				if altName.lower() == name.lower():
					return lice
		return None

	def searchLicenses(self, search: str) -> list[License]:
		"""Get a list of candidate licenses from a search string.

		Args:
		----
			search (str): search string

		Returns:
		-------
			list[License]: list of licenses

		"""
		search = search.lower()
		licenses = []
		for lice in self.licenses:
			if (
				search in lice.name.lower()
				or search in "\t".join(lice.altNames).lower()
				or search in lice.spdx.lower()
			):
				licenses.append(lice)
		return licenses

	def closestSPDX(self, spdx: str) -> License:
		"""Guarantee a license from a spdx id (may be inaccurate).

		Args:
		----
			spdx (str): spdx id to lookup

		Returns:
		-------
			License: license

		"""
		licenses = []
		for lice in self.licenses:
			licenses.append((SequenceMatcher(None, spdx.lower(), lice.spdx.lower()).ratio(), lice))
		return max(licenses, key=itemgetter(0))[1]

	def closestTitle(self, name: str) -> License:
		"""Guarantee a license from a name (may be inaccurate).

		Args:
		----
			name (str): name to lookup

		Returns:
		-------
			License: license

		"""
		licenses = []
		for lice in self.licenses:
			licenses.append((SequenceMatcher(None, name.lower(), lice.name.lower()).ratio(), lice))
		return max(licenses, key=itemgetter(0))[1]
