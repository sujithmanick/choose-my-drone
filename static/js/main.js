let mainNav = document.getElementById("js-menu");
let navBarToggle = document.getElementById("js-navbar-toggle");
let toggle = true;
navBarToggle.addEventListener("click", function () {
  
  if (toggle === true){
  navBarToggle.classList.remove("fa-bars");
  navBarToggle.classList.add("fa-close");
  mainNav.classList.toggle("active");
  toggle = false;}
  else{
    navBarToggle.classList.remove("fa-close");
  navBarToggle.classList.add("fa-bars");
  mainNav.classList.toggle("active");
  toggle = true;
  }
});
