var up = false,
    right = false,
    down = false,
    left = false,
    x = window.innerWidth/2-130/2,
    y = window.innerHeight/2-130/2
document.addEventListener('keydown',press)
function press(e){
  if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
    up = true
  }
  if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
    right = true
  }
  if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
    down = true
  }
  if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */ || e.keyCode === 81 /* q */){
    left = true
  }
}
document.addEventListener('keyup',release)
function release(e){
  if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
    up = false
  }
  if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
    right = false
  }
  if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
    down = false
  }
  if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */ || e.keyCode === 81 /* q */){
    left = false
  }
}
function gameLoop(){
  var div = document.querySelector('div')
  if (up){
    y = y - 10
  }
  if (right){
    x = x + 10
  }
  if (down){
    y = y + 10
  }
  if (left){
    x = x - 10
  }
  div.style.left = x+'px'
  div.style.top = y+'px'
  window.requestAnimationFrame(gameLoop)
}
window.requestAnimationFrame(gameLoop)

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

<<<<<<< HEAD
//setMap(); // when press button start

// setInterval(mode, 2000);

var notepad = document.getElementById("car_red");
notepad.addEventListener("contextmenu",function(event){
    event.preventDefault();
    var ctxMenu = document.getElementById("ctxMenu");
    ctxMenu.style.display = "block";
    ctxMenu.style.left = (event.pageX - 10)+"px";
    ctxMenu.style.top = (event.pageY - 10)+"px";
},false);
notepad.addEventListener("click",function(event){
    var ctxMenu = document.getElementById("ctxMenu");
    ctxMenu.style.display = "";
    ctxMenu.style.left = "";
    ctxMenu.style.top = "";
},false);

=======
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
>>>>>>> 230a52b8f0eab9d65bf432dca56545548d89b5a2
