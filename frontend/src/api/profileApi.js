
const URL = "/profiles";

export async function getProfile(){
    const response = await fetch (`${URL}/me`, {
        method: "GET",
        credentials: "include"
    });
    if (!response.ok){
        const error = new Error("Failed to retrive profile");
        error.status = response.status;
        throw error;
    }
    return response.json();
}

export async function createProfile(profile){
    const response = await fetch(`${URL}/me`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify(profile)
    });
    if(!response.ok){
        const errorData = await response.json().catch( () => null);

        const error = new Error(
            typeof errorData?.detail === "string" ? errorData.detail : "Failed to create profile"
        );
        error.status = response.status;
        throw error;
    }
    return response.json();
}