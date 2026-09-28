// ==========================================
// CONFIG
// ==========================================
const API_BASE_URL = "http://127.0.0.1:8000";

// ==========================================
// GLOBAL STATE
// ==========================================
let authToken = localStorage.getItem("token") || null;
let currentUser = JSON.parse(localStorage.getItem("user") || "null");
let editingId = null;
let modalType = null;

const $ = (id) => document.getElementById(id);

console.log("=== script.js loaded ===");

// ==========================================
// SWITCH LOGIN <-> SIGNUP
// ==========================================
$("switchFormBtn").addEventListener("click", (e) => {
  e.preventDefault();
  const loginForm = $("loginForm");
  const signupForm = $("signupForm");
  const switchText = $("switchText");
  const switchBtn = $("switchFormBtn");
  const subtitle = $("formSubtitle");

  if (loginForm.classList.contains("hidden")) {
    loginForm.classList.remove("hidden");
    signupForm.classList.add("hidden");
    subtitle.textContent = "Login to continue";
    switchText.textContent = "Don't have an account?";
    switchBtn.textContent = "Sign Up";
  } else {
    loginForm.classList.add("hidden");
    signupForm.classList.remove("hidden");
    subtitle.textContent = "Create a new account";
    switchText.textContent = "Already have an account?";
    switchBtn.textContent = "Login";
  }
  $("loginError").textContent = "";
});

// ==========================================
// SIGNUP
// ==========================================
$("signupForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("loginError").textContent = "";

  const body = {
    username: $("signupUsername").value.trim(),
    email: $("signupEmail").value.trim(),
    password: $("signupPassword").value,
  };

  try {
    const res = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Signup failed");
    alert("Account created successfully! Please login.");
    $("switchFormBtn").click();
  } catch (err) {
    $("loginError").textContent = err.message;
  }
});

// ==========================================
// LOGIN
// ==========================================
$("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("loginError").textContent = "";

  const email = $("loginEmail").value.trim();
  const password = $("loginPassword").value;

  try {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Invalid email or password");

    authToken = data.token || data.access_token;
    if (!authToken) throw new Error("Token missing in response");

    currentUser = { email };
    localStorage.setItem("token", authToken);
    localStorage.setItem("user", JSON.stringify(currentUser));
    showApp();
  } catch (err) {
    $("loginError").textContent = err.message;
  }
});

// ==========================================
// LOGOUT
// ==========================================
$("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  authToken = null;
  currentUser = null;
  $("app").classList.add("hidden");
  $("loginPage").classList.remove("hidden");
});

// ==========================================
// SHOW APP
// ==========================================
function showApp() {
  $("loginPage").classList.add("hidden");
  $("app").classList.remove("hidden");
  $("welcomeUser").textContent = `Welcome, ${currentUser?.email || "User"}`;
  loadDashboard();
}

// ==========================================
// AUTH HEADERS
// ==========================================
function authHeaders() {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${authToken}`,
  };
}

function handleUnauthorized(res) {
  if (res.status === 401) {
    alert("Session expired. Please login again.");
    $("logoutBtn").click();
    return true;
  }
  return false;
}

// ==========================================
// SIDEBAR NAV
// ==========================================
document.querySelectorAll(".menu-item").forEach((item) => {
  item.addEventListener("click", (e) => {
    e.preventDefault();
    const page = item.dataset.page;
    document.querySelectorAll(".menu-item").forEach((m) => m.classList.remove("active"));
    item.classList.add("active");
    document.querySelectorAll(".page").forEach((p) => p.classList.remove("active-page"));
    $(`${page}Page`).classList.add("active-page");

    if (page === "dashboard") loadDashboard();
    if (page === "employees") loadEmployees();
    if (page === "tasks") loadTasks();
  });
});

// ==========================================
// DASHBOARD
// ==========================================
async function loadDashboard() {
  try {
    const [empRes, taskRes] = await Promise.all([
      fetch(`${API_BASE_URL}/emp/`, { headers: authHeaders() }),
      fetch(`${API_BASE_URL}/task/`, { headers: authHeaders() }),
    ]);
    if (handleUnauthorized(empRes) || handleUnauthorized(taskRes)) return;

    const employees = empRes.ok ? await empRes.json() : [];
    const tasks = taskRes.ok ? await taskRes.json() : [];

    $("totalEmployees").textContent = employees.length;
    $("totalTasks").textContent = tasks.length;
    $("pendingTasks").textContent = 0;
    $("completedTasks").textContent = 0;
  } catch (err) {
    console.error("Dashboard load failed:", err);
  }
}

// ==========================================
// EMPLOYEES
// ==========================================
async function loadEmployees() {
  try {
    const res = await fetch(`${API_BASE_URL}/emp/`, { headers: authHeaders() });
    if (handleUnauthorized(res)) return;
    const employees = await res.json();

    const tbody = $("employeesTable");
    tbody.innerHTML = "";

    if (!employees.length) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:#999;">No employees found</td></tr>`;
    } else {
      employees.forEach((emp) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${emp.emp_id}</td>
          <td>${emp.emp_name || "-"}</td>
          <td>${emp.emp_department || "-"}</td>
          <td>${emp.emp_salary ?? "-"}</td>
          <td>
            <button class="btn-sm btn-edit" onclick="editEmployee(${emp.emp_id})">Edit</button>
            <button class="btn-sm btn-delete" onclick="deleteEmployee(${emp.emp_id})">Delete</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }
    window._employees = employees;
  } catch (err) {
    console.error("Failed to load employees:", err);
  }
}

