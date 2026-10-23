
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
        const detail = Array.isArray(error.detail)
            ? error.detail.map((issue) => `${issue.loc.join(".")}: ${issue.msg}`).join("; ")
            : error.detail;
        throw new Error(detail || "Failed to create user");
    }
    return response.json();
}
