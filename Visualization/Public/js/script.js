const root = document.body;

let dump = "";

// Echo of backend

var socket = io("localhost:3001", {transports : ['websocket'] } )

socket.on("connect", function() {
    //socket.emit("getReady");
    // socket.send(["setMap", "Ivano-Frankivsk, Ukraine"].join('#'));

    socket.on("ready", () =>
    {
        // socket.send(["setMap", "Ivano-Frankivsk, Ivano-Frankivsk, Ukraine"].join('#'));
    });

});

let minX;
let minY;
let maxX;
let maxY;

socket.on("setMap", (string) => {
    dump = string;
    array = JSON.parse(dump);

    let nx = [];
    let ny = [];
    
    for(let i = 0; i < array['nodes'].length; i++){
        nx.push(array['nodes'][i][0][0]);
        ny.push(array['nodes'][i][0][1]);
    }  

    minX = getMinOfArray(nx);
    minY = getMinOfArray(ny);
    maxX = getMaxOfArray(nx);
    maxY = getMaxOfArray(ny);

    for(let i = 0; i < array['nodes'].length; i++){
        let x = +array['nodes'][i][0][0] - minX + 4; 
        let y = +array['nodes'][i][0][1] - minY + 4; 

        addNode(i, x, y);
    }

    roadWay(array['roads']);

    for(let i = 0; i < 1000; i++){
        let x = Math.random() * ((maxX - minX) * 10);
        let y = Math.random() * ((maxY - minY) * 10);
        if(
            !document.elementFromPoint(x, y) &&  
            !document.elementFromPoint(x + 20, y) && 
            !document.elementFromPoint(x - 20, y) &&
            !document.elementFromPoint(x, y + 20) &&
            !document.elementFromPoint(x, y - 20)
        ){
            addTree(x, y, Math.random() * 360);
        }
    }
});

let start = setInterval(() => {socket.on("setCars", (string) => {
    let array = JSON.parse(string);
    console.log(string);

    for(let i of array['cars']){
        let index = Object.keys(i);
        let x = i[Object.keys(i)][0][0] - minX + 4;
        let y = i[Object.keys(i)][0][1] - minY + 4;
        let incline = i[Object.keys(i)][1] * 180 / Math.PI;

        addCar(index, x, y, incline);
    }

    socket.send("setCars"); 
})}, 1000);

// document.addEventListener('keypress', moveWin);

// let zoom = 0;

// document.addEventListener('wheel', (event) => {
//     if(event.deltaY < 0){
//         zoom += 0.01;
//         root.style.transform = 'scale(' + (1 + zoom) + ')';
//     }else{
//         zoom -= 0.01;
//         root.style.transform = 'scale(' + (1 + zoom) + ')';
//     } 
// });

function moveWin(event){  
    if(event.key == 'w'){
        window.scroll({
            left:window.pageXOffset,
            top:window.pageYOffset - 500,
            behavior:'smooth'
        });
    }if(event.key == 's'){
        window.scroll({
            left:window.pageXOffset,
            top:window.pageYOffset + 500,
            behavior:'smooth'
        });
    }if(event.key == 'a'){
        window.scroll({
            top:window.pageYOffset,
            left:window.pageXOffset - 500,
            behavior:'smooth'
        });
    }if(event.key == 'd'){
        window.scroll({
            top:window.pageYOffset,
            left:window.pageXOffset + 500,
            behavior:'smooth'
        });
    }
}

function getMinOfArray(numArray) {
    return Math.min.apply(null, numArray);
}

function getMaxOfArray(numArray) {
    return Math.max.apply(null, numArray);
}

