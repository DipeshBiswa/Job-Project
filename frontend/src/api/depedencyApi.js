
const URL = "/users"

export async function getCurrentUser(){
    const response = await fetch(`${URL}/me`, {
        method: "GET",
        credentials: "include"
    });

    if(!response.ok){
        throw new Error("Failed to retrive current user");
    }

    return response.json();
}
