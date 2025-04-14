#!/bin/sh

folder=$1
placeholders=`./config.py -l -q $folder 2> /dev/null`
echo "Placeholders found in ${folder} are: ${placeholders}"
echo
for placeholder in ${placeholders};
do
    value=$(eval echo \$$placeholder)
    if [[ -z "${placeholder}" ]]; then
        echo "Environment variable not set for placeholder [$placeholder]"
    else
        echo "Configuring ${placeholder}=${value}"
        ./config.py $folder $placeholder $value
    fi
done

/usr/local/bin/httpd-foreground

