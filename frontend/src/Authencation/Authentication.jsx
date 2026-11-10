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
        <div className="auth-page">
            <Link to={"/"} className="site-logo">Prefill</Link>
            <div className="auth-card">
                <h1 className="auth-title">Log in</h1>

                <form onSubmit={login} className="auth-form">
                    <label htmlFor="email">Email</label>
                    <input type="email" id="email" name="email" autoComplete="email" required onChange={(e) => setEmail(e.target.value)}/>

                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" autoComplete="current-password" required onChange={(e) => setPassword(e.target.value)} />

                    <button type="submit" className="btn btn-primary">Log in</button>

                    {error && <p className="auth-error">{error}</p>}

                </form>

                <p className="auth-footer">Don't have an account?{" "}
                    <Link to={"/register"}>Sign up</Link>
                </p>
            </div>
        </div>
    )
}

export default Authencation
