

// assigning buttons
var left_button = document.getElementById("button_left");
var right_button = document.getElementById("button_right");
var about_author_button = document.getElementById("about_author_button");
var page_topic = document.getElementById("page_topic");
var contact_info_button = document.getElementById("contact_info_button");
var homepage_button = document.getElementById("homepage_button");
// assigning buttons end



// images variables
var images = document.getElementById("images_id");
var image_min_limit = -300;
var image_max_limit = 0;
var images_computed = window.getComputedStyle(images);
var xStartingOffset = images_computed.getPropertyValue("translate");
var move_x_value_pre = parseInt(xStartingOffset);
// images variables end

// slides variables
var text_slides = document.getElementById("slide_outer");
var computed_text_slides = window.getComputedStyle(text_slides);
var text_starting_x = computed_text_slides.getPropertyValue("translate");
var text_starting_x_int = parseInt(text_starting_x);
// slides variables end

//variables for seperate content
var content_about_author = document.getElementById("content_about_author");
var content_page_topic = document.getElementById("content_page_topic");
var content_contact_info = document.getElementById("content_contact_info");
//variables for seperate content end



var left_animating = false;
var right_animating = false;



function left_button_function(){

    if( move_x_value_pre == image_max_limit){
        console.log("left max image limit");
        return
    }

    //animation inprogress check
    if(left_animating || right_animating){
        console.log("animation in progress");
        return
    }
    console.log("left starting animation");
    left_animating = true;
    //animation inprogress check end


    //animation
    //images
    move_x_value_pre = move_x_value_pre + 100;
    var move_x_value_post = `${move_x_value_pre}%`;


    image_animation_status =
    images.animate(
        [
            { transform: "translateX(0%)" },
            { transform: "translateX(100%)" },
        ],
        { duration: 2000,
            easing: "ease-in-out"},
    );
    image_animation_status.onfinish = (event) => {

        images.style.setProperty("translate", move_x_value_post);
    }
    //images end


    //slides
    text_starting_x_int = text_starting_x_int + 40;
    var text_new_x_value = `${text_starting_x_int}em`

    slides_animation_status =
    text_slides.animate(
        [
            { transform: "translateX(0em)" },
            { transform: "translateX(40em)" },
        ],
            { duration: 2000,
              easing: "ease-in-out"},
        );
    slides_animation_status.onfinish = (event) => {

        text_slides.style.setProperty("translate", text_new_x_value);
    }
    //slides end
    //animation end

    //animation inprogress reset
    setTimeout(() => {
        left_animating = false;
        console.log("left done animating");
    }, 2000);
    //animation inprogress reset end

}

function right_button_function(){

    if(move_x_value_pre == image_min_limit){
        console.log("right min image limit");
        return
    }

    //animation inprogress check
    if(right_animating || left_animating){
        console.log("animation in progress");
        return
    }
    console.log("right starting animation");
    right_animating = true;
    //animation inprogress check end

    move_x_value_pre = move_x_value_pre - 100;
    var move_x_value_post = `${move_x_value_pre}%`;

    //animation
    //images
    image_animation_status =
    images.animate(
        [
            { transform: "translateX(0%)" },
            { transform: "translateX(-100%)" },
        ],
        { duration: 2000,
            easing: "ease-in-out"},
    );
    image_animation_status.onfinish = (event) => {

        images.style.setProperty("translate", move_x_value_post);
    }
    //images end

    //slides
    text_starting_x_int = text_starting_x_int - 40;
    var text_new_x_value = `${text_starting_x_int}em`

    slides_animation_status =
    text_slides.animate(
        [
            { transform: "translateX(0em)" },
            { transform: "translateX(-40em)" },
        ],
            { duration: 2000,
                easing: "ease-in-out"},
        );
    slides_animation_status.onfinish = (event) => {

        text_slides.style.setProperty("translate", text_new_x_value);
    }
    //slides end
    //animation end

    //animation inprogress reset
    setTimeout(() => {
        right_animating = false;
        console.log("right done animating");
    }, 2000);
    //animation inprogress reset end
}

function homepage_function(){
    window.location.href = '../homepage/index.html';
}

function about_author_function(){
    if(content_about_author.style.display == "none" && !left_animating && !right_animating){
        content_page_topic.style.display = "none";
        content_contact_info.style.display = "none";
        content_about_author.style.display = "flex";
    }
}

function synergistic_ideas_function(){
    if(content_page_topic.style.display == "none"){
        content_about_author.style.display = "none";
        content_contact_info.style.display = "none";
        content_page_topic.style.display = "flex";
    }
}

function contact_info_function(){
    if(content_contact_info.style.display == "none" && !left_animating && !right_animating){
        content_about_author.style.display = "none";
        content_page_topic.style.display = "none";
        content_contact_info.style.display = "flex";
    }
}

left_button.addEventListener("click", left_button_function);
right_button.addEventListener("click", right_button_function);
homepage_button.addEventListener("click", homepage_function);
about_author_button.addEventListener("click", about_author_function);
page_topic.addEventListener("click", synergistic_ideas_function);
contact_info_button.addEventListener("click", contact_info_function);
// cool website https://css-tricks.com/emulating-css-timing-functions-javascript/
