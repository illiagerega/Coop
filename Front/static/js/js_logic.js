

class Car {        
    constructor(id, x, y, rotation, speed, startNode, endNode){
    this.id = id;
    this.x = x;
    this.y = y;
    this.rotation = rotation;
    this.speed = speed;
    this.endNode =endNode;
    this.startNode = startNode;
}

    draw_car(){
       return  `<div class="car_red" id="${this.id}" onclick ="show_car(${this.id})" style="left: ${this.x}px; top: ${this.y}px; transform: rotate(${this.rotation}deg);"> </div>`;
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


function form_car_array(python_car_array_str){
        const startTime =new Date().getTime();   
        current_cars.clear();
        let python_car_array = JSON.parse(python_car_array_str);
        for(const [skey, value] of Object.entries(python_car_array)){
            let key = parseInt(skey);
            current_cars.set(key, new Car(key,parseFloat(value[0]), parseFloat(value[1]), parseFloat(value[2]), parseFloat(value[3]), parseInt(value[4]), parseInt(value[5])));

        }
        /*
        console.log("somehting:", this.new_cars.get(2));

        for(const [skey, value] of Object.entries(python_car_array)){
            let key = parseInt(skey);
            console.log(key);
            if(this.prev.has(key)){
                this.alive.set(key, new Car(key,parseFloat(value[0]), parseFloat(value[1]), parseFloat(value[2])));
                this.prev.delete(key);
                console.log("alive");
            }
            else{
                this.new_cars.set(key, new Car(key, parseFloat(value[0]), parseFloat(value[1]), parseFloat(value[2])));
                console.log("new", this.new_cars.get(key));
                console.log(this.new_cars.size);
            }
        }
        console.log("somehting:", this.new_cars.get(2));
        console.log(this.new_cars);
        console.log(python_car_array);
        console.log(this.new_cars.size);
        console.log(this.new_cars.entries());
        Array.from(this.new_cars.keys()).map(key => console.log(key));


        for(const [key, value] of Object.entries(this.new_cars)){
          
            const [key, value] = entry;
            console.log("hellojdsiojfdlskfj");
        }

        Array.from(this.prev.keys()).map(key =>
          this.dead.set(key, key));
        this.prev.clear();

        



        /*Object.entries(python_car_array).forEach((entry) => {
            const [key, value] = entry;
            if(this.living_cars.has(key)){
                this.living_cars.delete(key);
            }
        });
        console.log(this.living_cars);
        Object.entries(python_car_array).forEach((entry) => {
            const [key, value] = entry;
            if(this.living_cars.has(key)){
                this.car_array[key] = null;
                this.prev_car_array[key] = null;
            }
            else if(this.car_array[key] == null){
                this.car_array[key] = new Car(key, value[0], value[1], value[2]);
                this.living_cars.add(key);
            }
            else {
                this.prev_car_array[key] = this.car_array[key];
                this.car_array[key] = new Car(key, value[0], value[1], value[2]);
                this.living_cars.add(key);
            }
            
        
        });*/

        var endTime = new Date().getTime();
        console.log(`${2} time taken ${(endTime - startTime)/1000} seconds`);
        construct_cars();
        endTime = new Date().getTime();


        /*
        Array.from(current_cars.entries()).map(([key, value]) => {
            prev.set(key, value);
        });
        console.log(`${3} time taken ${(endTime - startTime)/1000} seconds`);
*/
}
function construct_cars(){
        let draw_cars = "";
        let draw_table = "";
        Array.from(current_cars.entries()).map(([key, value]) => {
            draw_cars += value.draw_car();
            draw_table += `<tr><td>${value.id}</td><td>${value.x}</td><td>${value.y}</td><td>${value.rotation}deg</td><td>${value.startNode}</td><td>${value.endNode}</td></tr>`;
        });
        document.getElementById("cars").innerHTML = draw_cars;
        /* WHY ISN'T IT WORKING????????????????????????????*/
        document.getElementById("cars_table").innerHTML = draw_table;
        
        /*
        let new_cars_html = "";
        Array.from(this.new_cars.entries()).map(([key, value]) => {
            new_cars_html += `<div class="car_red c${key}" id="${value.id}" style="left: ${value.x}px; top: ${value.y}px; transform: rotate(${value.rotation}deg);"> </div>`
            console.log("Drawing", key);

        });
        document.getElementById("cars").innerHTML += new_cars_html;
        Array.from(this.alive.entries()).map(([key, value]) => {
            
            console.log("ALIVE", key, value);
            let div = document.getElementById(key);
            anime.timeline().add({
                targets: `.c${key}`,
                rotate:  `rotate(${value.rotation}deg)`,
            }).add({
                targets: `.c${key}`,
                translateX: Math.sqrt((parseFloat(div.style.left)-value.x)*(parseFloat(div.style.left)-value.x)+(parseFloat(div.style.top)-value.y)*(parseFloat(div.style.top)-value.y))
                
            });
              div.style.left = `${value.x}`;
              div.style.top = `${value.y}`;
              div.style.transform = `rotate(${value.rotation}deg)`;
              console.log(value.rotation);
        });
        Array.from(this.dead.keys()).map(key =>
            document.getElementById(`${key}`).innerHTML = "");
        this.dead.clear();
    */
}
function show_car(car_id){
    if(!paused) return;
    hide_all();
    let car = current_cars.get(car_id);
    
    //alert(`Id: ${car.id}, x: ${car.x}, y:${car.y}, Someone make this menu pretty`);
    highlight_path(car_id);
}

function form_lights_array(lights_str){ // [id, sublights[], green_period, red_period]
    //document.getElementById("lights_movable").innerHTML = lights_str["lights"];
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
                    if(i == 0){
                        delta_height = parseFloat($(`#${car_id}`).css('top'), 10) - parseFloat($(`#road_${road_id}`).css('top'), 10); 
                    }
                    console.log(delta_height, original_road.style.posTop);
                    var highlighted_road = original_road.cloneNode(true);
                    highlighted_road.id = `#highlighted_road_${road_id}`;
                    if(current_cars.get(parseInt(car_id)).rotation < 90){
                        highlighted_road.style.marginTop = `14px`;
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
