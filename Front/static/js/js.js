var map_ajax_state_sending = false;


// AJAX receivement



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
        eventCars = setInterval(setCars, speed);
        $("#pause").text("Pause");
    }
        
    if (paused)
    {
        clearInterval(eventCars);
        $("#pause").text("Resume");

    }
    
}

const onStart = () => {
    started = !started;

    if (started)
    {
        setMap();
        eventCars = setInterval(setCars, speed);
        $("#pause").text("Pause");
        $("#pause").css("visibility", "visible");
    }
    else
    {
        
    }
}

const onEditor = () => {
    
}

const setSpeed = (value) => {
    $("#speed_display").text("Speed in ms: " + value.toString())
}

// movement of main window

var up = false,
    right = false,
    down = false,
    left = false,
    wheel = false,
    inverted = false; // Invert WASD movement

var mousePosX = 0, mousePosY = 0;

var offset = 10; // default: 10 px per frame
var zoom_scale = -0.002;
var zoom_max = 4;
var zoom_min = 0.125;
var zoom_delta = 0;

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

    scale = zoom_delta * zoom_scale;

    // restriction of scaling
    scale = Math.min(Math.max(zoom_min, scale), zoom_max);

    //element.css("transform-origin", (x + mousePosX).toString() + "px " + (mousePosY + y).toString() + "px")
    $("#movable_scene").css("transform", "scale(" + scale + ")");

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