const root = document.body;

// addNode(0, 200, 200);
// addCar(1, 100, 100, 30);

addNode(0, 150, 150);
addNode(1, 600, 400);
addNode(2, 800, 200);
addNode(3, 300, 500);
addNode(4, 800, 600);
roadWay([0,1], [1,2], [0,2], [0,3], [1,3], [1,4], [2,4], [3,4]);

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
    const car = document.createElement('div');
    car.classList.add('car_red');

    car.style.left = (x - 15) + 'px';
    car.style.top = (y - 8) + 'px';
    car.style.transform = 'rotate(' + direct + 'deg)';

    root.prepend(car);
}

function roadWay(...c){
    for(let i of c){
        const node1 = document.getElementById(i[0]); 
        const node2 = document.getElementById(i[1]);

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