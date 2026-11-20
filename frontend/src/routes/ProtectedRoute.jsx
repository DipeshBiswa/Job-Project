
import { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { getCurrentUser } from "../api/depedencyApi";


function ProtectedRoute(){
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(()=>{
        async function checkAuthentication(){
            try{
                await getCurrentUser();
                setIsAuthenticated(true);
            }catch(error){
                setIsAuthenticated(false);
            }finally{
                setLoading(false);
            }
        }
        checkAuthentication();
    }, []);
    if(loading){
        return <p>Loading...</p>
    }
    if (!isAuthenticated){
        return <Navigate to="/login" replace />

    }
    return <Outlet />;
}

export default ProtectedRoute;