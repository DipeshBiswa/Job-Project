import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { createBrowserRouter, RouterProvider} from "react-router-dom"
import Register from './Authencation/Register.jsx'
import Authencation from './Authencation/Authentication.jsx'

const router = createBrowserRouter([
  {path: "/register", element: <Register/>},
  {path: "/login" , element: <Authencation />},
  {path: "/", element: <App />}
  

])

createRoot(document.getElementById('root')).render(
  <StrictMode>
   <RouterProvider router={router} />
  </StrictMode>
);
