
import Authencation from "./Authencation/Authentication.jsx";
import { Link } from "react-router-dom";


function App() {
  

  return (
   <div>
    <div>

      <Link to={"/register"}>
        <button>
          Register
        </button>
      </Link>

      <div>

      <Link to={"/login"}>
        <button>
          Login
        </button>
      </Link>
      
      </div>
    </div>

   </div>
  );
}

export default App
