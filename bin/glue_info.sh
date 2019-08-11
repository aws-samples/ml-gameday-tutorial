#! /bin/bash

__dirname="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$__dirname/../templates/main/bin/output.js | jq '{"GameDatabase":.GlueDatabase,"GameTable":.GlueTable}'

DB=$($__dirname/../templates/main/bin/output.js | jq .GlueDatabase --raw-output)
TABLE=$($__dirname/../templates/main/bin/output.js | jq .GlueTable --raw-output)
echo "----example sql Query----

SELECT * FROM $DB.$TABLE limit 10;
"
