import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getProfile } from "../api/profileApi";

function display(value) {
    return value === null || value === undefined || value === "" ? "Not provided" : value;
}

function month(value) {
    if (!value) return "Not provided";
    const match = /^(\d{4})-(\d{2})(?:-\d{2})?$/.exec(value);
    if (!match || Number(match[2]) < 1 || Number(match[2]) > 12) return value;
    return new Intl.DateTimeFormat("en-US", { month: "short", year: "numeric", timeZone: "UTC" })
        .format(new Date(`${match[1]}-${match[2]}-01T00:00:00Z`));
}

function Details({ items }) {
    return <dl>{items.map(([label, value]) => (
        <div key={label}><dt>{label}</dt><dd>{display(value)}</dd></div>
    ))}</dl>;
}

function Section({ id, title, children }) {
    return <section id={id} aria-labelledby={`${id}-heading`}>
        <h2 id={`${id}-heading`}>{title}</h2>{children}
    </section>;
}

function ProfessionalLink({ label, value }) {
    let url;
    if (value) {
        try {
            const candidate = new URL(/^[a-z][a-z\d+.-]*:/i.test(value) ? value : `https://${value}`);
            if (["http:", "https:"].includes(candidate.protocol)) url = candidate.href;
        } catch { /* Keep malformed saved links readable without making them clickable. */ }
    }
    return <div><dt>{label}</dt><dd>{url
        ? <a href={url} target="_blank" rel="noopener noreferrer">{value} (opens in a new tab)</a>
        : display(value)}</dd></div>;
}

export default function Profile() {
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        let active = true;
        async function loadProfile() {
            try {
                const data = await getProfile();
                if (active) setProfile(data);
            } catch (error) {
                if (!active) return;
                if (error.status === 404) navigate("/profile/setup", { replace: true });
                else if (error.status === 401) navigate("/login", { replace: true });
                else setError(error.message);
            }
        }
        loadProfile();
        return () => { active = false; };
    }, [navigate]);

    if (error || !profile) return (
        <main>
            <Link to="/dashboard">Back to dashboard</Link>
            <div>
                <h1>My profile</h1>
                {error ? <p role="alert">{error}</p> : <p role="status">Loading your profile…</p>}
            </div>
        </main>
    );

    const contact = profile.contactInformation ?? {};
    const address = profile.address ?? {};
    const eligibility = profile.workEligibility ?? {};
    const education = profile.education ?? [];
    const experience = profile.workExperience ?? [];
    const skills = profile.skills ?? [];
    const links = profile.professionalLinks ?? {};
    const yesNo = value => value === true ? "Yes" : value === false ? "No" : "Not answered";

    return (
        <main>
            <h1>My Profile</h1>
            <Link to="/profile/edit">Edit Profile</Link>
            <Section id="contact" title="Contact information">
                <Details items={[["Preferred name", contact.preferredName], ["Phone number", contact.phoneNumber], ["Application email", contact.applicationEmail]]} />
            </Section>
            <Section id="address" title="Address">
                <Details items={[["Street address", address.street], ["Apartment / unit", address.apartment], ["City", address.city], ["State / province", address.state], ["ZIP / postal code", address.zipCode], ["Country", address.country]]} />
            </Section>
            <Section id="education" title="Education">
                {education.length ? education.map((item, index) => <article key={index}>
                    <h3>{display(item.university)}</h3>
                    <Details items={[["Degree", item.degree], ["Major", item.major], ["GPA", item.gpa], ["Start date", month(item.startDate)], ["Graduation date", month(item.graduationDate)]]} />
                </article>) : <p>No education added yet.</p>}
            </Section>
            <Section id="experience" title="Work experience">
                {experience.length ? experience.map((item, index) => <article key={index}>
                    <h3>{display(item.jobTitle)}</h3>
                    <Details items={[["Company", item.company], ["Location", item.location], ["Start date", month(item.startDate)], ["End date", item.currentlyWorking ? "Present" : month(item.endDate)], ["Currently working here", yesNo(item.currentlyWorking)]]} />
                    <dl><dt>Description</dt><dd>{display(item.description)}</dd></dl>
                </article>) : <p>No work experience added yet.</p>}
            </Section>
            <Section id="skills" title="Skills">
                {skills.length ? <ul>{skills.map((skill, index) => <li key={index}>{skill}</li>)}</ul> : <p>No skills added yet.</p>}
            </Section>
            <Section id="links" title="Professional links">
                <dl>{[["LinkedIn", links.linkedin], ["GitHub", links.github], ["Portfolio", links.portfolio]].map(([label, value]) => <ProfessionalLink key={label} label={label} value={value} />)}</dl>
            </Section>
            <Section id="eligibility" title="Work eligibility">
                <Details items={[["Authorized to work", yesNo(eligibility.authorizedToWork)], ["Requires sponsorship", yesNo(eligibility.requiresSponsorship)], ["Willing to relocate", yesNo(eligibility.willingToRelocate)]]} />
            </Section>
            <Link to="/dashboard">Back to Dashboard</Link>
        </main>
    );
}
