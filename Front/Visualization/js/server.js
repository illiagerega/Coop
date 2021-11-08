
const express = require('express')
const http = require('http')
const fs = require('fs')
const path_ = require('path')
const net = require('net')
const events = require('events')
const socketIO = require('socket.io')
const formidable = require('formidable')


let app = express()
let router = express.Router()
let eventEmmiter = new events()

const menu_path = "/../index.html"
const model_path = "/../model.html"
const settings_html_path = "/../settings.html"
const path_data = "/../../data/map.json"
const path_cars = "/../../data/cars.json"
const public_directory = "/../Public"
const settings_path = "/../../settings.json"
const maps_path = "/../../data/"


const {setFileOrName, setNCars, getFileOrName, getNCars} = require(path_.join(__dirname + public_directory + "/js/settings.js")) 


const settings = JSON.parse(fs.readFileSync(path_.join(__dirname + settings_path)))

const port = settings["port_server"]
const port_io = port + 1
const port_main = settings["port_main"]

var current_client = null


app.use('/', router)
app.use(express.static(path_.join(__dirname + public_directory)))

app.set("view engine", "pug");
app.set("views", path_.join(__dirname, "views"));


router.get('/', (request, response) => {
    //var data = fs.readFileSync(__dirname + path, 'utf-8')
    response.sendFile(path_.join(__dirname + menu_path))
})


router.get('/model', (request, response) => {
    //var data = fs.readFileSync(__dirname + path, 'utf-8')
    console.log(getNCars());
    response.sendFile(path_.join(__dirname + model_path));
})

router.get('/settings', (request, response) => {
    //var data = fs.readFileSync(__dirname + path, 'utf-8')

    response.sendFile(path_.join(__dirname + settings_html_path))
})





app.post('/settings', (req, res) => {    
    if (req.method == 'POST') {
        var form = new formidable.IncomingForm();
        form.parse(req, function (err, fields, files) {
            
        if(fields.item == 'UploadFile'){
        var oldpath = files.inputFile.path;
          console.log(oldpath);
          var newpath = path_.join(__dirname + maps_path + "user_selected.osm");
          fs.copyFile(oldpath, newpath, function (err) {
            if (err) throw err;
          });
          setFileOrName(newpath);
        }
        else{
            setFileOrName( path_.join(__dirname + maps_path + fields.item));
        }
        setNCars(fields.cars_n);
         
        console.log("Link to file: ", getFileOrName());
        console.log("NCars: ", getNCars());


        var file = path_.join(__dirname + public_directory + "/js/settings.js")
        var newNCars = getNCars();
        var newFile = getFileOrName();
        updateFile(file, [{
            rule: 'NCars',
            replacer: newNCars
        }], function (err) {
            sails.log.info((err));
        });

        updateFile(file, [{
            rule: 'FileOrName',
            replacer: (("'" + newFile + "'").replace(/\\/g, "/"))
        }], function (err) {
            sails.log.info((err));
        });




     });


    }
})

var server = http.createServer(app)
var io = socketIO(port_io)

var socket = net.createServer(function(connection) {
    console.log("Python connected!")

    connection.on("end", function() {
        console.log("Python disconnected")
    })

    eventEmmiter.on("data", (data) => {
        connection.write(data)
    })

    connection.on("data", function(data){
        data = data.toString()

        if (data == "quit")
        {
            
            server.close()
            io.close()
            socket.close()
            console.log("Js disconected!")
        }
        if(data == "setMap")
        {
            eventEmmiter.emit(data)
        }
        if(data == "setCars")
        {
            eventEmmiter.emit(data)
        }
        if(data == "ready")
        {
            eventEmmiter.emit(data)
        }

    })

})

socket.listen(port_main, function(){
    console.log("server is listening!")
})

io.on("connection", function(client){

    //var data = fs.readFileSync(path_.join(__dirname + path_data)).toString()
    //console.log("connected with site!")
    // socket.emit("sendDump", data)

    eventEmmiter.on("setMap", () =>{
        var json = fs.readFileSync(path_.join(__dirname + path_data)).toString()
        console.log("setMap to site")
        client.emit("setMap", json)
    })

    eventEmmiter.on("setCars", () => {
        // console.log("setting cars...")
        var json = fs.readFileSync(path_.join(__dirname + path_cars)).toString()
        client.emit("setCars", json)
    })

    eventEmmiter.on("ready", () =>{
        console.log("\x1b[32m", "Everything is ready for usage!")
        console.log("\x1b[1m")
        client.emit("ready")
    })

    client.on("message", function(data) {

        console.log(data)
        eventEmmiter.emit("data", data)
    })

    client.on('disconnect', function() {
        delete client;
    });
})





// Це такий костиль шо просто.....
  function updateFile(filename, replacements) {
            return new Promise(function(resolve) {
                fs.readFile(filename, 'utf-8', function(err, data) {
                    var regex, replaceStr;
                    if (err) {
                        throw (err);
                    } else {
                        regex = new RegExp("(\\" + 'let' + "\\s* ]*" + replacements[0].rule + "\\s*=\\s*)([^\\n;}]+)([\\s*;}])");
                            replaceStr = "$1" + replacements[0].replacer + "$3";
                            data = data.replace(regex, replaceStr);

                    }
                    fs.writeFile(filename, data, 'utf-8', function(err) {

                        if (err) {
                            throw (err);
                        } else {
                            resolve();
                        }
                    });
                });
            })
        }


server.listen(process.env.port || port, () => console.log(`App listening on port ${port}!`))
