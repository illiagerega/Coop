const root = document.getElementById("rootId");

let dump = "";

let is_paused = false;
let is_started = false;
let generated = false;
let cars_created = false;

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

// const adasd = [[-393.4310344827586, 46.80344827586207], -0.33261969157391236, 3]
// const dd = [[-382.0708333333333, 101.3763888888889], 1.0019484683735376, 2]

// function testCar()
// {
//     var x = adasd[0][0] - minX + 2;
//     var y = adasd[0][1] - minY + 2;
//     var incline = adasd[1] * 180 / Math.PI;
//     console.log(minX);
//     addCar(0, x, y, incline);


//      x = dd[0][0] - minX + 2;
//      y = dd[0][1] - minY + 2;
//      incline = dd[1] * 180 / Math.PI;
//     console.log(minX);
//     addCar(0, x, y, incline);
// }

socket.on("setMap", (string) => {
    if(generated) return;
    generated = true;

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

    // testCar();

    for(let i = 0; i < array['nodes'].length; i++){
        let x = +array['nodes'][i][0][0] - minX + 4; 
        let y = +array['nodes'][i][0][1] - minY + 4; 

        addNode(i, x, y);
    }

    roadWay(array['roads']);

    // for(let i = 0; i < 200; i++){
    //     let x = Math.random() * ((maxX - minX) * 10);
    //     let y = Math.random() * ((maxY - minY) * 10);
    //     if(
    //         !document.elementFromPoint(x, y) &&  
    //         !document.elementFromPoint(x + 20, y) && 
    //         !document.elementFromPoint(x - 20, y) &&
    //         !document.elementFromPoint(x, y + 20) &&
    //         !document.elementFromPoint(x, y - 20)
    //     ){
    //         addTree(x, y, Math.random() * 360);
    //     }
    // }
});

socket.on("setCars", (string) => {
    if (!is_paused){

        let array = JSON.parse(string);
        // console.log(string);
    
        for(let i of array['cars']){
            let index = Object.keys(i);

            if(i[Object.keys(i)][0][0] == -100 && i[Object.keys(i)][0][1] == -150  && i[Object.keys(i)][1] == -200 ){ // just some special values to tell that this car has reached destination and it needs to be removed
                document.getElementById(index).remove();
                continue;
            }
            let x = i[Object.keys(i)][0][0] - minX + 1.8;
            let y = i[Object.keys(i)][0][1] - minY + 2;
            let incline = i[Object.keys(i)][1] * 180 / Math.PI;
    
            if (!cars_created) addCar(index, x, y, incline);
            else moveCar(index, x, y, incline)
        }
        
        cars_created = True;
        socket.send("setCars"); 
    }
})

function clearScene()
{
    // past something here

    
    
}



document.addEventListener('keypress', moveWin);

 let zoom = 0;

 document.addEventListener('wheel', (event) => {
     if(event.deltaY < 0){
         zoom += 0.02;
         root.style.transform = 'scale(' + (1 + zoom) + ')';
     }else{
         zoom -= 0.02;
         root.style.transform = 'scale(' + (1 + zoom) + ')';
     } 
 });

function moveWin(event){  
    if(event.key == 'w' || event.key == 'ц' || event.key == 'Ц'|| event.key == 'W'){
        window.scroll({
            left:window.pageXOffset,
            top:window.pageYOffset - 500,
            behavior:'smooth'
        });
        document.querySelector('.set_container').style.display = 'none';
    }if(event.key == 's' || event.key == 'ы' || event.key == 'Ы' || event.key == 'S' || event.key == 'і'|| event.key == 'І' ){
        window.scroll({
            left:window.pageXOffset,
            top:window.pageYOffset + 500,
            behavior:'smooth'
        });
        document.querySelector('.set_container').style.display = 'none';
    }if(event.key == 'a' || event.key == 'ф' || event.key == 'Ф' || event.key == 'A' ){
        window.scroll({
            top:window.pageYOffset,
            left:window.pageXOffset - 500,
            behavior:'smooth'
        });
        document.querySelector('.set_container').style.display = 'none';
    }if(event.key == 'd' || event.key == 'в' || event.key == 'В' || event.key == 'D'){
        window.scroll({
            top:window.pageYOffset,
            left:window.pageXOffset + 500,
            behavior:'smooth'
        });
        document.querySelector('.set_container').style.display = 'none';
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
    document.getElementById(index).remove();
    const car = document.createElement('div');
    car.classList.add('car_red');
    car.id = index;

    car.style.left = x + 'px';
    car.style.top = y + 'px';
    car.style.transform = 'rotate(' + direct + 'deg)';

    root.prepend(car);
}

function moveCar(index, x2, y2, direction){
    // let car = document.getElementById(index);
    // let x1 = +car.style.left.slice(0, car.style.left.length - 2);
    // let y1 = +car.style.top.slice(0, car.style.top.length - 2);
    // let deltaX = (Math.abs(x1 - x2) ** 2 + Math.abs(y1 - y2) ** 2) ** 0.5;

    // car.style.left = x2*10 + 'px';
    // car.style.top = y2*10 + 'px';

    // car.style.transform = 'rotate(' + direction + 'deg)';

    let car = document.getElementById(index);
    let x1 = +car.style.left.slice(0, car.style.left.length - 2);
    let y1 = +car.style.top.slice(0, car.style.top.length - 2);
    let deltaX = (Math.abs(x1 - x2) ** 2 + Math.abs(y1 - y2) ** 2) ** 0.5;

    car.setAttribute('v', Math.round(deltaX / 100));
    car.setAttribute('direction', direction);

    console.log(direction);
    car.style.left = x2*10 + 'px';
    car.style.top = y2*10 + 'px';
    car.style.transform = 'rotate(' + direction + 'deg)';
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
            // console.log(c);
            if(key in c[ekey]) addRoad(x, y, length, incline);
            else addRoad(x, y, length, incline, true)
            
        }
    };
}

// addTree(400, 100, 0);

let cont = document.createElement('div');
let h3 = document.createElement('div');
let spanId = document.createElement('span');
let spanDirection = document.createElement('span');
let spanX = document.createElement('span');
let spanY = document.createElement('span');

document.addEventListener('mousedown', settings);

function settings(event){
    let x = event.clientX;
    let y = event.clientY;
    let car;

    if(document.elementFromPoint(x, y).classList.contains('car_red') && is_paused){
        car = document.elementFromPoint(x, y);

        cont.classList.add('set_container');
        h3.classList.add('set_h3');

        cont.style.left = x + 'px';
        cont.style.top = y + 'px';
        cont.style.display = 'inline-flex';

        h3.textContent = 'Car Red';
        spanId.textContent = 'Id: ' + +car.id;
        spanDirection.textContent = 'Direction: ' + Math.round(+car.getAttribute('direction'));
        spanX.textContent = 'X: ' + +x;
        spanY.textContent = 'Y: ' + +y;

        cont.prepend(spanY);
        cont.prepend(spanX);
        cont.prepend(spanDirection);
        cont.prepend(spanId);
        cont.prepend(h3);
        document.getElementById("carMenu").prepend(cont);

    }
    else{
        cont.style.display = "none";
    }
} 


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