

let type = "WebGL"
if (!PIXI.utils.isWebGLSupported()) {
    type = "canvas"
}

PIXI.utils.sayHello(type)


// init stage

let app = new PIXI.Application({
    antialias: true,
    transparent: false,
    backgroundColor: 0x28B463
})

app.renderer.resize(window.innerWidth, window.innerHeight);

app.renderer.view.style.position = 'absolute'

let cars_container = new PIXI.Container({
    transparent: false,
    antialias : true,
})

let nodes_container = new PIXI.Container({
    transparent: false,
    antialias : true,

})

let roads_container = new PIXI.Container({
    transparent: false,
    antialias : true,

})

document.body.appendChild(app.view)

app.stage.addChild(roads_container)
app.stage.addChild(nodes_container)

const texture_car = new PIXI.Texture.from("../img/car_red.png")
const texture_one_road = new PIXI.Texture.from("../img/one_road.png")
const node_radius = 20
const width_lane = 10

//




var map = {"nodes" : [[[20, 8], "spawn"], [[10, 8], "spawn"]], "roads" : {'0' : {'1' : 1}, '1' : {'0' : 1}} }

setMap(map)

function setMap(array)
{
    for(var i = 0; i < array["nodes"].length; i++)
    {
        console.log(array["nodes"][i][0][0])
        addNode(array["nodes"][i][0][0], array["nodes"][i][0][1])
    }

    for(var key in array["roads"])
    {
        
    }
}

function addRoad(x1, x2, y1, y2, n_lanes, angle, is_one = false)
{
    angle = angle
    degree_angle = angle * 180 / Math.PI
    if(is_one)
    {
        road_piece = new PIXI.Sprite(texture_one_road)
        road_piece.anchor.x = 0.5
        road_piece.anchor.y = 0.5
        road_piece.position.x = x1
        road_piece.position.y = y1
        road_piece.rotation = angle
        //road_piece.position.y = angle
        
        road_piece.height = ((Math.abs(x1 - x2) ** 2) + (Math.abs(y1 - y2) ** 2)) ** 0.5;
        road_piece.width = width_lane

        roads_container.addChild(road_piece)
    }
}


function addNode(x, y){
    x = x * 10
    y = y * 10
    // console.log(x)
    // console.log(y)

    node = new PIXI.Graphics()
    node.beginFill(0x4a4a4a)
    node.lineStyle(2, 0x6b6b6b)
    node.drawCircle(x, y, node_radius)
    node.endFill()

    nodes_container.addChild(node)

}