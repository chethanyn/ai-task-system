import { useState } from "react";
import API from "./api";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  // 🔐 LOGIN
  const login = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: email.trim().toLowerCase(),
          password: password.trim()
        })
      });

      const data = await res.json();

      console.log("STATUS:", res.status);
      console.log("RESPONSE:", data);

      if (!res.ok) {
        alert("ERROR: " + data.detail);
        return;
      }

      localStorage.setItem("token", data.access_token);

      alert("Login successful ✅");

      getTasks(); // ✅ auto load tasks after login

    } catch (error) {
      console.error("FETCH ERROR:", error);
      alert("Network error ❌");
    }
  };

  // 📋 GET TASKS
  const getTasks = async () => {
    try {
      const res = await API.get("/tasks/");
      console.log("TASKS:", res.data);
      setTasks(res.data);
    } catch (error) {
      console.error("ERROR:", error.response?.data || error.message);
      alert("Failed to load tasks ❌");
    }
  };

  // ➕ CREATE TASK
  const createTask = async () => {
    if (!newTask.trim()) {
      alert("Enter task first ⚠️");
      return;
    }

    try {
      await API.post("/tasks/", {
        title: newTask,
        status: "pending"
      });

      setNewTask("");
      getTasks();

    } catch (error) {
      console.error(error);
      alert("Failed to create task ❌");
    }
  };

  // ✅ COMPLETE TASK
  const completeTask = async (id) => {
    try {
      await API.put(`/tasks/${id}`, { status: "completed" });
      getTasks();
    } catch (error) {
      console.error(error);
      alert("Failed to update task ❌");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Login</h2>

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br /><br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br /><br />

      <button onClick={login}>Login</button>

      <hr />

      <h2>Create Task</h2>

      <input
        placeholder="Enter new task..."
        value={newTask}
        onChange={(e) => setNewTask(e.target.value)}
      />

      <button onClick={createTask}>Add Task</button>

      <hr />

      <h2>Tasks</h2>
      <button onClick={getTasks}>Load Tasks</button>

      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            <strong>{t.title}</strong>{" "}
            <span style={{ color: t.status === "completed" ? "green" : "orange" }}>
              ({t.status})
            </span>

            <button
              onClick={() => completeTask(t.id)}
              disabled={t.status === "completed"}
              style={{ marginLeft: "10px" }}
            >
              Complete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;