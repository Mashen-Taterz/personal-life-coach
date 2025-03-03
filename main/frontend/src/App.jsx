import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [tasks, setTasks] = useState([]);
  const [username, setUsername] = useState(""); // State for username
  const [email, setEmail] = useState(""); // State for email
  const [password, setPassword] = useState(""); // State for password
  const [userId, setUserId] = useState(null); // Store user session
  const [error, setError] = useState(null); // Store error message
  const [isRegistering, setIsRegistering] = useState(false); // Toggle between login & signup

  // Fetch tasks from the backend
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/tasks", { withCredentials: true}) // Allow session cookies
      .then((response) => {
        const updatedTasks = response.data.map((task) => ({
          ...task,
          completed: false, // Ensure all tasks start unchecked
        }));
        setTasks(updatedTasks); // Set tasks state with updated tasks
      })
      .catch((error) => {
        console.error("Error fetching tasks:", error);
      });

    // Check if user is logged in
    axios
      .get("http://127.0.0.1:5000/check-session", { withCredentials: true })
      .then((response) => {
        setUserId(response.data.user_id); // Set user session if logged in
      })
      .catch(() => setUserId(null));  
  }, []);

  // Function to toggle task completion
  const toggleCompletion = (taskId, currentStatus) => {
    console.log("Toggling task", taskId)
    if (!userId) {
      // Allow task completion toggling without login
      setTasks((prevTasks) =>
        prevTasks.map((task) =>
          task.id === taskId ? { ...task, completed: !currentStatus } : task
        )
      );
    } else {
      // If logged in, update the backend as well
      axios
        .put(
          `http://127.0.0.1:5000/tasks/${taskId}`,
          { completed: !currentStatus },
          { withCredentials: true }
        )
        .then(() => {
          // Update tasks in frontend after a successful request
          setTasks((prevTasks) =>
            prevTasks.map((task) =>
              task.id === taskId ? { ...task, completed: !currentStatus } : task
            )
          );
        })
        .catch((error) => {
          console.error("Error updating task:", error);
        });
    }
  };  

  // Handle login
  const handleLogin = () => {
    axios
      .post(
        "http://127.0.0.1:5000/login",
        { email, password },
        { withCredentials: true }
      )
      .then((response) => {
        setUserId(response.data.user_id);
        setUsername(response.data.username);
        setError(null);
        setEmail("");
        setPassword("");
      })
      .catch(() => setError("Invalid login credentials"));
  };

  // Handle signup (register)
  const handleSignup = () => {
    axios
      .post(
        "http://127.0.0.1:5000/register",
        { username, email, password },
        { withCredentials: true }
      )
      .then((response) => {
        setUserId(response.data.user_id); // Log in automatically after signup
        setError(null);
        setUsername("");
        setEmail("");
        setPassword("");
      })
      .catch(() => setError("Email already exists"));
  };

  // Handle logout
  const handleLogout = () => {
    axios
      .post("http://127.0.0.1:5000/logout", {}, { withCredentials: true })
      .then(() => {
        setUserId(null);
        setTasks(tasks.filter((task) => task.user_id === null)); // Show only default tasks
      });
  };

  return (
    <div>
      <h1>Personal Life Coach</h1>

      {/* Authentication Section */}
      {!userId ? (
        <div>
          {isRegistering ? (
            // Signup Form
            <div>
              <h2>Sign Up</h2>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button onClick={handleSignup}>Sign Up</button>
              <p>
                Already have an account?{" "}
                <button onClick={() => setIsRegistering(false)}>Login</button>
              </p>
            </div>
          ) : (
            // Login Form
            <div>
              <h2>Login</h2>
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button onClick={handleLogin}>Login</button>
              <p>
                No account?{" "}
                <button onClick={() => setIsRegistering(true)}>Sign Up</button>
              </p>
            </div>
          )}
          {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
      ) : (
        // Logout Button
        <div>
          <p>Logged in as {username ? username: "Guest"}</p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}

      {/* Task List */}
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleCompletion(task.id, task.completed)}
            />
            <strong style={{ textDecoration: task.completed ? "line-through" : "none" }}>
              {task.title}
            </strong>{" "}
            - {task.description} (Due: {task.due_date})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;