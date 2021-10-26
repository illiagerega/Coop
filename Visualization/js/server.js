const express = require('express')
const http = require('http')
const fs = require('fs')
const path_ = require('path')
const net = require('net')
const socketIO = require('socket.io')
let app = express()
let router = express.Router()

const path = "/../index.html"
const path_data = "/../../data/map.json"
const public_directory = "/../Public"
const settings_path = "/../../settings.json"

const settings = JSON.parse(fs.readFileSync(path_.join(__dirname + settings_path)))

const port = settings["port_server"]
const port_io = port + 1
const port_main = settings["port_main"]

router.get('/', (request, response) => {
    //var data = fs.readFileSync(__dirname + path, 'utf-8')
    response.sendFile(path_.join(__dirname + path))
})

app.use('/', router)
app.use(express.static(path_.join(__dirname + public_directory)))

var server = http.createServer(app)
var io = socketIO(port_io)

var socket = net.createServer(function(connection) {
    console.log("client connected!")

    connection.on("end", function() {
        console.log("disconnected")
    })


})

io.on("connection", function(socket){

    var data = fs.readFileSync(path_.join(__dirname + path_data)).toString()
    console.log("connected!")
    socket.emit("sendDump", data)
})



server.listen(process.env.port || port, () => console.log(`Example app listening on port ${port}!`))
socket.listen(port_main, function(){
    console.log("server is listening!")
})