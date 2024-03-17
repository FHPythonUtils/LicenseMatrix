# License Type

[Licensematrix Index](../README.md#licensematrix-index) / [Licensematrix](./index.md#licensematrix) / License Type

> Auto-generated documentation for [licensematrix.license_type](../../../licensematrix/license_type.py) module.

- [License Type](#license-type)
  - [License](#license)
    - [License().__repr__](#license()__repr__)
    - [License().__str__](#license()__str__)
    - [License().isCopyleft](#license()iscopyleft)
    - [License().isPermissive](#license()ispermissive)
    - [License().isPublicDomain](#license()ispublicdomain)
    - [License().isViral](#license()isviral)
    - [License().isWeakCopyleft](#license()isweakcopyleft)
    - [License().mergeBoth](#license()mergeboth)
    - [License().mergeIntoDest](#license()mergeintodest)
    - [License().naiveCompatDest](#license()naivecompatdest)
    - [License().naiveCompatDestLinking](#license()naivecompatdestlinking)
    - [License().naiveCompatSource](#license()naivecompatsource)
    - [License().naiveCompatSourceLinking](#license()naivecompatsourcelinking)
    - [License().termsCompatible](#license()termscompatible)
  - [equal](#equal)
  - [getMostStrictType](#getmoststricttype)
  - [mergeSPDX](#mergespdx)

## License

[Show source in license_type.py:12](../../../licensematrix/license_type.py#L12)

Represent a license.

Source: represents an existing license
Dest: represents a new combined license (possibly for a combined work)

#### Signature

```python
class License:
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
    ) -> None: ...
```

### License().__repr__

[Show source in license_type.py:73](../../../licensematrix/license_type.py#L73)

Get the string representation.

#### Signature

```python
def __repr__(self) -> str: ...
```

### License().__str__

[Show source in license_type.py:77](../../../licensematrix/license_type.py#L77)

To string.

#### Signature

```python
def __str__(self) -> str: ...
```

### License().isCopyleft

[Show source in license_type.py:89](../../../licensematrix/license_type.py#L89)

Is the License Copyleft?.

#### Signature

```python
def isCopyleft(self): ...
```

### License().isPermissive

[Show source in license_type.py:81](../../../licensematrix/license_type.py#L81)

Is the License Permissive?.

#### Signature

```python
def isPermissive(self): ...
```

### License().isPublicDomain

[Show source in license_type.py:97](../../../licensematrix/license_type.py#L97)

Is the License Public Domain?.

#### Signature

```python
def isPublicDomain(self): ...
```

### License().isViral

[Show source in license_type.py:93](../../../licensematrix/license_type.py#L93)

Is the License Viral?.

#### Signature

```python
def isViral(self): ...
```

### License().isWeakCopyleft

[Show source in license_type.py:85](../../../licensematrix/license_type.py#L85)

Is the License Weak Copyleft?.

#### Signature

```python
def isWeakCopyleft(self): ...
```

### License().mergeBoth

[Show source in license_type.py:101](../../../licensematrix/license_type.py#L101)

Combine two licenses into one super license.

Performs no checks on compatibility, this is up to the user.

#### Arguments

----
 - `rhs` *License* - the other license to merge

#### Returns

-------
 - [License](#license) - the new, combined license

#### Signature

```python
def mergeBoth(self, rhs: License): ...
```

### License().mergeIntoDest

[Show source in license_type.py:126](../../../licensematrix/license_type.py#L126)

Combine two licenses into one super license, but preserve the...

destination name. Performs no checks on compatibility, this is up to the user.

#### Arguments

----
 - `dest` *License* - the other license to merge

#### Returns

-------
 - [License](#license) - the new, combined license

#### Signature

```python
def mergeIntoDest(self, dest: License): ...
```

### License().naiveCompatDest

[Show source in license_type.py:245](../../../licensematrix/license_type.py#L245)

Check the source (self) is compatible with the destination license (rhs).

#### Arguments

----
 - `dest` *License* - the destination license

#### Returns

-------
 - `bool` - are the licenses compatible?

#### Signature

```python
def naiveCompatDest(self, dest: License) -> bool: ...
```

### License().naiveCompatDestLinking

[Show source in license_type.py:222](../../../licensematrix/license_type.py#L222)

Check the source (self) is compatible with the destination license (rhs).

For linking licenses

#### Arguments

----
 - `dest` *License* - the destination license

#### Returns

-------
 - `bool` - are the licenses compatible?

#### Signature

```python
def naiveCompatDestLinking(self, dest: License) -> bool: ...
```

### License().naiveCompatSource

[Show source in license_type.py:201](../../../licensematrix/license_type.py#L201)

Check the destination (rhs) is compatible with the source license (self).

#### Arguments

----
 - `dest` *License* - the destination license

#### Returns

-------
 - `bool` - are the licenses compatible?

#### Signature

```python
def naiveCompatSource(self, dest: License) -> bool: ...
```

### License().naiveCompatSourceLinking

[Show source in license_type.py:178](../../../licensematrix/license_type.py#L178)

Check the destination (rhs) is compatible with the source license (self).

For linking licenses

#### Arguments

----
 - `dest` *License* - the destination license

#### Returns

-------
 - `bool` - are the licenses compatible?

#### Signature

```python
def naiveCompatSourceLinking(self, dest: License) -> bool: ...
```

### License().termsCompatible

[Show source in license_type.py:151](../../../licensematrix/license_type.py#L151)

Check the destination terms (rhs) are compatible with the source license terms (self).

#### Arguments

----
 - `dest` *License* - the destination license

#### Returns

-------
 - `bool` - are the license terms compatible?

#### Signature

```python
def termsCompatible(self, dest: License) -> bool: ...
```



## equal

[Show source in license_type.py:310](../../../licensematrix/license_type.py#L310)

Are two licenses equal?.

#### Arguments

----
 - `licenseA` *License* - the first license
 - `licenseB` *License* - the second license

#### Returns

-------
 - `bool` - equal?

#### Signature

```python
def equal(licenseA: License, licenseB: License) -> bool: ...
```

#### See also

- [License](#license)



## getMostStrictType

[Show source in license_type.py:269](../../../licensematrix/license_type.py#L269)

Return the most 'strict' type of license from the available types.

#### Arguments

----
 - `typeA` *str* - type of the first license
 - `typeB` *str* - type of the second license

#### Returns

-------
 - `str` - the most 'strict' type

#### Signature

```python
def getMostStrictType(typeA: str, typeB: str) -> str: ...
```



## mergeSPDX

[Show source in license_type.py:290](../../../licensematrix/license_type.py#L290)

Combine the spdx ids.

#### Arguments

----
 - `spdxA` *str* - spdx of the first license
 - `spdxB` *str* - spdx of the second license

#### Returns

-------
 - `str` - combined spdx

#### Signature

```python
def mergeSPDX(spdxA: str, spdxB: str) -> str: ...
```