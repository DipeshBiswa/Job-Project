import { useState } from "react"
import './authentication.css'


function Authencation(){
    
    return(
        <div>

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
    )
}

export default Authencation
