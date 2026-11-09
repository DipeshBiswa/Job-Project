
import { registerUser } from "../api/authencationApi";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
/**
 * Register component handles user registration functionality.
 *  It provides a form for users to enter their first name, last name, email, and password, and upon submission,
 *  it attempts to register the user using the registerUser API function. If successful, it navigates the user to the login page; if not, it displays an error message.
 * @returns 
 */
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
        <div className="register">
            <form onSubmit={makeUser}>
                <label htmlFor="email">Email</label>
                <input type="email" id="email" name="email" autoComplete="email" onChange={(e) => setEmail(e.target.value)} required />

                <label htmlFor="firstname"> First Name</label>
                <input type="text" id="firstname" autoComplete="given-name" onChange={(e) => setFirst(e.target.value)} required />

                <label htmlFor="lastname"> Last Name</label>
                <input type="text" id="lastname" autoComplete="family-name" onChange={(e) => setLast(e.target.value)} required />

                <label htmlFor="password"> Password</label>
                <input type="password" id="password" autoComplete="new-password" minLength={8} onChange={(e) => setPassword(e.target.value)} required />


                <button type="submit"> Register </button>
                
                {error && <p>{error}</p>}

            </form>
            <div>
                <h5>Already have an account? 
                    <Link to={"/login"}>login</Link>
                </h5>
            </div>
            </div>
    )    
}