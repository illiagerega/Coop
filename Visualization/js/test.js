
let fs = require('fs')

let dump = fs.readFileSync('../data/map.json', 'utf8')
let array = JSON.parse(dump)


console.log(array)




