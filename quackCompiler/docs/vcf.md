# **VCF**
=======
**CLASS: `vcfreader`**

	Description:Read the vcf file and construct it as an object.

* **Fields:**
  
  |Name|Description|
  |----|-----------|
  |filename|Store the file's name.|


* **Methods:**

  **`getByPos`**
  
  _Description:Get a record by a position (chromosome, position)._
  
  > * param `pos`: A position (chromosome, position).

  > * return `_Record`: It's in __PyVcf__.
  
  **`getAllelesByPos`**
  
  _Description:Get Alleles by a list of Position._
  
  > * param `pos`: A list of positions((chromosome1, position1),(chromosome2, position2),...).
  
  > * return `genotype`: A list of `genotype`s.
  
* **Superclass:** `object`

* **Others:**
  
  **File: vcfreader.py**
  

**CLASS: `genotype`**

	Description:Design this class for operating the genotype's alleles.

* **Fields:**
  
  Name|Description
  ----|-----------
  __alleles|the alleles in the genotype.


* **Methods:**

  **`testGenotype`**
  
  _Description: test whether the genotype's alleles is specified. It will call `compare` method below._
  
  > * param `gStr`: Specified the alleles, E.g. `'T,T'` .
  
  > * return `Boolean`: `True` or `False`. 
  
  **`compare`**
  
  _Description:_
  
  > * param alleles: The input alleles.
  
  > * return `RES`: See `RES` below.
  
* **Superclass:** `object`

* **Others:**
  
  **File: genotype.py**
  
***CLASS: `RES`***

	Description:Result of Compare. The result has three situations.
	
* **Fields:**

  Name|Value|Description
  ----|-----|-----------
  notEq|0|not matching
  exactEq|1|exact matching
  fuzzyEq|2|fuzzy matching

* **Superclass:** `Enum`

* **Others:**

  **File:genotype.py**


