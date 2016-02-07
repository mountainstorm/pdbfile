PDBFile
=======

A basic clone of the Microsoft clr [PDB file parser](https://github.com/Microsoft/clrmd/blob/master/src/Microsoft.Diagnostics.Runtime/Utilities/PDB/) (debug symbols).

I've tried to make it slightly more pythonic e.g. changing the naming scheme of members something python style, changing 'out' params into multiple returns

References
----------
* http://pierrelib.pagesperso-orange.fr/exec_formats/MS_Symbol_Type_v1.0.pdf
* http://sawbuck.googlecode.com/svn-history/r922/trunk/syzygy/pdb/pdb_dbi_stream.cc


Testing
-------

Testing is performed using a set of scripts to validate that nothings broken (since a previous run).

### Prereqs ###

* pefile; https://github.com/erocarrera/pefile
* p7zip; keka7z (or similar)

### Process ###

1. run extract_signatures.py over a directory of pe files to extract the pdb signatures.  Save stdout to a file.
2. run download_symbols.py using the saved signature file and a symbols server
3. run test.py to validate those symbols against the saved info


License
-------
MIT; see LICENSE for more info



