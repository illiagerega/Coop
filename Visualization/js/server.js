const express = require('express')
const http = require('http')
const fs = require('fs')
const path_ = require('path')
const socketIO = require('socket.io')
let app = express()
let router = express.Router()
const port = 3000

const path = "/../index.html"
const path_data = "/../../data/map.json"
const public_directory = "/../Public"


router.get('/', (request, response) => {
    //var data = fs.readFileSync(__dirname + path, 'utf-8')
    response.sendFile(path_.join(__dirname + path))
})

app.use('/', router)
app.use(express.static(path_.join(__dirname + public_directory)))

var server = http.createServer(app)
var io = socketIO(port + 1)

io.on("connection", function(socket){

    var data = fs.readFileSync(path_.join(__dirname + path_data)).toString()
    console.log("connected!")
    socket.emit("sendDump", data)
})

server.listen(process.env.port || port, () => console.log(`Example app listening on port ${port}!`))