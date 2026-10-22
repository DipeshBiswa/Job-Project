

function Authencation(){

    return(
        <div>
            <form method="POST">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" autoComplete="email" required />

                <label for="firstname"> First Name</label>
                <input type="firstname" id="firstname" autoComplete="firstname" required />

                <label for="lastname"> Last Name</label>
                <input type="lastname" id="lastname" autoComplete="lastname" required />

                <label for="password"> Password</label>
                <input type="password" id="password" autoComplete="password" required />


                <button type="submit"> Register</button>


            </form>
        </div>
    )



}

export default Authencation