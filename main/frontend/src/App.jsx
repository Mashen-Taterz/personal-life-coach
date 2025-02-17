import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/tasks") // Replace with your actual backend URL
      .then((response) => {
        setTasks(response.data);
      })
      .catch((error) => {
        console.error("Error fetching tasks:", error);
      });
  }, []);

  return (
    <div>
      <h1>Personal Life Coach</h1>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <strong>{task.title}</strong> - {task.description} (Due: {task.due_date})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
