
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getProfile } from "../api/profileApi";

export default function Profile() {
    const navigate = useNavigate();

    const [profile, setProfile] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        let active = true;

        async function loadProfile() {
            try {
                const data = await getProfile();

                if (active) {
                    setProfile(data);
                }

            } catch (error) {
                if (!active) return;

                if (error.status === 404) {
                    navigate("/profile/setup", { replace: true });
                } else if (error.status === 401) {
                    navigate("/login", { replace: true });
                } else {
                    setError(error.message);
                }
            }
        }

        loadProfile();

        return () => {
            active = false;
        };
    }, [navigate]);

    if (error) {
        return <p role="alert">{error}</p>;
    }

    if (!profile) {
        return <p>Loading profile...</p>;
    }

    return (
        <div>
            <h1>My Profile</h1>

            <pre>
                {JSON.stringify(profile, null, 2)}
            </pre>

            <button onClick={() => navigate("/dashboard")}>
                Back to Dashboard
            </button>
        </div>
    );
}
