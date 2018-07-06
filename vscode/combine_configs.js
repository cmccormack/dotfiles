const fs = require('fs')

const mac = fs.readFileSync("mac/settings.json").toString('utf8')
const windows = fs.readFileSync("windows/settings.json").toString("utf8")

const combined = Object.assign(JSON.parse(mac), JSON.parse(windows))

fs.writeFileSync("combined.json", JSON.stringify(combined, null, 4))