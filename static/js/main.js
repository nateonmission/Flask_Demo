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


