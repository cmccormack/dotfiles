const fs = require('fs')

const file = process.argv[2]
const [name, ext] = file.split('.')

if (!file) {
  console.log("Must include filename argument, terminating...")
  process.exit(1)
}

fs.readFile(file, (err, file) => {
  if (err) {
    console.error(`Error reading file '${filename}': ${err.message}, terminating...`);
    process.exit(1)
  }

  try {
    const json = JSON.parse(file.toString('utf8'))
    const keys = Object.keys(json).sort()
    const cleanObj = keys.reduce(
      (a,key) => Object.assign(a, {[key]: json[key]}),
      {}
    )
    fs.writeFile(
      `${name}-clean.${ext}`,
      JSON.stringify(cleanObj, null, 4),
      (err) => {
        if (err) {
          console.error(`Error writing file: ${err.message}, terminating...`)
          process.exit(1)
        }
      }
    )
  } catch(err) {
    console.error(`Invalid JSON file: ${err.message}, terminating...`);
    process.exit(1)
  }
})