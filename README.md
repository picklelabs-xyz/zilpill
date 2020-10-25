# zil
Requirements:
`python`, `pip-tools`


### Instructions to install:
* ``mkvirtualenv  -i "pip-tools==5.*" zil``  creates the venv named `zil`

* ``pip-compile --generate-hashes`` Generates the-hashes from `requirement.in`
  to `requirement.txt`, freezes the requirements.
* ``pip-sync requirements.txt`` Install all the dependencies from `requirement
.txt` 


#### Extra Remarks:
1. Could not successfully install Pyzil in WIN.
2. In Ubuntu (with Python 3.6.8), Pyzil installation failed initially due to inconsistent versions of
jsonrpcclient and Click (specified in the requirements.txt of Pyzil). Resolved it by
using Click==6.7 and jsonrpcclient==3.3.6.
3. It does work fine in macOS
