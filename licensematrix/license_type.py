"""Represent a license.

Source: represents an existing license
Dest: represents a new combined license (possibly for a combined work)
"""

from __future__ import annotations

from typing import Any


class License:
	"""Represent a license.

	Source: represents an existing license
	Dest: represents a new combined license (possibly for a combined work)
	"""

	def __init__(
		self,
		name: str = "",
		altNames: list[str] | None = None,
		tags: list[str] | None = None,
		must: list[str] | None = None,
		cannot: list[str] | None = None,
		can: list[str] | None = None,
		typeIn: str = "",
		spdx: str = "",
		fromDict: dict[str, Any] | None = None,
	) -> None:
		"""Construct License. Create from a dict of 'by hand'.

		Args:
		----
			name (str, optional): name. Defaults to "".
			tags (Optional[list[str]], optional): list of alt names.
			Defaults to None.
			tags (Optional[list[str]], optional): list of attributes.
			Defaults to None.
			must (Optional[list[str]], optional): list of requirements.
			Defaults to None.
			cannot (Optional[list[str]], optional): list of things you
			cannot do. Defaults to None.
			can (Optional[list[str]], optional): list of things the license
			allows you to do. Defaults to None.
			typeIn (str, optional): the type of license. Defaults to "".
			spdx (str, optional): the spdx id for the license. Defaults to "".
			fromDict (Optional[dict[str, Any]], optional): create from dict.
			Defaults to None.

		"""
		self.name = name
		self.altNames = altNames if altNames is not None else []
		self.tags = tags if tags is not None else []
		self.must = must if must is not None else []
		self.cannot = cannot if cannot is not None else []
		self.can = can if can is not None else []
		self.type = typeIn
		self.spdx = spdx
		if fromDict is not None:
			self.altNames = fromDict["altnames"]
			self.tags = (
				list(set([fromDict["type"]] + fromDict["tags"]))
				if fromDict["type"] is not None
				else fromDict["tags"]
			)
			self.must = fromDict["must"]
			self.cannot = fromDict["cannot"]
			self.can = fromDict["can"]
			self.type = fromDict["type"] if fromDict["type"] is not None else ""
			self.spdx = fromDict["spdx"] if fromDict["spdx"] is not None else ""

	def __repr__(self) -> str:
		"""Get the string representation."""
		return self.__str__()

	def __str__(self) -> str:
		"""To string."""
		return f"<{self.name} type:{self.type} spdx:{self.spdx}>"

	def isPermissive(self):
		"""Is the License Permissive?."""
		return self.type == "Permissive"

	def isWeakCopyleft(self):
		"""Is the License Weak Copyleft?."""
		return self.type == "Weak Copyleft"

	def isCopyleft(self):
		"""Is the License Copyleft?."""
		return self.type == "Copyleft"

	def isViral(self):
		"""Is the License Viral?."""
		return self.type == "Viral"

	def isPublicDomain(self):
		"""Is the License Public Domain?."""
		return self.type == "Public Domain"

	def mergeBoth(self, rhs: License):
		"""Combine two licenses into one super license.

		Performs no checks on compatibility, this is up to the user.

		Args:
		----
			rhs (License): the other license to merge

		Returns:
		-------
			License: the new, combined license

		"""
		return License(
			self.name + "+" + rhs.name,
			self.altNames + rhs.altNames,
			list(set(self.tags + rhs.tags)),
			list(set(self.must + rhs.must)),
			list(set(self.cannot + rhs.cannot)),
			list(set(self.can + rhs.can)),
			getMostStrictType(self.type, rhs.type),
			mergeSPDX(self.spdx, rhs.spdx),
		)

	def mergeIntoDest(self, dest: License):
		"""Combine two licenses into one super license, but preserve the...

		destination name. Performs no checks on compatibility, this is up to the user.

		Args:
		----
			dest (License): the other license to merge

		Returns:
		-------
			License: the new, combined license

		"""
		return License(
			dest.name,
			dest.altNames,
			list(set(self.tags + dest.tags)),
			list(set(self.must + dest.must)),
			list(set(self.cannot + dest.cannot)),
			list(set(self.can + dest.can)),
			getMostStrictType(self.type, dest.type),
			mergeSPDX(self.spdx, dest.spdx),
		)

	def termsCompatible(self, dest: License) -> bool:
		"""Check the destination terms (rhs) are compatible with the source license terms (self).

		Args:
		----
			dest (License): the destination license

		Returns:
		-------
			bool: are the license terms compatible?

		"""
		# If any of must is under cannot?
		if (
			self.must is not None
			and dest.cannot is not None
			and len(set(self.must).intersection(dest.cannot)) > 0
		):
			return False
		if (
			self.cannot is not None
			and dest.must is not None
			and len(set(self.cannot).intersection(dest.must)) > 0
		):
			return False
		return True

	def naiveCompatSourceLinking(self, dest: License) -> bool:
		"""Check the destination (rhs) is compatible with the source license (self).

		For linking licenses

		Args:
		----
			dest (License): the destination license

		Returns:
		-------
			bool: are the licenses compatible?

		"""
		strict = ["Public Domain", "Permissive", "Weak Copyleft", "Copyleft", "Viral"]
		if strict.index(dest.type) > 2:  # if the dest license is Copyleft/ Viral then unlikely
			return False
		if dest.isViral() and not equal(self, dest):
			return False
		if not self.termsCompatible(dest):
			return False
		return True

	def naiveCompatSource(self, dest: License) -> bool:
		"""Check the destination (rhs) is compatible with the source license (self).

		Args:
		----
			dest (License): the destination license

		Returns:
		-------
			bool: are the licenses compatible?

		"""
		strict = ["Public Domain", "Permissive", "Weak Copyleft", "Copyleft", "Viral"]
		if strict.index(self.type) < strict.index(dest.type):
			return False
		if dest.isViral() and not equal(self, dest):
			return False
		if not self.termsCompatible(dest):
			return False
		return True

	def naiveCompatDestLinking(self, dest: License) -> bool:
		"""Check the source (self) is compatible with the destination license (rhs).

		For linking licenses

		Args:
		----
			dest (License): the destination license

		Returns:
		-------
			bool: are the licenses compatible?

		"""
		strict = ["Public Domain", "Permissive", "Weak Copyleft", "Copyleft", "Viral"]
		if strict.index(self.type) > 2:  # if the dest license is Copyleft/ Viral then unlikely
			return False
		if self.isViral() and not equal(self, dest):
			return False
		if not self.termsCompatible(dest):
			return False
		return True

	def naiveCompatDest(self, dest: License) -> bool:
		"""Check the source (self) is compatible with the destination license (rhs).

		Args:
		----
			dest (License): the destination license

		Returns:
		-------
			bool: are the licenses compatible?

		"""
		strict = ["Public Domain", "Permissive", "Weak Copyleft", "Copyleft", "Viral"]
		# If the source has a more restrictive license then the derivative work
		# must be relicensed
		if strict.index(self.type) > strict.index(dest.type):
			return False
		if self.isViral() and not equal(self, dest):
			return False
		if not self.termsCompatible(dest):
			return False
		return True


def getMostStrictType(typeA: str, typeB: str) -> str:
	"""Return the most 'strict' type of license from the available types.

	Args:
	----
		typeA (str): type of the first license
		typeB (str): type of the second license

	Returns:
	-------
		str: the most 'strict' type

	"""
	strict = ["Public Domain", "Permissive", "Weak Copyleft", "Copyleft", "Viral"]
	if len(typeA) == 0:
		return typeB
	if len(typeB) == 0:
		return typeA
	return strict[max(strict.index(typeA), strict.index(typeB))]


def mergeSPDX(spdxA: str, spdxB: str) -> str:
	"""Combine the spdx ids.

	Args:
	----
		spdxA (str): spdx of the first license
		spdxB (str): spdx of the second license

	Returns:
	-------
		str: combined spdx

	"""
	if len(spdxA) == 0:
		return spdxB
	if len(spdxB) == 0:
		return spdxA
	return spdxA + "+" + spdxB


def equal(licenseA: License, licenseB: License) -> bool:
	"""Are two licenses equal?.

	Args:
	----
		licenseA (License): the first license
		licenseB (License): the second license

	Returns:
	-------
		bool: equal?

	"""
	return licenseA.spdx == licenseB.spdx or licenseA.name == licenseB.name
