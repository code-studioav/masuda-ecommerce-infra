input_file=$(echo "$1")
key_search=$(echo "$2")

output_script=$(npm run read_key -- --inputFile=$input_file --key=$key_search | tail -n 1)
replace=$(echo "$key_search=")
replace_with=$(echo "")

echo "${output_script/${replace}/${replace_with}}"