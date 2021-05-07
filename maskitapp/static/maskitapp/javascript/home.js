var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0px";
  } else {
    document.getElementById("navbar").style.top = "-80px";
    
  }
  prevScrollpos = currentScrollPos;
  if(window.pageYOffset>20){
    document.getElementById("navbar").style.backgroundColor = "rgba(47, 88, 116, 1)";
  }
  else{
    document.getElementById("navbar").style.backgroundColor = "rgba(47, 88, 116, 0)";
  }
}