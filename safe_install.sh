#!/bin/bash
read -r -d '' payload << 'EOF'
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

local_hashes="8e23bb0fb4157e575d738fa38b1855d80318e59d426254b5810f5fa212c1cfcdb43984f2efc25344befae0e4b3e12da7d66b66228d4dcd58601b06e3a88a404623e9a0e90c1bece1e707cdf0e95aa28bf449d1e936a745bcda13a877eed307a9" && remote_hashes=$(curl https://pypi.org/pypi/md-toc/json | jq '.urls[] | .digests | to_entries[] | select(.key != "blake2b_256") | .value' | tr -d '"' | sort | tr -d "\n") && [ ${local_hashes} = ${remote_hashes} ] && export PIP_ONLY_BINARY=:all: && pipx install md-toc==9.0.1
-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEECQ7wtO7QEmICo89RJBFu2FZmeAoFAmq4OO8ACgkQJBFu2FZm
eAp9KBAAq8M71MAwBS3mRgGnQvKqvYVAUa71MCGpHE9p9Lkgky50YiX7l+JkyM2F
xz3Ypv094tGG6re9+t2GOb7gLCm7QzS2mxI1DLXETywwIZ+7ETgkwXAmzd5bUK8o
TXeFQYC2UXcxfC2FoNyTzRQQuRR8R7ZG1g0Li2VrYm+8Hk9LlrjdvLHC/bxbPivB
FNneK5km8DFyCM7G2XkKEuzpc0UM+7e3PONxACiyMYc8PsShH18crzGKSxNl5vuM
foPz/UNK9yfOZVnQHGiqiAJCTZdGakQZVekw9f1x9GRTyGTqNaNZ/gTVdcxCBQSJ
J0DA85FYBOhY4hdiwLiXxo6EfzK5T6AC5H1kfOWkXDaanTEFp1PSDGQH6rTY8rH7
6sABkITysPagTsMS+WVVWpFRu7MH7mlW3gkJvUSDuxkZl86Bfm1FCI5WwZqN6721
32U5MwgwUM62J70Q5YsgkiCHrAjcRXWAXOtt8SgXpiiJ+P848ZdhuJTBOxQShWR5
ez8tn17aeEzKv03YaMoIx24P48EoGYq9xMsyx0Fhw15yZi9pPsH5jPTR3P6O915c
oRvS0ajQzC32rLAFHdd7OEcvTvProhDR+o8RlG0XnK4O4E6kOi40IooWhiNs1tHl
c4iMwJVkMhnJmmBt4Jvuok1ji7Yl7uNDGCcSWxgfXy5NDO1Gjjg=
=BmDJ
-----END PGP SIGNATURE-----
EOF
which curl pipx sort tr jq echo && echo "${payload}" | gpg --verify - && { echo "${payload}" | gpg --decrypt - | sh; } || exit 1