$("addEmployeeBtn").addEventListener("click", () => openModal("employee"));

// ==========================================
// MODAL
// ==========================================
function openModal(type, data = null) {
  modalType = type;

  if (type === "employee") {
    editingId = data?.emp_id || null;
  } else {
    editingId = data?.task_id || null;
  }

  $("modal").classList.remove("hidden");
  $("modalTitle").textContent =
    (editingId ? "Edit " : "Add ") + (type === "employee" ? "Employee" : "Task");

  const form = $("modalForm");
  form.innerHTML = "";

  if (type === "employee") {
    form.innerHTML = `
      <input type="text" id="f_name" placeholder="Employee Name" value="${data?.emp_name || ""}" required />
      <input type="text" id="f_department" placeholder="Department" value="${data?.emp_department || ""}" required />
      <input type="number" step="0.01" id="f_salary" placeholder="Salary" value="${data?.emp_salary ?? ""}" required />
    `;
  } else {
    form.innerHTML = `
      <input type="number" id="f_emp_id" placeholder="Employee ID" value="${data?.emp_id || ""}" required />
      <input type="text" id="f_task_name" placeholder="Task Name" value="${data?.task_name || ""}" required />
    `;
  }
}

$("cancelBtn").addEventListener("click", () => {
  console.log("### CANCEL CLICKED ###");
  $("modal").classList.add("hidden");
});

$("saveBtn").addEventListener("click", async () => {
  console.log("### SAVE CLICKED ### modalType:", modalType, "editingId:", editingId);
  try {
    if (modalType === "employee") {
      const body = {
        emp_name: $("f_name").value,
        emp_department: $("f_department").value,
        emp_salary: parseFloat($("f_salary").value),
      };
      const url = editingId
        ? `${API_BASE_URL}/emp/?emp_id=${editingId}`
        : `${API_BASE_URL}/emp/`;
      const method = editingId ? "PUT" : "POST";
      const res = await fetch(url, {
        method,
        headers: authHeaders(),
        body: JSON.stringify(body),
      });
      if (handleUnauthorized(res)) return;
      if (!res.ok) throw new Error(await res.text());
      loadEmployees();
    } else {
      const empId = parseInt($("f_emp_id").value);
      const taskName = $("f_task_name").value;
      const url = editingId
        ? `${API_BASE_URL}/task/${editingId}`
        : `${API_BASE_URL}/task/assign`;
      const method = editingId ? "PUT" : "POST";
      const res = await fetch(url, {
        method,
        headers: authHeaders(),
        body: JSON.stringify({ emp_id: empId, task_name: taskName }),
      });
      if (handleUnauthorized(res)) return;
      if (!res.ok) throw new Error(await res.text());
      loadTasks();
    }
    $("modal").classList.add("hidden");
  } catch (err) {
    console.error("### SAVE ERROR ###", err);
    alert("Save failed: " + err.message);
  }
});

// ==========================================
// EDIT / DELETE EMPLOYEE
// ==========================================
window.editEmployee = (id) => {
  console.log("### editEmployee called ###", id);
  const emp = (window._employees || []).find((e) => e.emp_id === id);
  if (emp) openModal("employee", emp);
};

window.deleteEmployee = async (id) => {
  if (!confirm("Delete this employee?")) return;
  const res = await fetch(`${API_BASE_URL}/emp/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (handleUnauthorized(res)) return;
  loadEmployees();
  loadDashboard();
};

// ==========================================
// TASKS
// ==========================================
async function loadTasks() {
  console.log("### loadTasks STARTED ###");
  try {
    const res = await fetch(`${API_BASE_URL}/task/`, { headers: authHeaders() });
    console.log("### task fetch status:", res.status);
    if (handleUnauthorized(res)) return;
    const tasks = await res.json();
    console.log("### tasks received:", tasks);

    const tbody = $("tasksTable");
    tbody.innerHTML = "";

    if (!tasks.length) {
      tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:#999;">No tasks found</td></tr>`;
    } else {
      tasks.forEach((task) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${task.task_id}</td>
          <td>${task.task_name}</td>
          <td>${task.emp_id}</td>
          <td>
            <button class="btn-sm btn-edit" onclick="editTask(${task.task_id})">Edit</button>
            <button class="btn-sm btn-delete" onclick="deleteTask(${task.task_id})">Delete</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    window._tasks = tasks;
    console.log("### window._tasks set:", window._tasks);
  } catch (err) {
    console.error("### loadTasks ERROR ###", err);
  }
}

$("addTaskBtn").addEventListener("click", () => openModal("task"));

window.editTask = (id) => {
  console.log("### editTask called ###", id);
  const task = (window._tasks || []).find((t) => t.task_id === id);
  console.log("### found task:", task);
  if (task) openModal("task", task);
};

window.deleteTask = async (id) => {
  if (!confirm("Delete this task?")) return;
  const res = await fetch(`${API_BASE_URL}/task/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (handleUnauthorized(res)) return;
  loadTasks();
  loadDashboard();
};

// ==========================================
// AUTO LOGIN
// ==========================================
if (authToken && currentUser) {
  showApp();
}