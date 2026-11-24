import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { createBrowserRouter, RouterProvider} from "react-router-dom"
import Register from './Authencation/Register.jsx'
import Authencation from './Authencation/Authentication.jsx'
import Dashboard from './Dashboard/Dashboard.jsx'
import ProtectedRoute from './routes/ProtectedRoute.jsx'
import ProfileSetup from './Dashboard/ProfileSetup.jsx'
import Profile from './Profile/Profile.jsx'

const router = createBrowserRouter([
  {path: "/register", element: <Register/>},
  {path: "/login" , element: <Authencation />},
  {path: "/", element: <App />},
  {
    element: <ProtectedRoute />,
    children: [
      {
        path: "/dashboard",
        element: <Dashboard />
      },
      {
        path: "/profile/setup",
        element: <ProfileSetup />
      },
      {
        path: "/profile",
        element: <Profile />
      }

    ]
  }
  
  

])

createRoot(document.getElementById('root')).render(
  <StrictMode>
   <RouterProvider router={router} />
  </StrictMode>
);
