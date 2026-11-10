
import { registerUser } from "../api/authencationApi";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./authentication.css";

export default function Register(){

    const navigate = useNavigate();

    const [firstName, setFirst] = useState("");
    const [lastName, setLast] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
        
    const user = {
            firstName: firstName,
            lastName: lastName,
            email: email,
            password: password
        }
    async function makeUser(e){
            e.preventDefault();
            setError("");
            try{
                const response = await registerUser(user);
                navigate("/login");

            }catch(error){
                setError(error.message);
            }
    }
//cimments aded for this function

    return(
        <div className="auth-page">
            <Link to={"/"} className="site-logo">Prefill</Link>
            <div className="auth-card">
                <h1 className="auth-title">Sign up</h1>

                <form onSubmit={makeUser} className="auth-form">
                    <label htmlFor="firstname">First name</label>
                    <input type="text" id="firstname" autoComplete="given-name" onChange={(e) => setFirst(e.target.value)} required />

                    <label htmlFor="lastname">Last name</label>
                    <input type="text" id="lastname" autoComplete="family-name" onChange={(e) => setLast(e.target.value)} required />

                    <label htmlFor="email">Email</label>
                    <input type="email" id="email" name="email" autoComplete="email" onChange={(e) => setEmail(e.target.value)} required />

                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" autoComplete="new-password" minLength={8} onChange={(e) => setPassword(e.target.value)} required />

                    <button type="submit" className="btn btn-primary">Sign up</button>

                    {error && <p className="auth-error">{error}</p>}

                </form>

                <p className="auth-footer">Already have an account?{" "}
                    <Link to={"/login"}>Log in</Link>
                </p>
            </div>
        </div>
    )    
}