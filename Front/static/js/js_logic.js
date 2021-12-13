

class Car {        
    constructor(id, x, y, rotation, speed, startNode, endNode, color){
    this.id = id;
    this.x = x;
    this.y = y;
    this.rotation = rotation;
    this.speed = speed;
    this.endNode =endNode;
    this.startNode = startNode;
    this.color = color;
}

    draw_car(){
       return  `<div class="car ${this.color}" id="${this.id}" onclick ="show_car(${this.id})" style="left: ${this.x}px; top: ${this.y}px; transform: rotate(${this.rotation}deg);"> </div>`;
    }

}

class Light{
    constructor(id, sublights, green_period, red_period){
        this.id = id;
        this.sublights = sublights;
        this.green_period = green_period;
        this.red_period = red_period;
    }

    draw_light(){
        let light_html = `<div class="light" id="light_${this.id}">`
        for(sublight of this.sublights){
            light_html += sublight.draw_sublight();
        }
        light_html += "</div>";
        return light_html;
        
    }
}
class Sublight{
    constructor(x, y, rotation, color){
        this.x = x;
        this.y = y;
        this.rotation = rotation;
        this.color = color;
    }
    draw_sublight(){
        return `<div class="sublight" style="left: ${this.x}px; top: ${this.y}px; transform: rotate(${this.rotation}deg); background-color: ${this.color}"> </div>`;
    }

}


//new_cars = new Map();
current_cars = new Map(); 
//prev = new Map();
//dead = new Map();
current_lights = new Map();


function add_car_to_dictionary_from_string(_map, string_key, string_value){
    let key = parseInt(string_key)
    _map.set(key, new Car(key,parseFloat(string_value[0]), parseFloat(string_value[1]), parseFloat(string_value[2]),
     parseFloat(string_value[3]), parseInt(string_value[4]), parseInt(string_value[5]), string_value[6]));
}






function form_car_array(python_car_array_str){


        const startTime =new Date().getTime();   
        current_cars.clear();
        let python_car_array = JSON.parse(python_car_array_str);
 
        for(const [skey, value] of Object.entries(python_car_array)){
            add_car_to_dictionary_from_string(current_cars, skey, value);
        }

        var endTime = new Date().getTime();
        console.log(`${2} time taken ${(endTime - startTime)/1000} seconds`);
        construct_cars();
        endTime = new Date().getTime();
}


function construct_cars(){
        let draw_cars = "";
        Array.from(current_cars.entries()).map(([key, value]) => {
            draw_cars += value.draw_car();
        });
        document.getElementById("cars").innerHTML = draw_cars;
}
function show_car(car_id){
    if(!paused) return;
    hide_all();
    let car = current_cars.get(car_id);
    showCarsEditor();
    highlight_path(car_id);
}

function form_lights_array(lights_str){ // [id, sublights[], green_period, red_period]
     lights_python_array = JSON.parse(lights_str);
     for(const [skey, value] of Object.entries(lights_python_array)){
        let key = parseInt(skey);
        let sublights = new Array();
        for(sublight of value[1]){
            sublights.push(new Sublight(parseFloat(sublight[0]), parseFloat(sublight[1]), parseFloat(sublight[2]), sublight[3]))
        }
        current_lights.set(key, new Light(value[0], sublights, value[2], value[3]));
    }
   
    construct_lights();

}
function construct_lights(){
    let draw_lights_html = "";
    Array.from(current_lights.entries()).map(([key, value]) => {
        draw_lights_html += value.draw_light();
        
    });
    document.getElementById("lights_movable").innerHTML = draw_lights_html;
}

function get_light_editor(light_index){
    if(!current_lights.has(light_index) || !paused) return;
    hide_all();

    showLightsEditor();
    let curr_light = current_lights.get(light_index);
    document.getElementById("red_period_input").value=curr_light.red_period;
    document.getElementById("green_period_input").value=curr_light.green_period;
    document.getElementById("light_id").value=light_index;
}

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
            let json_response = JSON.parse(response);
            form_car_array(json_response["cars"]);
            form_lights_array(json_response["lights"]);
            map_ajax_state_sending = false;
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

function highlight_path(car_id)
{
    if(!map_ajax_state_sending){
        map_ajax_state_sending = true
        $.ajax({
            url: "/util_ajax",
            type: "post",
            data: {operation: "getCarPath", car_index: car_id},
            cache: false,
            success: function(response) {
                //$('#map').html(response);
                //console.log(response);
                let roads = JSON.parse(response)["way"];
                console.log(roads);
                let i = 0;
                let delta_height = 0;
                for(road_id of roads){
                    
                    var original_road = document.querySelector(`#road_${road_id}`)
                    var highlighted_road = original_road.cloneNode(true);
                    highlighted_road.id = `#highlighted_road_${road_id}`;
                    if(current_cars.get(parseInt(car_id)).rotation < 90){
                        highlighted_road.style.marginTop = `17.5px`;
                    }

                    highlighted_road.classList = ('road_highlight');

                    original_road.after(highlighted_road);
                    i++;
                }
                map_ajax_state_sending = false;
            },
        });
    }
}

function setPrice()
{
    if(!map_ajax_state_sending){
        map_ajax_state_sending = true
        $.ajax({
            url: "/price",
            type: "get",
            cache: false,
            success: function(response) {
                $('#price_info').html(response);
                console.log(response);
                map_ajax_state_sending = false;
            },
        });
    }
}