function addRoad(x, y, length, incline, one_road = false){
    const road = document.createElement('div');

    if (!one_road) {
        road.classList.add('road');

        road.style.left = (x - (length / 2)) + 'px';
        road.style.top = (y - 12) + 'px';
        road.style.width = length + 'px';
        road.style.transform = 'rotate(' + incline + 'deg)';
    }
    else {
        road.classList.add('road_one_line');
        
        road.style.left = (x - (length / 2)) + 'px';
        road.style.top = (y - 6) + 'px';
        road.style.width = length + 'px';
        road.style.transform = 'rotate(' + incline + 'deg)';
    }
    
    

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
    pavement.style.left = (x - 33) + 'px';
    pavement.style.top = (y - 33) + 'px';

    mainCircle.id = index;
    pavement.id = index;

    root.prepend(mainCircle);
    root.prepend(pavement);
}

function addCar(index, x, y, direct){
    x *= 10;
    y *= 10;
    const car = document.createElement('div');
    car.classList.add('car_red');
    car.id = index;

    car.style.left = x + 'px';
    car.style.top = y + 'px';
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
    c = c[0]
    for(let key in c){
        for(let ekey in c[key])
        {
            if (c[key][ekey].length == 0) continue;

            const node1 = document.getElementById(parseInt(key)); 
            const node2 = document.getElementById(parseInt(ekey));

            let x1 = parseInt(node1.style.left) + 18;
            let y1 = parseInt(node1.style.top) + 18;
            let x2 = parseInt(node2.style.left) + 18;
            let y2 = parseInt(node2.style.top) + 18;

            let x = (x1 + x2) / 2;
            let y = (y1 + y2) / 2;
            let length = ((Math.abs(x1 - x2) ** 2) + (Math.abs(y1 - y2) ** 2)) ** 0.5;
            let incline = Math.atan((y1 - y2) / (x1 - x2)) / Math.PI * 180;
            
            //console.log(key);
            console.log(c);
            if(key in c[ekey]) addRoad(x, y, length, incline);
            else addRoad(x, y, length, incline, true)
            
        }
    };
}

addTree(400, 100, 0);

function addTree(x, y, incline){
    const mainBranch = document.createElement('div');
    const branch1 = document.createElement('div');
    const branch2 = document.createElement('div');
    const mainBranchShadow = document.createElement('div');
    const branch1shadow = document.createElement('div');
    const branch2shadow = document.createElement('div');

    mainBranch.classList.add('tree');
    branch1.classList.add('tree_branch1');
    branch2.classList.add('tree_branch2');
    mainBranchShadow.classList.add('tree_shadow');
    branch1shadow.classList.add('tree_branch1_shadow');
    branch2shadow.classList.add('tree_branch2_shadow');

    let b1x = (x - 15) + (25 * Math.cos(incline * Math.PI / 180));
    let b1y = (y - 15) + (25 * Math.sin(incline * Math.PI / 180));
    let b2x = (x - 15) + (25 * Math.cos((incline + 150) * Math.PI / 180));
    let b2y = (y - 15) + (25 * Math.sin((incline + 150) * Math.PI / 180));

    mainBranch.style.left = (x - 25) + 'px';
    mainBranch.style.top = (y - 25) + 'px';
    branch1.style.left = b1x + 'px';
    branch1.style.top = b1y + 'px';
    branch2.style.left = b2x + 'px';
    branch2.style.top = b2y + 'px';

    mainBranchShadow.style.left = (x - 25) + (15 * Math.cos(60 * Math.PI / 180)) + 'px';
    mainBranchShadow.style.top = (y - 25) + (15 * Math.sin(60 * Math.PI / 180)) + 'px';
    branch1shadow.style.left = b1x + (10 * Math.cos(60 * Math.PI / 180)) + 'px';
    branch1shadow.style.top = b1y + (10 * Math.sin(60 * Math.PI / 180)) + 'px';
    branch2shadow.style.left = b2x + (10 * Math.cos(60 * Math.PI / 180)) + 'px';
    branch2shadow.style.top = b2y + (10 * Math.sin(60 * Math.PI / 180)) + 'px';

    root.prepend(mainBranch);
    root.prepend(branch1);
    root.prepend(branch2);
    root.prepend(mainBranchShadow);
    root.prepend(branch1shadow);
    root.prepend(branch2shadow);
}