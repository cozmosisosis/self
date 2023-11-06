
var bannerimg = document.getElementById("bannerimg");
var bannerimgframe = document.getElementById("bannerimgframe");
var banner_placeholder = document.getElementById("banner_placeholder");
var loading_screen = document.getElementById("custom_loading_page");
var page_content = document.getElementById("page_content");

var waste_content = document.getElementById("pills-waste-content");






// all draging code start


var sliding_container = document.getElementById("sliding_container");
var sliding_content = document.getElementById("sliding_content");

var mouse_is_over = false;
var x_drag_starting_value;
var animation_finished = false;
var active_drag = false;
var sliding_content_style_left_int;


// drag start function    start
function drag_start_function(e) {

    // e.preventDefault();
    if (!animation_finished) { return; }
    sliding_content_style_left_int = parseInt(sliding_content.style.left);
    if (e.type === "touchstart") {
        x_drag_starting_value = e.touches[0].clientX;
    }
    else {
        x_drag_starting_value = e.clientX;

    }
    active_drag = true;

}
// drag start function    end


// drag function start
function drag_function(e) {

    if (!animation_finished || !active_drag) { return; };
    // e.preventDefault();

    var x_new_value_from_drag;

    if (e.type === "touchmove") {
        x_new_value_from_drag = e.touches[0].clientX - x_drag_starting_value;
    }
    else {
        x_new_value_from_drag = e.clientX - x_drag_starting_value;
    }


    set_position_function(x_new_value_from_drag);
    if (!mouse_is_over) { return; };


}
// drag function end


// drag end function start
function drag_end_function(e) {
    // e.preventDefault();

    if (!active_drag) { return; }

    var x_new_value_from_drag;
    if (e.type === "touchend") {
        // x_new_value_from_drag = e.touches[0].clientX - x_drag_starting_value;
    }
    else if (e.type === "mouseup") {
        // x_new_value_from_drag = e.clientX - x_drag_starting_value;
    }
    else {
        mouse_is_over = false;
        active_drag = false;
        return;
    }

    active_drag = false;
    // set_position_function(x_new_value_from_drag);
}
// drag end function end


// set position function start
function set_position_function(x) {

    var left_offset_min = 50;
    var left_offset_max = -(sliding_content.offsetWidth - sliding_container.offsetWidth + left_offset_min);

    if ((sliding_content_style_left_int + x) >= left_offset_min) {
        sliding_content.style.left = left_offset_min + "px";
        return;
    }
    else if ((sliding_content_style_left_int + x) <= left_offset_max) {
        sliding_content.style.left = left_offset_max + "px";
        return
    }
    else {
        sliding_content.style.left = (sliding_content_style_left_int + x) + "px";
        return;
    }
}
// set position function end



// event listeners for draging content start

sliding_content.addEventListener("animationstart", () => { animation_finished = true; setTimeout(() => { sliding_content.classList.remove("sliding-left-animation"); }, 2000) });

sliding_container.addEventListener("mousedown", drag_start_function);
sliding_container.addEventListener("touchstart", drag_start_function);

sliding_container.addEventListener("mousemove", drag_function);
sliding_container.addEventListener("touchmove", drag_function);

sliding_container.addEventListener("mouseup", drag_end_function);
sliding_container.addEventListener("touchend", drag_end_function);
sliding_container.addEventListener("mouseout", drag_end_function);

sliding_container.addEventListener("mouseover", () => { mouse_is_over = true; });

// event listeners for draging content end
// all draging code end





//  slide in and fade in animation start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


var first_img_to_animate = document.getElementById("first_img_to_animate");
var second_img_to_animate = document.getElementById("second_img_to_animate");
var third_img_to_animate = document.getElementById("third_img_to_animate");
var fourth_img_to_animate = document.getElementById("fourth_img_to_animate");
var fifth_img_to_animate = document.getElementById("fifth_img_to_animate");
var sixth_img_to_animate = document.getElementById("sixth_img_to_animate");
var first_animated_paragraph = document.getElementById("first_animated_paragraph");
var second_animated_paragraph = document.getElementById("second_animated_paragraph");
var third_animated_paragraph = document.getElementById("third_animated_paragraph");
var first_sm_animated_paragraph = document.getElementById("first_sm_animated_paragraph");
var second_sm_animated_paragraph = document.getElementById("second_sm_animated_paragraph");
var third_sm_animated_paragraph = document.getElementById("third_sm_animated_paragraph");


const elements_to_check = [
    first_img_to_animate,
    second_img_to_animate,
    third_img_to_animate,
    fourth_img_to_animate,
    fifth_img_to_animate,
    sixth_img_to_animate,
    first_animated_paragraph,
    second_animated_paragraph,
    third_animated_paragraph,
    first_sm_animated_paragraph,
    second_sm_animated_paragraph,
    third_sm_animated_paragraph

];

var number_of_elements_to_check = elements_to_check.length;
var boolean_for_if_animation_has_occured = new Array(number_of_elements_to_check).fill(false);







function inview_function(a, b) {

    if (!boolean_for_if_animation_has_occured[b]) {

        var element_location = a.getBoundingClientRect();
        var element_top = element_location.top;
        var element_bottom = element_location.bottom;

        var element_is_visible = (element_top >= 0) && (element_bottom <= window.innerHeight);
        if (element_is_visible) {
            if (a.tagName == "IMG") {
                a.classList.add("img_slidein_animation");
                a.style.visibility = "visible";
                setTimeout(() => (a.classList.remove("img_slidein_animation")), 3000);
            }
            if (a.tagName == "P") {
                a.classList.add("paragraph_fadein_animation");
                a.style.opacity = "100%";
                setTimeout(() => (a.classList.remove("paragraph_fadein_animation")), 3000);
            }
            boolean_for_if_animation_has_occured[b] = true;
        }
    }

    return true;
}

// animated_elements_inview.apply(elements_to_check);
function animated_elements_inview() {
    if (waste_content.classList.contains("active") && waste_content.classList.contains("show")) {
        elements_to_check.every(inview_function);
    }

}

document.addEventListener("scroll", animated_elements_inview);



//  slide in and fade in animation end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!






function loaded_img_function() {
    bannerimgframe.setAttribute("style", "display: block;");
    banner_placeholder.setAttribute("style", "visibility: hidden;");

}


// Function for banner image placeholder
bannerimg.addEventListener("load", loaded_img_function(event));

// Enables popover buttons
const popoverTriggerList_contact_info = document.querySelectorAll('[data-bs-toggle="contact_info_popover"]');
const popoverList_contact_info = [...popoverTriggerList_contact_info].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

const popoverTriggerList_careers = document.querySelectorAll('[data-bs-toggle="careers_popover"]');
const popoverList_careers = [...popoverTriggerList_careers].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

const popoverTriggerList_more = document.querySelectorAll('[data-bs-toggle="more_popover"]');
const popoverList_careers_more = [...popoverTriggerList_more].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));


// Signals when all images are loaded
Promise.all(Array.from(document.images).map(img => {
    if (img.complete)
        return Promise.resolve(img.naturalHeight !== 0);
    return new Promise(resolve => {
        img.addEventListener('load', () => resolve(true));
        img.addEventListener('error', () => resolve(false));
    });
})).then(results => {
    loading_screen.setAttribute("style", "display: none;");
    page_content.setAttribute("style", "display: block;");
    if (results.every(res => res))
        console.log('all images loaded successfully');
    else
        console.log('some images failed to load, all finished loading');
});
