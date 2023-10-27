
var bannerimg = document.getElementById("bannerimg");
var bannerimgframe = document.getElementById("bannerimgframe");
var banner_placeholder = document.getElementById("banner_placeholder");
var loading_screen = document.getElementById("custom_loading_page");
var page_content = document.getElementById("page_content");


var first_img_to_animate = document.getElementById("first_img_to_animate");
var second_img_to_animate = document.getElementById("second_img_to_animate");
var third_img_to_animate = document.getElementById("third_img_to_animate");
var fourth_img_to_animate = document.getElementById("fourth_img_to_animate");
var fifth_img_to_animate = document.getElementById("fifth_img_to_animate");
var sixth_img_to_animate = document.getElementById("sixth_img_to_animate");


const elements_to_check = [
    first_img_to_animate,
    second_img_to_animate,
    third_img_to_animate,
    fourth_img_to_animate,
    fifth_img_to_animate,
    sixth_img_to_animate,

];

var number_of_elements_to_check = elements_to_check.length;
var boolean_for_if_animation_has_occured = new Array(number_of_elements_to_check).fill(false);
console.log(boolean_for_if_animation_has_occured);





// FINISH CHECKING IF ALL IMAGES ARE IN FRAME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


function inview_function(a, b) {
    // console.log(boolean_for_if_animation_has_occured[b]);
    if(!boolean_for_if_animation_has_occured[b]){

        var element_location = a.getBoundingClientRect();
        var element_top = element_location.top;
        var element_bottom = element_location.bottom;

        var element_is_visible = (element_top >= 0) && (element_bottom <= window.innerHeight);
        if(element_is_visible){
            console.log("it is alive " + b);
            a.classList.add("img_slidein_animation");
            a.style.visibility = "visible";
            boolean_for_if_animation_has_occured[b] = true;
        }
    }
    return true;
}

// animated_elements_inview.apply(elements_to_check);
function animated_elements_inview() {
    elements_to_check.every(inview_function);

}

document.addEventListener("scroll", animated_elements_inview);

// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!







function loaded_img_function() {
    console.log("test");
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