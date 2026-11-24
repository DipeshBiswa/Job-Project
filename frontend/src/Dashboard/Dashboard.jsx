
import { useNavigate, Link } from "react-router-dom";
import { logoutUser } from "../api/authencationApi";
import { getCurrentUser } from "../api/depedencyApi";
import { getProfile } from "../api/profileApi";

import { useEffect, useState } from "react";
import ProfileSetupModal from "./ProfileSetupModal";

export default function Dashboard() {
    const navigate = useNavigate();

    const [user, setUser] = useState(null);
    const [profileStatus, setProfileStatus] = useState("loading");
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {
        let active = true;

        async function loadDashboard() {
            try {
                const currentUser = await getCurrentUser();

                if (!active) return;

                setUser(currentUser);

                try {
                    await getProfile();

                    if (active) {
                        setProfileStatus("exists");
                    }

                } catch (error) {
                    if (!active) return;

                    if (error.status === 404) {
                        setProfileStatus("missing");
                        setShowModal(true);
                    } else if (error.status === 401) {
                        navigate("/login", { replace: true });
                    } else {
                        setProfileStatus("error");
                    }
                }

            } catch (error) {
                if (active) {
                    console.error(error.message);
                    navigate("/login", { replace: true });
                }
            }
        }

        loadDashboard();

        return () => {
            active = false;
        };
    }, [navigate]);

    async function logout() {
        try {
            await logoutUser();
            navigate("/login", { replace: true });
        } catch (error) {
            console.error("Logout failed:", error);
        }
    }

    return (
        <div>
            <h1>User Dashboard</h1>

            {user && <h2>Welcome, {user.firstName}!</h2>}

            {profileStatus === "loading" && (
                <p>Checking your profile...</p>
            )}

            {profileStatus === "exists" && (
                <>
                    <p>Your profile has been created.</p>
                    <Link to="/profile">My Profile</Link>
                </>
            )}

            {profileStatus === "missing" && (
                <>
                    <p>You haven't created a profile yet.</p>
                    <Link to="/profile/setup">Create Profile</Link>
                </>
            )}

            {profileStatus === "error" && (
                <p>Unable to load your profile. Please refresh.</p>
            )}

            <button onClick={logout}>
                Logout
            </button>

            {showModal && (
                <ProfileSetupModal
                    onClose={() => setShowModal(false)}
                    onStart={() => navigate("/profile/setup")}
                />
            )}
        </div>
    );
}
;