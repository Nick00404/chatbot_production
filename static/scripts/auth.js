document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("loginUsername").value;
            const password = document.getElementById("loginPassword").value;

            try {
                const response = await fetch("/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();
                if (data.success) {
                    window.location.href = "/"; // Redirect to chat UI
                } else {
                    alert("Login failed: " + data.message);
                }
            } catch (error) {
                console.error("Login error:", error);
                alert("Error logging in.");
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("registerUsername").value;
            const password = document.getElementById("registerPassword").value;

            try {
                const response = await fetch("/register", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();
                if (data.success) {
                    alert("Registration successful! You can now log in.");
                    window.location.href = "/login";
                } else {
                    alert("Registration failed: " + data.message);
                }
            } catch (error) {
                console.error("Register error:", error);
                alert("Error registering user.");
            }
        });
    }
});
