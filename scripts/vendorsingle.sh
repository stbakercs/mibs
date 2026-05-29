#!/usr/bin/env bash
echo $1
v=$(basename $1)
d=$(dirname $1)

mib=$(find "$1" -type f ! -name '*.json-skip' -exec basename {} \; | tr '\n' ' ')
mib_json=$(find "$1" -type f ! -name '*.json-skip' | while read -r path; do
    if [[ -f "${path}.json-skip" ]]; then
        continue
    fi
    basename "$path"
done | tr '\n' ' ')

# Flatten vendor MIBs (including subdirs like nokia/stellar) into output/asn1 so
# local sources win over broken remote copies of the same module name.
find "$1" -type f ! -name '*.json-skip' -exec cp -f {} output/asn1/ \;

poetry run mibdump \
        --cache-directory=.pycache \
        --mib-source=file://$1/ --mib-source=file://$(pwd)/output/asn1 --mib-source=https://pysnmp.github.io:443/mibs/asn1/@mib@ \
        --destination-directory=./output/notexts $mib >log/$v-nt.log 2>log/$v-nt.err

poetry run mibdump \
        --cache-directory=.pycache \
        --mib-source=file://$1/ --mib-source=file://$(pwd)/output/asn1 --mib-source=https://pysnmp.github.io:443/mibs/asn1/@mib@ \
        --destination-directory=./output/texts \
        --generate-mib-texts --keep-texts-layout $mib >log/$v-t.log 2>log/$v-t.err

poetry run mibdump \
	--ignore-errors \
 	--cache-directory=.pycache \
        --mib-source=file://$1/ --mib-source=file://$(pwd)/output/asn1 --mib-source=https://pysnmp.github.io:443/mibs/asn1/@mib@ \
	--destination-directory=./output/json --destination-format=json \
	 $mib_json >log/$v-j.log 2>log/$v-j.err


find "$1" -type f ! -name '*.json-skip' -exec cp -f {} output/asn1/ \;