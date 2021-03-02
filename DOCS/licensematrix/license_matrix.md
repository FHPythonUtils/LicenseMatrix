# license_matrix

> Auto-generated documentation for [licensematrix.license_matrix](../../licensematrix/license_matrix.py) module.

Make a list of Licenses from a json file.

- [Licensematrix_](../README.md#licensematrix_-index) / [Modules](../README.md#licensematrix_-modules) / [licensematrix](index.md#licensematrix) / license_matrix
    - [LicenseMatrix](#licensematrix)
        - [LicenseMatrix().buildLicenses](#licensematrixbuildlicenses)
        - [LicenseMatrix().closestSPDX](#licensematrixclosestspdx)
        - [LicenseMatrix().closestTitle](#licensematrixclosesttitle)
        - [LicenseMatrix().licenseFormSPDX](#licensematrixlicenseformspdx)
        - [LicenseMatrix().licenseFromTitle](#licensematrixlicensefromtitle)
        - [LicenseMatrix().searchLicenses](#licensematrixsearchlicenses)

## LicenseMatrix

[[find in source code]](../../licensematrix/license_matrix.py#L16)

```python
class LicenseMatrix():
    def __init__():
```

Make a list of Licenses from a json file.

### LicenseMatrix().buildLicenses

[[find in source code]](../../licensematrix/license_matrix.py#L24)

```python
def buildLicenses(
    fileName: str = THISDIR + '/license_matrix.json',
) -> list[License]:
```

Generate a list of licenses from a specified license_matrix...

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

#### Arguments

- `fileName` *str, optional* - the file path to process. Defaults to THISDIR+"/license_matrix.json".

#### Returns

- `list[License]` - list of Licenses

### LicenseMatrix().closestSPDX

[[find in source code]](../../licensematrix/license_matrix.py#L118)

```python
def closestSPDX(spdx: str) -> License:
```

Guarantee a license from a spdx id (may be inaccurate).

#### Arguments

- `spdx` *str* - spdx id to lookup

#### Returns

- `License` - license

#### See also

- [License](license_type.md#license)

### LicenseMatrix().closestTitle

[[find in source code]](../../licensematrix/license_matrix.py#L133)

```python
def closestTitle(title: str) -> License:
```

Guarantee a license from a title (may be inaccurate).

#### Arguments

- `title` *str* - title to lookup

#### Returns

- `License` - license

#### See also

- [License](license_type.md#license)

### LicenseMatrix().licenseFormSPDX

[[find in source code]](../../licensematrix/license_matrix.py#L73)

```python
def licenseFormSPDX(spdx: str) -> Optional[License]:
```

Get the license from a spdx id.

#### Arguments

- `spdx` *str* - spdx id to lookup

#### Returns

- `Optional[License]` - license

### LicenseMatrix().licenseFromTitle

[[find in source code]](../../licensematrix/license_matrix.py#L87)

```python
def licenseFromTitle(title: str) -> Optional[License]:
```

Get the license from a title.

#### Arguments

- `title` *str* - title to lookup

#### Returns

- `Optional[License]` - license

### LicenseMatrix().searchLicenses

[[find in source code]](../../licensematrix/license_matrix.py#L101)

```python
def searchLicenses(search: str) -> list[License]:
```

Get a list of candidate licenses from a search string.

#### Arguments

- `search` *str* - search string

#### Returns

- `list[License]` - list of licenses
