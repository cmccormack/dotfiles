const fs = require('fs')
const path = require('path')
const chalk = require("chalk")

console.log(__dirname)
const OUTFILE = path.resolve(__dirname, "./combined.json")
const combine = require('../combine_json_from_files')

const write = process.stdout.write.bind(process.stdout)

fs.unlink(OUTFILE, async (err) => {
  if (err && err.code !== "ENOENT") {
    console.log(err)
    write(chalk.red(" ✘ "))
    write(`Error deleting file ${OUTFILE} "${err.message}", terminating...`)
    process.exit(1)
  }

  const success = await combine(['./a.json', './b.json'].map(file => path.resolve(__dirname, file)), OUTFILE)

  if (success) {
    write(chalk.green(" ✔ "))
    write(`Successfully created "${OUTFILE}"!`)
    return
  }
})