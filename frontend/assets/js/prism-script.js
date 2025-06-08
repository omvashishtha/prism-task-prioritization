document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addTaskForm");
    const API_BASE_URL = "http://127.0.0.1:5000"; // Change if hosted elsewhere

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const title = document.getElementById("title").value.trim();
        const description = document.getElementById("description").value.trim();
        const deadline = document.getElementById("deadline").value;

        if (!title || !description || !deadline) {
            alert("Please fill in all fields.");
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/add-task`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ title, description, deadline })
            });

            const data = await response.json();

            if (data.success) {
                displayTaskInMatrix(data.task);
                form.reset();
            } else {
                alert("Error: Could not create task.");
            }

        } catch (error) {
            console.error("Error adding task:", error);
            alert("Server error. Please try again later.");
        }
    });

    function displayTaskInMatrix(task) {
        const { title, description, deadline, priority, quadrant } = task;

        const taskCard = document.createElement("div");
        taskCard.classList.add("task-card");
        taskCard.style.border = "1px solid #ccc";
        taskCard.style.borderRadius = "8px";
        taskCard.style.padding = "10px";
        taskCard.style.margin = "10px 0";
        taskCard.style.background = "#f9f9f9";
        taskCard.innerHTML = `
            <strong>${title}</strong><br/>
            <small><em>${description}</em></small><br/>
            <span>Deadline: ${deadline}</span><br/>
            <span>Priority: ${priority}</span>
        `;

        let targetDiv = "";

        switch (quadrant) {
            case "Important & Urgent":
                targetDiv = "important-urgent";
                break;
            case "Important, Not Urgent":
                targetDiv = "important-not-urgent";
                break;
            case "Not Important, Urgent":
                targetDiv = "not-important-urgent";
                break;
            case "Not Important, Not Urgent":
                targetDiv = "not-important-not-urgent";
                break;
            default:
                targetDiv = "not-important-not-urgent";
        }

        document.querySelector(`#${targetDiv} .tasks-list`).appendChild(taskCard);
    }

    // Optional: Load all existing tasks on page load
    async function loadTasks() {
        try {
            const response = await fetch(`${API_BASE_URL}/tasks`);
            const data = await response.json();

            if (data.success && Array.isArray(data.tasks)) {
                data.tasks.forEach(task => displayTaskInMatrix(task));
            }
        } catch (error) {
            console.error("Error loading tasks:", error);
        }
    }

    loadTasks();
});
