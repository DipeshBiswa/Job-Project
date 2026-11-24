
export default function ProfileSetupModal({ onClose, onStart }) {
    return (
        <div role="dialog" aria-modal="true" aria-labelledby="profile-setup-title">
            <h2 id="profile-setup-title">Welcome to Prefill!</h2>

            <p>
                You haven't created your profile yet.
                Create a profile to save your information
                and use it for future job applications.
            </p>

            <button onClick={onStart}>
                Create Profile
            </button>

            <button onClick={onClose}>
                Maybe Later
            </button>
        </div>
    );
}
