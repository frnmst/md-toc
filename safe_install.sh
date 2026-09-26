#!/bin/bash
read -r -d '' payload << 'EOF'
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

local_hashes="3bc9dde15853dacd565d774a917fab858e23bb0fb4157e575d738fa38b1855d80318e59d426254b5810f5fa212c1cfcdb43984f2efc25344befae0e4b3e12da7ec27f92e2ce638e2068ef4789aca2eda724762f386bda6d05f5b03cd05b2b297" && remote_hashes=$(curl https://pypi.org/pypi/md-toc/json | jq '.urls[] | .digests | to_entries[] | select(.key != "blake2b_256") | .value' | tr -d '"' | sort | tr -d "\n") && [ ${local_hashes} = ${remote_hashes} ] && export PIP_ONLY_BINARY=:all: && pipx install md-toc==9.0.1
-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEECQ7wtO7QEmICo89RJBFu2FZmeAoFAmq37+gACgkQJBFu2FZm
eAoUzg//U6Wqahx+uMZH6TmA6IxuF/6BT3Xed01S98cKSYL2x17qpzUvcy5trtvT
5Rv6/nxOePTVWLEpSQV568/VfV22MtpVljbjqoEcJost78OSCytQKcWMb/CyRltG
/5XVuL5iKFUvl4DqyeewVjGpX1hSy3Gjk65NPCoLyJ/CXfxobgSRjSdjnI7c2Cq9
hLKxn0crjfQhvL6jrq798sJUa221MVl2QKI4R9QDiR66xKRDPXYlfg2H4RQUPswW
ZWVumuJ/V/63IRaRss5Hq9nudiQLuYajlIMTNWXxEAlViUzEiMBS1uGmnSfF4MkM
nQFTdIF0zU8QH9jhBRMxzH8dal57eCdqKVxNQ1aNR4pYo22o3DBQiycysbNuLGd6
IfS2cqez9tN6My5M0UlU0QlqQgqNz1ahJY1eY+UsRnFwo41aHqZHJA+c2q+QcmcH
AfTbjJEYDPaDRiEoZ9LjapWdYAGF1OnlL/JmWKDaORgWxudgtjs3nHyorDA/jZVK
Bwhw6/TRECgVkboF8ZLYKWVHB2som9MOVLLToQsWxQINR2WRFAKxqSLx0HiMqyJM
kH+QPF8+AH8OFKNbJPZGxYqWvEFN2spqhMKzl1UqJzeGTSBi+ENwbIVEYF5pmwvj
mqjpDQzKn2CunbTuIsWn2w8JdSsGSqPgyc0Vbkj4Y7QdcWkZ1Jg=
=0F0E
-----END PGP SIGNATURE-----
EOF
which curl pipx sort tr jq echo && echo "${payload}" | gpg --verify - && { echo "${payload}" | gpg --decrypt - | sh; } || exit 1
