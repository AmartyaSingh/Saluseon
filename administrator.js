function check() {
  var check = localStorage.getItem('complete');
  console.log(check);
  if (check == "yes") {
    document.getElementById("hidden").style.display = "block";
    document.getElementsByClassName("flex")[0].style.display = "none";
  }
}

function show(x) {
  document.getElementById("hidden").style.display = "block";
  localStorage.setItem('complete', "yes");
}

function hide(x) {
  document.getElementsByClassName("flex")[0].style.display = "none";
}
