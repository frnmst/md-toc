#!/bin/bash
read -r -d '' payload << 'EOF'
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

local_hashes="17b4bd5dc287d643f7da0b9654aee10b48c00e05f39be0edfabe7b69d7aa02e57914cdf1bd2d452e1b9ef95804b3a212d2463eb277c06e05ff49a11b3fd6e4d47cf184bee206b738ea0d9a639bfbb146e6e3988b87786f8c792035e49c67f483" && remote_hashes=$(curl https://pypi.org/pypi/md-toc/json | jq '.urls[] | .digests | to_entries[] | select(.key != "blake2b_256") | .value' | tr -d '"' | sort | tr -d "\n") && [ ${local_hashes} = ${remote_hashes} ] && export PIP_ONLY_BINARY=:all: && pipx install md-toc==9.1.0
-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEECQ7wtO7QEmICo89RJBFu2FZmeAoFAmq+gb0ACgkQJBFu2FZm
eApIARAAnjStMiXHIlRU0lGYIfL47LT3H/RbRnfNAOt9ojRjYuLadh/h6kaRy3eR
uT4p4/2iHxIIp1GZ1Lzmlo8C4k3F7cFL5vEw/YgP4FwrTXU8A05NbO9Pm0g7+5S6
IiVkkPbqQmFECFOpXkvImvEwapHTXPZiw8iUGa/3ziOQX0C406GgyT/SYrOXept7
ID46mJaZtouMxUTD/h9RXAJAF7Ym/J/vQO7HUyi3942JeZj6x4ALjPuarapS+9gd
ZyCugZ5BoqgQyKFyG2/E+00tfaledvU6vkhZsgMjb5fmYdlfqHR0SGUwlR3547Pu
Za00vAodV8AuhLXtmx04cHbx1be7EkpThuAaMw+QJVtZlRsvRCitU3l4lCilI5NE
PbCtkzq3k79ciY2aohtaj08wkl3ijgA+7IYQRfvpEmZqp7o/6FoxqZIt+YuylYfY
gNgoTIllAGTvlVRmHGUrQsrDDUby431k4WQoGna1i+vzASxaxshH6kMSAoSgv3F1
pN67c4ZtbfgJ44vXOF06nz3mWTLbSyGQF5TymA21Fa3l3+cDcG5Avo9a1TWtXBIR
5FsdXejpN8v2wdbHXoISnuzSy3YGUS/YRDy5A+EqzTTKRCt9sRY79d7iMVPi7TrY
jfwPJie8kII3RL7tWDLtQ+niqq9AT4WL1T4ySvxjPDc5n/JN8RU=
=cSf5
-----END PGP SIGNATURE-----
EOF
which curl pipx sort tr jq echo && echo "${payload}" | gpg --verify - && { echo "${payload}" | gpg --decrypt - | sh; } || exit 1
