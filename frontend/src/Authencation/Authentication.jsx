import { useState } from "react"
import './authentication.css'

import { loginUser } from "../api/authencationApi";
import { Link, useNavigate } from "react-router-dom";


function Authencation(){

    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("")

    const user ={
        email:email,
        password : password
    }

    async function login(e){
        e.preventDefault();
        setError("");
        try{
            const token = await loginUser(user);
            navigate("/dashboard")
        }catch(error){
            setError(error.message);

        }

    }


    
    return(
        <div>

            <div>
                <form onSubmit={login}>
                    <label htmlFor="email"> Email</label>
                    <input type="email" id="email" name="email" autoComplete="email" required onChange={(e) => setEmail(e.target.value)}/>

                    <label htmlFor="password"> password</label>
                    <input type="password" id="password" autoComplete="current-password" required onChange={(e) => setPassword(e.target.value)} />

                    <button type="submit"> Login </button>

                    {error && <p>{error}</p>}

                </form>
            </div>

            <div>
                <h5>Need a account? 
                    <Link to={"/register"}>register</Link>
                </h5>
            </div>
            
        </div>
    )
}

export default Authencation
