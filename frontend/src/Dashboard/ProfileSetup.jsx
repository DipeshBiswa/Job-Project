
import { useState, useRef } from "react";
import { useNavigate, Link } from "react-router-dom";
import { createProfile } from "../api/profileApi";

const blankEducation = (id) => ({
    id,
    university: "",
    degree: "",
    major: "",
    gpa: "",
    startDate: "",
    graduationDate: ""
});

const blankWorkExperience = (id) => ({
    id,
    company: "",
    jobTitle: "",
    location: "",
    startDate: "",
    endDate: "",
    currentlyWorking: false,
    description: ""
});

export default function ProfileSetup() {
    const navigate = useNavigate();
    const nextId = useRef(3);

    const [form, setForm] = useState({
        preferredName: "",
        phoneNumber: "",
        applicationEmail: "",
        street: "",
        apartment: "",
        city: "",
        state: "",
        zipCode: "",
        country: "",
        skills: "",
        linkedin: "",
        github: "",
        portfolio: "",
        authorizedToWork: "",
        requiresSponsorship: "",
        willingToRelocate: ""
    });

    const [educations, setEducations] = useState([
        blankEducation(1)
    ]);

    const [workExperiences, setWorkExperiences] = useState([
        blankWorkExperience(2)
    ]);

    const [error, setError] = useState("");
    const [saving, setSaving] = useState(false);

    // General profile fields
    function handleChange(e) {
        const { name, value } = e.target;

        setForm(previous => ({
            ...previous,
            [name]: value
        }));
    }

    // Education functions
    function addEducation() {
        const id = nextId.current++;
        setEducations(previous => [
            ...previous,
            blankEducation(id)
        ]);
    }

    function removeEducation(id) {
        setEducations(previous =>
            previous.filter(education => education.id !== id)
        );
    }

    function updateEducation(id, field, value) {
        setEducations(previous =>
            previous.map(education =>
                education.id === id
                    ? { ...education, [field]: value }
                    : education
            )
        );
    }

    // Work experience functions
    function addWorkExperience() {
        const id = nextId.current++;
        setWorkExperiences(previous => [
            ...previous,
            blankWorkExperience(id)
        ]);
    }

    function removeWorkExperience(id) {
        setWorkExperiences(previous =>
            previous.filter(work => work.id !== id)
        );
    }

    function updateWorkExperience(id, field, value) {
        setWorkExperiences(previous =>
            previous.map(work =>
                work.id === id
                    ? { ...work, [field]: value }
                    : work
            )
        );
    }

    function toBoolean(value) {
        if (value === "") return null;
        return value === "true";
    }

    // Submit profile to backend
    async function handleSubmit(e) {
        e.preventDefault();
        setError("");

        // Ignore completely empty education entries
        const filledEducations = educations.filter(education =>
            education.university.trim() ||
            education.degree.trim() ||
            education.major.trim() ||
            education.gpa !== "" ||
            education.startDate ||
            education.graduationDate
        );

        // Validate education entries
        for (const education of filledEducations) {
            if (
                !education.university.trim() ||
                !education.degree.trim() ||
                !education.major.trim()
            ) {
                setError(
                    "Each education entry needs a university, degree, and major."
                );
                return;
            }
        }

        // Ignore completely empty work entries
        const filledWorkExperiences = workExperiences.filter(work =>
            work.company.trim() ||
            work.jobTitle.trim() ||
            work.location.trim() ||
            work.startDate ||
            work.endDate ||
            work.currentlyWorking ||
            work.description.trim()
        );

        // Validate work entries
        for (const work of filledWorkExperiences) {
            if (!work.company.trim() || !work.jobTitle.trim()) {
                setError(
                    "Each work experience needs a company and job title."
                );
                return;
            }
        }

        // Convert React form state into the backend schema
        const profile = {
            contactInformation: {
                preferredName: form.preferredName,
                phoneNumber: form.phoneNumber,
                applicationEmail: form.applicationEmail || null
            },

            address: {
                street: form.street,
                apartment: form.apartment,
                city: form.city,
                state: form.state,
                zipCode: form.zipCode,
                country: form.country
            },

            education: filledEducations.map(education => ({
                university: education.university,
                degree: education.degree,
                major: education.major,
                gpa: education.gpa === ""
                    ? null
                    : Number(education.gpa),
                startDate: education.startDate || null,
                graduationDate: education.graduationDate || null
            })),

            workExperience: filledWorkExperiences.map(work => ({
                company: work.company,
                jobTitle: work.jobTitle,
                location: work.location || null,
                startDate: work.startDate || null,
                endDate: work.currentlyWorking
                    ? null
                    : work.endDate || null,
                currentlyWorking: work.currentlyWorking,
                description: work.description || null
            })),

            skills: form.skills
                .split(",")
                .map(skill => skill.trim())
                .filter(Boolean),

            professionalLinks: {
                linkedin: form.linkedin,
                github: form.github,
                portfolio: form.portfolio
            },

            workEligibility: {
                authorizedToWork: toBoolean(form.authorizedToWork),
                requiresSponsorship: toBoolean(form.requiresSponsorship),
                willingToRelocate: toBoolean(form.willingToRelocate)
            }
        };

        setSaving(true);

        try {
            await createProfile(profile);
            navigate("/dashboard", { replace: true });
        } catch (error) {
            setError(error.message);
        } finally {
            setSaving(false);
        }
    }

    // Reusable input for general profile fields
    function input(label, name, type = "text") {
        return (
            <div key={name}>
                <label htmlFor={name}>{label}</label>
                <input
                    id={name}
                    name={name}
                    type={type}
                    value={form[name]}
                    onChange={handleChange}
                />
            </div>
        );
    }

    // Reusable input for education and work entries
    function entryInput(
        group, item, label, name, update, type = "text"
    ) {
        const inputId = `${group}-${item.id}-${name}`;

        return (
            <div key={name}>
                <label htmlFor={inputId}>{label}</label>
                <input
                    id={inputId}
                    type={type}
                    step={type === "number" ? "0.01" : undefined}
                    value={item[name]}
                    onChange={e =>
                        update(item.id, name, e.target.value)
                    }
                />
            </div>
        );
    }

    function yesNoInput(label, name) {
        return (
            <div key={name}>
                <label htmlFor={name}>{label}</label>
                <select
                    id={name}
                    name={name}
                    value={form[name]}
                    onChange={handleChange}
                >
                    <option value="">Not answered</option>
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
        );
    }

    return (
        <div>
            <Link to="/dashboard">
                ← Back to Dashboard
            </Link>

            <h1>Create Your Profile</h1>

            <form onSubmit={handleSubmit}>

                <h2>Contact Information</h2>
                {input("Preferred Name", "preferredName")}
                {input("Phone Number", "phoneNumber", "tel")}
                {input("Application Email", "applicationEmail", "email")}

                <h2>Address</h2>
                {input("Street Address", "street")}
                {input("Apartment", "apartment")}
                {input("City", "city")}
                {input("State", "state")}
                {input("ZIP Code", "zipCode")}
                {input("Country", "country")}

                <h2>Education</h2>

                {educations.map((education, index) => (
                    <fieldset key={education.id}>
                        <legend>Education {index + 1}</legend>

                        {entryInput(
                            "education", education,
                            "University", "university",
                            updateEducation
                        )}

                        {entryInput(
                            "education", education,
                            "Degree", "degree",
                            updateEducation
                        )}

                        {entryInput(
                            "education", education,
                            "Major", "major",
                            updateEducation
                        )}

                        {entryInput(
                            "education", education,
                            "GPA", "gpa",
                            updateEducation, "number"
                        )}

                        {entryInput(
                            "education", education,
                            "Start Date", "startDate",
                            updateEducation, "month"
                        )}

                        {entryInput(
                            "education", education,
                            "Graduation Date", "graduationDate",
                            updateEducation, "month"
                        )}

                        <button
                            type="button"
                            onClick={() =>
                                removeEducation(education.id)
                            }
                        >
                            Remove Education
                        </button>
                    </fieldset>
                ))}

                <button
                    type="button"
                    onClick={addEducation}
                >
                    + Add Education
                </button>

                <h2>Work Experience</h2>

                {workExperiences.map((work, index) => (
                    <fieldset key={work.id}>
                        <legend>Work Experience {index + 1}</legend>

                        {entryInput(
                            "work", work,
                            "Company", "company",
                            updateWorkExperience
                        )}

                        {entryInput(
                            "work", work,
                            "Job Title", "jobTitle",
                            updateWorkExperience
                        )}

                        {entryInput(
                            "work", work,
                            "Location", "location",
                            updateWorkExperience
                        )}

                        {entryInput(
                            "work", work,
                            "Start Date", "startDate",
                            updateWorkExperience, "month"
                        )}

                        <div>
                            <label>
                                <input
                                    type="checkbox"
                                    checked={work.currentlyWorking}
                                    onChange={e =>
                                        updateWorkExperience(
                                            work.id,
                                            "currentlyWorking",
                                            e.target.checked
                                        )
                                    }
                                />
                                I currently work here
                            </label>
                        </div>

                        {!work.currentlyWorking && entryInput(
                            "work", work,
                            "End Date", "endDate",
                            updateWorkExperience, "month"
                        )}

                        <div>
                            <label htmlFor={`description-${work.id}`}>
                                Description
                            </label>
                            <textarea
                                id={`description-${work.id}`}
                                value={work.description}
                                onChange={e =>
                                    updateWorkExperience(
                                        work.id,
                                        "description",
                                        e.target.value
                                    )
                                }
                            />
                        </div>

                        <button
                            type="button"
                            onClick={() =>
                                removeWorkExperience(work.id)
                            }
                        >
                            Remove Work Experience
                        </button>
                    </fieldset>
                ))}

                <button
                    type="button"
                    onClick={addWorkExperience}
                >
                    + Add Work Experience
                </button>

                <h2>Skills</h2>
                {input("Skills (comma-separated)", "skills")}

                <h2>Professional Links</h2>
                {input("LinkedIn", "linkedin", "url")}
                {input("GitHub", "github", "url")}
                {input("Portfolio", "portfolio", "url")}

                <h2>Work Eligibility</h2>
                {yesNoInput(
                    "Authorized to Work", "authorizedToWork"
                )}
                {yesNoInput(
                    "Requires Sponsorship", "requiresSponsorship"
                )}
                {yesNoInput(
                    "Willing to Relocate", "willingToRelocate"
                )}

                {error && <p role="alert">{error}</p>}

                <button type="submit" disabled={saving}>
                    {saving ? "Saving..." : "Save Profile"}
                </button>

            </form>
        </div>
    );
}
