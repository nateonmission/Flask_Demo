function to_do() {
  const x = document.getElementById("to_do").value;
  const edit = document.getElementById("edit");
  const create = document.getElementById("create");
  if(x == "Edit") {
      edit.style.display = "block";
      create.style.display = "none";
  }
  else if(x == "Create") {
      edit.style.display = "none";
      create.style.display = "block";
  }
}


function fade(element) {
    let op = 1;  // initial opacity
    const timer = setInterval(function () {
        if (op <= 0.1){
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
}


function unfade(element) {
    let op = 0.1;  // initial opacity
    element.style.display = 'block';
    const timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 10);
}


const flashField = document.getElementsByClassName("h1");

flashField.addEventListener("click", mine)

function mine() {
    flashField.style.backgroundColor = "Blue";
}


