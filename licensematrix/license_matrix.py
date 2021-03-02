"""Make a list of Licenses from a json file.
"""
from __future__ import annotations

from difflib import SequenceMatcher
from json import load
from operator import itemgetter
from pathlib import Path
from typing import Optional

from .license_type import License

THISDIR = str(Path(__file__).resolve().parent)


class LicenseMatrix():
	"""Make a list of Licenses from a json file.
	"""
	def __init__(self):
		"""Make a list of Licenses from a json file.
		"""
		self.licenses = self.buildLicenses()

	def buildLicenses(self,
	fileName: str = THISDIR + "/license_matrix.json") -> list[License]: # yapf: disable
		"""Generate a list of licenses from a specified license_matrix...

		Use license_matrix.json (part of the project) by default. Json format is:

		```json
		{
			"mit-license": {
				"title": "MIT License (Expat)",
				"short": "mit",
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
		}
		```

		Args:
			fileName (str, optional): the file path to process. Defaults to THISDIR+"/license_matrix.json".

		Returns:
			list[License]: list of Licenses
		"""
		licenses = []
		with open(fileName, encoding="utf-8") as matrix:
			matrixDict = load(matrix)
			for lice in matrixDict:
				licenses.append(License(lice, fromDict=matrixDict[lice]))
		return licenses

	def licenseFormSPDX(self, spdx: str) -> Optional[License]:
		"""Get the license from a spdx id.

		Args:
			spdx (str): spdx id to lookup

		Returns:
			Optional[License]: license
		"""
		for lice in self.licenses:
			if spdx == lice.spdx:
				return lice
		return None

	def licenseFromTitle(self, title: str) -> Optional[License]:
		"""Get the license from a title.

		Args:
			title (str): title to lookup

		Returns:
			Optional[License]: license
		"""
		for lice in self.licenses:
			if title == lice.title:
				return lice
		return None

	def searchLicenses(self, search: str) -> list[License]:
		"""Get a list of candidate licenses from a search string.

		Args:
			search (str): search string

		Returns:
			list[License]: list of licenses
		"""
		search = search.lower()
		licenses = []
		for lice in self.licenses:
			if (search in lice.name.lower() or search in lice.shortName.lower()
			or search in lice.spdx.lower()):
				licenses.append(lice)
		return licenses

	def closestSPDX(self, spdx: str) -> License:
		"""Guarantee a license from a spdx id (may be inaccurate).

		Args:
			spdx (str): spdx id to lookup

		Returns:
			License: license
		"""
		licenses = []
		for lice in self.licenses:
			licenses.append((SequenceMatcher(None, spdx.lower(),
			lice.spdx.lower()).ratio(), lice))
		return max(licenses, key=itemgetter(0))[1]

	def closestTitle(self, title: str) -> License:
		"""Guarantee a license from a title (may be inaccurate).

		Args:
			title (str): title to lookup

		Returns:
			License: license
		"""
		licenses = []
		for lice in self.licenses:
			licenses.append((SequenceMatcher(None, title.lower(),
			lice.title.lower()).ratio(), lice))
		return max(licenses, key=itemgetter(0))[1]
