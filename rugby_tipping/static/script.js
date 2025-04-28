let main = document.getElementById("main") //get main element
let nav = document.getElementById("nav") //get main element
var icon = document.getElementById("hamburger-icon");

//function to show navlinks on small screens
function show_menu() {
    var menu = document.getElementById("nav-bar");
    if (menu.style.maxHeight === "0px") {
        menu.style.maxHeight = "240px"
        icon.className = "fa-solid fa-xmark" //show x
    }
    else {
        menu.style.maxHeight = "0"
        icon.className = "fa-solid fa-bars"; //show bars
    }
}

// observe window resize
eventThrottle(window, 'resize', resizeHandler);
resizeHandler();

// throttled event handler
// boilerplate for events
function eventThrottle(element, event, callback, delay = 1) {
    let throttle;
    element.addEventListener(event, (e) => {
        throttle = throttle || setTimeout(() => {
            throttle = null;
            callback(e);
        }, delay);
    });
}

// calculate size
function resizeHandler() {
    // get window width
    const iw = window.innerWidth;
    // determine named size
    let menu = document.getElementById("nav-bar");
    if (iw >= 650) {
        menu.style.maxHeight = "150px";
    }
    else if (iw < 650) {
        menu.style.maxHeight = "0"
        icon.className = "fa-solid fa-bars";
    }
}