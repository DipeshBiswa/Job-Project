


/**
 * dashboard component serves as the main interface for authenticated users.
 * @returns 
 */

import { useNavigate } from "react-router-dom";
import { logoutUser } from "../api/authencationApi";
import { getCurrentUser } from "../api/depedencyApi";
import { useEffect } from "react";

export default function Dashboard(){
    const navigate = useNavigate();

    const [user, setUser] = useState(null);

    useEffect( () =>{
        async function fetchUser(){
            try{
                const currentUser = await getCurrentUser();
                setUser(currentUser);
            }catch(error){
                console.error(error.message);
            }
        }
        fetchUser();
    }, []);

    async function logout(){

        try{
            await logoutUser();
            navigate("/login", {replace : true});
        }catch(error){
            console.error("Logout failed:", error);
        }

    }

    return(
        <div>
            <h1>User Dashboard</h1>
            {user && <h1>Welcome, {user.firstName}!</h1>}
            
            <button onClick={logout}>
                Logout
            </button>
        </div>
    );

}
