
function showCars(event){
    var status = true;
    if (status) {
        $("#car").css("visibility", "visible");
    }
    
    
}

function showLights(event){
    var status = true;
    if (status) {
        $("#lights").css("visibility", "visible");
    }
    
}

function showRoads(event){
    var status = true;
    if (status) {
        $("#roads").css("visibility", "visible");
    }
    
}

function showMenu(event){
    var status = true;
    if (status) {
        $("#menu_param").css("visibility", "visible");
    }
    
}

function closeButton(event){
    var status = true;
    if (status) {
        $("#menu_param").css("visibility", "hidden");
        $("#roads").css("visibility", "hidden");
        $("#lights").css("visibility", "hidden");
        $("#car").css("visibility", "hidden");
    }
    
}

function closeCars(event){
    var status = true;
    if (status) {
        $("#car").css("visibility", "hidden");
    }
    
}

function closeLights(event){
    var status = true;
    if (status) {
        $("#lights").css("visibility", "hidden");
    }
    
}

function closeRoads(event){
    var status = true;
    if (status) {
        $("#roads").css("visibility", "hidden");
    }
    
}

function showLightsEditor(event){
    var status = true;
    if(status){
        $("#lights_editor").css("visibility", "visible");
    }
}
function closeLightsEditor(event){
    var status = true;
    if(status){
        $("#lights_editor").css("visibility", "hidden");
    }
}

function hide_all(event){
    var status = true;
    if(status){
        closeLightsEditor();
        document.querySelectorAll('.road_highlight').forEach(e => e.remove());
        // todo everything else as well
    }
}

function submit_lights_editor_form(){
    // need to check if user was typing in the right thing, (it should be positive and not blank)
    if(document.getElementById("green_period_input") == "0" ||
     document.getElementById("red_period_input") == "0") return;
    document.getElementById("lights_editor_form").submit();
    hide_all();
}