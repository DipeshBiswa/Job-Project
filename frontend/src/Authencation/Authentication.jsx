import { useState } from "react"
import { registerUser } from "../api/authencationApi";
import './authentication.css'


function Authencation(){
    
    const [firstName, setFirst] = useState("");
    const [lastName, setLast] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    
    const user = {
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password
    }
    async function makeUser(e){
        e.preventDefault();
        try{
            await registerUser(user);
        }catch(error){
            console.error("Failed to create user", error)
        }
    }
    return(
        <div>
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


            </form>

            <div>
                <form>
                    <label htmlFor="email"> Email</label>
                    <input type="email" id="email" name="email" autoComplete="email" required />

                    <label htmlFor="password"> password</label>
                    <input type="password" id="password" autoComplete="login-password" required />

                    <button type="submit"> Login </button>

                </form>
            </div>
            </div>
        </div>
    )
}

export default Authencation
