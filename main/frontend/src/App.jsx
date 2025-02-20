import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [tasks, setTasks] = useState([]);

  // Fetch tasks from the backend
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/tasks")
      .then((response) => {
        setTasks(response.data);
      })
      .catch((error) => {
        console.error("Error fetching tasks:", error);
      });
  }, []);

  // Function to toggle task completion
  const toggleCompletion = (taskId, currentStatus) => {
    axios
      .put(`http://127.0.0.1:5000/tasks/${taskId}`, {completed: !currentStatus})
      .then (() => {
        // Update tasks in frontend after succesful request
        setTasks((prevTasks) =>
          prevTasks.map((task) => 
            task.id === taskId ? { ...task, completed: !currentStatus } : task
          )
        );
      })
      .catch((error) => {
        console.error("Error updating task:", error);
      });
  };

  return (
    <div>
      <h1>Personal Life Coach</h1>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleCompletion(task.id, task.completed)}
            />
            <strong style={{ textDecoration: task.completed ? "line-through" : "none"}}>
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
