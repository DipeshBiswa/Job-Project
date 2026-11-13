


/**
 * dashboard component serves as the main interface for authenticated users.
 * @returns 
 */

import { Link, Navigate } from "react-router-dom";
import { loginUser } from "../api/authencationApi";

export default function Dashboard(){

    async function logout(){

        try{
            await loginUser();
            Navigate("/login", {replace : true});
        }catch(error){
            console.error("Logout failed:", error);
        }

    }

    return(
        <div>
            <h1>User Dashboard</h1>

            
            <button onClick={loginUser}>
                
            </button>
        </div>
    );

}