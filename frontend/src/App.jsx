
import Authencation from "./Authencation/Authentication.jsx";
import { Link } from "react-router-dom";
import "./App.css";


function App() {
  

  return (
   <div className="landing">
    <div>
      <h1 className="landing-title">Prefill</h1>
      <p className="landing-subtitle">Save your profile once and autofill your job applications.</p>

      <div className="landing-actions">
        <Link to={"/register"} className="btn btn-primary">
          Sign up
        </Link>

        <Link to={"/login"} className="btn btn-outline">
          Log in
        </Link>
      </div>
    </div>

   </div>
  );
}

export default App
