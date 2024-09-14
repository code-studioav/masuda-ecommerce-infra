const toml = require('toml');
const concat = require('concat-stream');
const fs = require('fs');

const argv = require('minimist')(process.argv.slice(2));

const read_by_dot_notation = (input_dot_key, data) => {
    let keys = input_dot_key.split('.');

    if (keys.length <= 1) return data[keys[0]];

    const actual_key = keys.shift()

    return read_by_dot_notation(keys.join('.'), data[actual_key])
}

const file_name = argv['inputFile']
const key = argv['key']

const raw_text = fs.readFileSync(file_name, { encoding: 'utf8', flag: 'r' })
let data = toml.parse(raw_text);
        
console.log(`${key}=${read_by_dot_notation(key, data)}`);