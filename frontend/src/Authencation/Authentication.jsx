import { useState } from "react"
import './authentication.css'

import { loginUser } from "../api/authencationApi";


function Authencation(){

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const user ={
        email:email,
        password : password
    }

    async function login(e){
        e.preventDefault();

        try{
            const token = loginUser(user);
        }catch(error){
            console.error("Error: ", token);

        }

    }


    
    return(
        <div>

            <div>
                <form>
                    <label htmlFor="email"> Email</label>
                    <input type="email" id="email" name="email" autoComplete="email" required onChange={(e) => setEmail(e.target.value)}/>

                    <label htmlFor="password"> password</label>
                    <input type="password" id="password" autoComplete="login-password" required onChange={(e) => setPassword(e.target.value)} />

                    <button type="submit"> Login </button>

                </form>
            </div>
            
        </div>
    )
}

export default Authencation
