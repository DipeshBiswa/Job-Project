
const URL  = "http://127.0.0.1:8000/users"

export async function registerUser(user){
    const response = await fetch(`${URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(user)
    });
    if(!response.ok){
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Failed to create user");
    }
    return response.json();
}