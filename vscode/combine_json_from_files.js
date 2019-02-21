const fs = require("fs")
const chalk = require("chalk")

const write = process.stdout.write.bind(process.stdout)
const OUTFILE_NAME = "combined.json"

const isModule = require.main !== module



const readFilePromise = (filename, opts="utf8") => new Promise((resolve, reject) => {
  fs.readFile(filename, opts, (err, data) => 
    err ? reject(filename) : resolve(data)
  )
})

const combine_json_from_files = async (filenames, output_filename) => {

  // Read data from files
  const files = await Promise.all(
    filenames.map(filename => readFilePromise(filename))
  )
  .catch(err => {
    write(chalk.red(" ✘ "))
    write(`Error reading file "${err}", terminating...`)
    process.exit(2)
  })

  // Combine files into single JSON file
  const combined_json = files.reduce((acc, file, i) => {
    try {
      return Object.assign(acc, JSON.parse(file))
    } catch (e) {
      write(chalk.red(" ✘ "))
      write(`Error parsing JSON in file ${filenames[i]} "${e.message}", terminating...`)
      process.exit(3)
    }
  }, {})

  // Write file to disk
  await fs.writeFile(output_filename, JSON.stringify(combined_json, null, 4), err => {
    if (err) {
      write(chalk.red(" ✘ "))
      write(`Error writing to file ${output_filename} "${e.message}", terminating...`)
      return process.exit(4)
    }
  })

  return true

}


if (!isModule) {
  
  const filenames = process.argv.slice(2, 4)
  
  if (filenames.length < 2) {
    write(chalk.red(" ✘ "))
    write("Must include at least two filename arguments, terminating...")
    process.exit(1)
  }
  
  combine_json_from_files(filenames, OUTFILE_NAME)
  
}


module.exports = combine_json_from_files