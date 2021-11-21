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