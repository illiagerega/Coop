const root = document.body;

let dump = "";

// {"nodes": [[[0, 0], "spawn"], [[2, 0], "spawn"], [[1, 4], "spawn"]};

var socket = io("localhost:3001", {transports : ['websocket'] } )
socket.on("connect", function() {
})
socket.on("sendDump", (string) => {
    dump = string;
    array = JSON.parse(dump);
    let nx = [];
    let ny = [];
    
    for(let i = 0; i < array['nodes'].length; i++){
        let x = +array['nodes'][i][0][0] + 2000; 
        let y = +array['nodes'][i][0][1] + 2000; 
        addNode(i, x, y);
    }  
    roadWay(array['roads']);
});

function getMaxOfArray(numArray) {
    return Math.max.apply(null, numArray);
}
function getMinOfArray(numArray) {
    return Math.min.apply(null, numArray);
}

function addRoad(x, y, length, incline){
    const road = document.createElement('div');
    road.classList.add('road');

    road.style.left = (x - (length / 2)) + 'px';
    road.style.top = (y - 25) + 'px';
    road.style.width = length + 'px';
    road.style.transform = 'rotate(' + incline + 'deg)';

    root.prepend(road);
}

function addNode(index, x, y){
    x *= 10;
    y *= 10;
    const mainCircle = document.createElement('div');
    const pavement = document.createElement('div');
    mainCircle.classList.add('main_circle');
    pavement.classList.add('main_circle_border');

    mainCircle.style.left = (x - 30) + 'px';
    mainCircle.style.top = (y - 30) + 'px';
    pavement.style.left = (x - 35) + 'px';
    pavement.style.top = (y - 35) + 'px';

    mainCircle.id = index;
    pavement.id = index;

    root.prepend(mainCircle);
    root.prepend(pavement);
}

function addCar(index, x, y, direct){
    x *= 50;
    y *= 50;
    const car = document.createElement('div');
    car.classList.add('car_red');
    car.id = index;

    car.style.left = (x - 15) + 'px';
    car.style.top = (y - 8) + 'px';
    car.style.transform = 'rotate(' + direct + 'deg)';

    root.prepend(car);
}

function moveCar(index, v){
    let car = document.getElementById(index);
    let x = +car.style.left.slice(0, car.style.left.length - 2);
    let y = +car.style.top.slice(0, car.style.top.length - 2);
    let road = document.elementFromPoint(x - 1, y + 8);
    let incline = +road.style.transform.slice(7, road.style.transform.length - 4);

    car.style.transform = 'rotate(' + incline + 'deg)';
}

function roadWay(...c){
    for(let i of c[0]){
        const node1 = document.getElementById(i[0][0]); 
        const node2 = document.getElementById(i[0][1]);

        let x1 = parseInt(node1.style.left) + 35;
        let y1 = parseInt(node1.style.top) + 35;
        let x2 = parseInt(node2.style.left) + 35;
        let y2 = parseInt(node2.style.top) + 35;

        let x = (x1 + x2) / 2;
        let y = (y1 + y2) / 2;
        let length = ((Math.abs(x1 - x2) ** 2) + (Math.abs(y1 - y2) ** 2)) ** 0.5;
        let incline = Math.atan((y1 - y2) / (x1 - x2)) / Math.PI * 180;

        addRoad(x, y, length, incline);
    };
}