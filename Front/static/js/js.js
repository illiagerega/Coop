// AJAX receivement
var map_ajax_state_sending = false;


function setCars() {
    if(!map_ajax_state_sending){
        map_ajax_state_sending = true
        $.ajax({
        url: "/map",
        type: "GET",
        data: {operation: "setCars"},
        cache: false,
        success: function(response) {
            $('#cars').html(response);
            map_ajax_state_sending = false; 
            console.log('I tf got that!');
            },

        });
        return false;
    }
};  

function setMap()
{
    if(!map_ajax_state_sending){
        map_ajax_state_sending = true
        $.ajax({
            url: "/map",
            type: "get",
            data: {operation: "setMap"},
            cache: false,
            success: function(response) {
                $('#map').html(response);
                console.log(response);
                map_ajax_state_sending = false;
            },
        });
    }
}


// Menu logic

let paused = false;
let started = false;
let speed = 2000; // 1/2 call per second
let eventCars = null;
let eventLights = null;


const onPause = () => {
    paused = !paused;

    if (started && !paused)
    {
        setIntervals();
        $("#pause").text("Pause");
    }
        
    if (paused)
    {
        clearIntervals();
        $("#pause").text("Resume");

    }
    
}

const onStart = () => {
    started = !started;

    if (started)
    {
        setMap();
        setIntervals();
        $("#pause").text("Pause");
        $("#pause").css("visibility", "visible");
        $("#speed_menu").css("visibility", "visible");
    }
    else
    {
        $("#pause").css("visibility", "hidden");
        $("#pause").text("Pause");
        $("#speed_menu").css("visibility", "visible");
        clearIntervals();
        paused = false;
    }
}

function setIntervals(){
    eventCars = setInterval(setCars, speed);
}

function clearIntervals(){
    clearInterval(eventCars);
}

const setSpeed = (value) => {
    $("#speed_display").text("Speed in ms: " + value.toString());
    speed = parseInt(value);
}


// get attributes && editor

const onEditor = () => {
    
}

// var notepad = document.getElementById("car_red");

// notepad.addEventListener("contextmenu", function(event){
//     event.preventDefault();
//     var ctxMenu = document.getElementById("ctxMenu");
//     ctxMenu.style.display = "block";
//     ctxMenu.style.left = (event.pageX - 10)+"px";
//     ctxMenu.style.top = (event.pageY - 10)+"px";
// },false);

// notepad.addEventListener("click",function(event){
//     var ctxMenu = document.getElementById("ctxMenu");
//     ctxMenu.style.display = "";
//     ctxMenu.style.left = "";
//     ctxMenu.style.top = "";
// },false);



// movement of main window

var up = false,
    right = false,
    down = false,
    left = false,
    wheel = false,
    inverted = false; // Invert WASD movement

var mousePosX = 0, mousePosY = 0;

var offset = 10; // default: 10 px per frame
var zoom_scale = -0.001;
var zoom_max = 4;
var zoom_min = 0.125;
var zoom_delta = 0;
var scale = 1;

document.addEventListener('keydown', press);
function press(e){
  if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
      if (inverted) up = true;
      else down = true;

  }
  if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
    if (inverted) right = true;
    else left = true;
  }
  if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
    if (inverted) down = true;
    else up = true;
  }
  if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */ || e.keyCode === 81 /* q */){
    if (inverted) left = true;
    else right = true;
  }
}

document.addEventListener('keyup',release)
function release(e){
  if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
    if (inverted) up = false;
      else down = false;
  }
  if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
    if (inverted) right = false;
    else left = false;
  }
  if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
    if (inverted) down = false;
    else up = false;
  }
  if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */ || e.keyCode === 81 /* q */){
    if (inverted) left = false;
    else right = false;
  }
}

document.addEventListener("mousewheel", zoom);

function zoom(e){
    // e.preventDefault();

    zoom_delta = e.deltaY;
    //wheel = true;

    var new_scale = scale + zoom_delta * zoom_scale;

    // restriction of scaling
    new_scale = Math.min(Math.max(zoom_min, new_scale), zoom_max);

    var element = $("#movable_scene");
    var position = element.position();
    const x = position.left, y = position.top;
    const parentRect = document.getElementById("movable_scene").parentNode.getBoundingClientRect();
    // element.css("transform-origin", (mousePosX * scale - x * scale).toString() + "px " + (mousePosY * scale - y * scale).toString() + "px")
    // element.css("left", 0);
    // element.css("top", 0);
    // (mousePosX - x) * (scale - 1)
    var xPercent = ((mousePosX - x)).toFixed(2);
    var yPercent = ((mousePosY - y)).toFixed(2);
    var left = Math.round(mousePosX - parentRect.left - (xPercent * (new_scale / scale)));
    var top = Math.round(mousePosY - parentRect.top - (yPercent * (new_scale / scale)));
  
    element.css("transform", "scale(" + new_scale + ")");
    element.css("left", left);
    element.css("top", top);

    scale = new_scale;
}

document.onmousemove = getCursorXY;
function getCursorXY(e){
    mousePosX = (window.Event) ? e.pageX : e.clientX + (document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft);
    mousePosY = (window.Event) ? e.pageY : e.clientY + (document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop);
  }

// main movement function

function mainMovement(){
    var element = $("#movable_scene");
    var position = element.position();
    var y = parseInt(position.top);
    var x = parseInt(position.left);
    var scale;

    if (up){
        y = y - offset;
    }
    if (right){
        x = x + offset;
    }
    if (down){
        y = y + offset;
    }
    if (left){
        x = x - offset;
    }

    element.css("left", x);
    element.css("top", y);
    // wheel = false;

    window.requestAnimationFrame(mainMovement)
}

window.requestAnimationFrame(mainMovement)


// setMap(); // when press button start

// setInterval(mode, 2000);

// var notepad = document.getElementById("car_red");
// notepad.addEventListener("contextmenu",function(event){
//     event.preventDefault();
//     var ctxMenu = document.getElementById("ctxMenu");
//     ctxMenu.style.display = "block";
//     ctxMenu.style.left = (event.pageX - 10)+"px";
//     ctxMenu.style.top = (event.pageY - 10)+"px";
// },false);
// notepad.addEventListener("click",function(event){
//     var ctxMenu = document.getElementById("ctxMenu");
//     ctxMenu.style.display = "";
//     ctxMenu.style.left = "";
//     ctxMenu.style.top = "";
// },false);

// var notepad = document.getElementById("car_red");
// notepad.addEventListener("contextmenu",function(event){
//     event.preventDefault();
//     var ctxMenu = document.getElementById("ctxMenu");
//     ctxMenu.style.display = "block";
//     ctxMenu.style.left = (event.pageX - 10)+"px";
//     ctxMenu.style.top = (event.pageY - 10)+"px";
// },false);

// notepad.addEventListener("click",function(event){
//     var ctxMenu = document.getElementById("ctxMenu");
//     ctxMenu.style.display = "";
//     ctxMenu.style.left = "";
//     ctxMenu.style.top = "";
// },false);
