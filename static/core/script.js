const input = document.getElementById("taskInput");
const addBtn = document.getElementById("addBtn");
const taskList = document.getElementById("taskList");

addBtn.addEventListener("click", addTask);
input.addEventListener("keypress", function (e) {
  if (e.key === "Enter") addTask();
});

function addTask() {
  let task = input.value.trim();
  if (task === "") return;

  let li = document.createElement("li");
  li.textContent = task;

  // click to mark done
  li.addEventListener("click", function () {
    li.classList.toggle("completed");
  });

  // delete button
  let del = document.createElement("button");
  del.textContent = "Xóa";
  del.className = "delete-btn";
  del.onclick = function () {
    li.remove();
  };

  li.appendChild(del);
  taskList.appendChild(li);

  input.value = "";
}
