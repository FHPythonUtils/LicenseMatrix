# LicenseMatrix

[Licensematrix Index](../README.md#licensematrix-index) / [Licensematrix](./index.md#licensematrix) / LicenseMatrix

> Auto-generated documentation for [licensematrix.license_matrix](../../../licensematrix/license_matrix.py) module.

- [LicenseMatrix](#licensematrix)
  - [LicenseMatrix](#licensematrix-1)
    - [LicenseMatrix().buildLicenses](#licensematrix()buildlicenses)
    - [LicenseMatrix().closestSPDX](#licensematrix()closestspdx)
    - [LicenseMatrix().closestTitle](#licensematrix()closesttitle)
    - [LicenseMatrix().licenseFromAltName](#licensematrix()licensefromaltname)
    - [LicenseMatrix().licenseFromName](#licensematrix()licensefromname)
    - [LicenseMatrix().licenseFromSPDX](#licensematrix()licensefromspdx)
    - [LicenseMatrix().searchLicenses](#licensematrix()searchlicenses)

## LicenseMatrix

[Show source in license_matrix.py:15](../../../licensematrix/license_matrix.py#L15)

Make a list of Licenses from a json file.

#### Signature

```python
class LicenseMatrix:
    def __init__(self) -> None: ...
```

### LicenseMatrix().buildLicenses

[Show source in license_matrix.py:24](../../../licensematrix/license_matrix.py#L24)

Generate a list of licenses from a specified license_matrix...

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

#### Arguments

----
 - `fileName` *str, optional* - the file path to process. Defaults to THISDIR+"/license_matrix.json".

#### Returns

-------
 - `list[License]` - list of Licenses

#### Signature

```python
def buildLicenses(
    self, fileName: str = str(THISDIR / "license_matrix.json")
) -> list[License]: ...
```

#### See also

- [License](./license_type.md#license)

### LicenseMatrix().closestSPDX

[Show source in license_matrix.py:150](../../../licensematrix/license_matrix.py#L150)

Guarantee a license from a spdx id (may be inaccurate).

#### Arguments

----
 - `spdx` *str* - spdx id to lookup

#### Returns

-------
 - `License` - license

#### Signature

```python
def closestSPDX(self, spdx: str) -> License: ...
```

#### See also

- [License](./license_type.md#license)

### LicenseMatrix().closestTitle

[Show source in license_matrix.py:167](../../../licensematrix/license_matrix.py#L167)

Guarantee a license from a name (may be inaccurate).

#### Arguments

----
 - `name` *str* - name to lookup

#### Returns

-------
 - `License` - license

#### Signature

```python
def closestTitle(self, name: str) -> License: ...
```

#### See also

- [License](./license_type.md#license)

### LicenseMatrix().licenseFromAltName

[Show source in license_matrix.py:109](../../../licensematrix/license_matrix.py#L109)

Get the license from an altName.

#### Arguments

----
 - `altName` *str* - altName to lookup

#### Returns

-------
 - `Optional[License]` - license

#### Signature

```python
def licenseFromAltName(self, altName: str) -> License | None: ...
```

### LicenseMatrix().licenseFromName

[Show source in license_matrix.py:92](../../../licensematrix/license_matrix.py#L92)

Get the license from a name.

#### Arguments

----
 - `name` *str* - name to lookup

#### Returns

-------
 - `Optional[License]` - license

#### Signature

```python
def licenseFromName(self, name: str) -> License | None: ...
```

### LicenseMatrix().licenseFromSPDX

[Show source in license_matrix.py:75](../../../licensematrix/license_matrix.py#L75)

Get the license from a spdx id.

#### Arguments

----
 - `spdx` *str* - spdx id to lookup

#### Returns

-------
 - `Optional[License]` - license

#### Signature

```python
def licenseFromSPDX(self, spdx: str) -> License | None: ...
```

### LicenseMatrix().searchLicenses

[Show source in license_matrix.py:127](../../../licensematrix/license_matrix.py#L127)

Get a list of candidate licenses from a search string.

#### Arguments

----
 - `search` *str* - search string

#### Returns

-------
 - `list[License]` - list of licenses

#### Signature

```python
def searchLicenses(self, search: str) -> list[License]: ...
```

#### See also

- [License](./license_type.md#license)