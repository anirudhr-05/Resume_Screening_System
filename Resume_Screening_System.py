from abc import ABC, abstractmethod


# 1. CANDIDATE CLASS - ENCAPSULATION
class Candidate:
    def __init__(self, name, skills, qualification):
        self.__name = name
        self.__skills = skills
        self.__qualification = qualification

    def get_name(self):
        return self.__name

    def get_skills(self):
        return self.__skills

    def get_qualification(self):
        return self.__qualification

    # This method is overridden by the child classes.
    def check_experience(self, required_experience):
        return False

    def display_details(self):
        print("\n===== CANDIDATE DETAILS =====")
        print("Name:", self.__name)
        print("Skills:", ", ".join(self.__skills))
        print("Qualification:", self.__qualification)


# 2. INHERITANCE - FRESHER CANDIDATE
class FresherCandidate(Candidate):
    def __init__(self, name, skills, qualification):
        super().__init__(name, skills, qualification)

    # 3. POLYMORPHISM - fresher-specific experience check
    def check_experience(self, required_experience):
        return required_experience == 0


# 2. INHERITANCE - EXPERIENCED CANDIDATE
class ExperiencedCandidate(Candidate):
    def __init__(self, name, skills, qualification, experience):
        super().__init__(name, skills, qualification)

        if experience < 0:
            raise ValueError("Experience cannot be negative.")

        self.__experience = experience

    def get_experience(self):
        return self.__experience

    # 3. POLYMORPHISM - experienced-candidate check
    def check_experience(self, required_experience):
        return self.__experience >= required_experience

    def display_details(self):
        super().display_details()
        print("Experience:", self.__experience, "years")


# 4. JOB CLASS
class Job:
    def __init__(self, job_title, required_skills,
                 required_experience=0, required_qualification="Any"):
        self.job_title = job_title
        self.required_skills = required_skills
        self.required_experience = required_experience
        self.required_qualification = required_qualification

    def display_requirements(self):
        print("\nJob:", self.job_title)
        print("Required Skills:", ", ".join(self.required_skills))
        print("Required Experience:", self.required_experience, "years")
        print("Required Qualification:", self.required_qualification)


# 5. ABSTRACTION
class ScreeningProcess(ABC):
    @abstractmethod
    def screen_candidate(self, candidate, job):
        pass


# 6. RESUME SCREENING CLASS
class ResumeScreening(ScreeningProcess):
    def __init__(self, minimum_match=70):
        self.minimum_match = minimum_match

    def calculate_skill_match(self, candidate, job):
        # Case-insensitive exact matching; extra spaces are ignored.
        candidate_skills = {
            skill.strip().casefold()
            for skill in candidate.get_skills()
        }

        matched_skills = []

        for required_skill in job.required_skills:
            if required_skill.strip().casefold() in candidate_skills:
                matched_skills.append(required_skill)

        if not job.required_skills:
            return 0.0, matched_skills

        percentage = (
            len(matched_skills) / len(job.required_skills)
        ) * 100

        return percentage, matched_skills

    def check_qualification(self, candidate, job):
        required = job.required_qualification.strip().casefold()
        actual = candidate.get_qualification().strip().casefold()

        return required == "any" or required == actual

    # Implements the abstract method.
    def screen_candidate(self, candidate, job):
        percentage, matched_skills = self.calculate_skill_match(
            candidate, job
        )

        experience_eligible = candidate.check_experience(
            job.required_experience
        )

        qualification_eligible = self.check_qualification(
            candidate, job
        )

        shortlisted = (
            percentage >= self.minimum_match
            and experience_eligible
            and qualification_eligible
        )

        return {
            "job": job,
            "matched_skills": matched_skills,
            "percentage": percentage,
            "experience_eligible": experience_eligible,
            "qualification_eligible": qualification_eligible,
            "shortlisted": shortlisted
        }

    def display_result(self, candidate, result):
        job = result["job"]

        print("\n----------------------------------------")
        print("Job:", job.job_title)
        print(
            "Matched Skills:",
            ", ".join(result["matched_skills"])
            if result["matched_skills"] else "None"
        )
        print("Skill Match:", round(result["percentage"], 2), "%")
        print(
            "Experience Eligibility:",
            "Eligible" if result["experience_eligible"]
            else "Not Eligible"
        )
        print(
            "Qualification Eligibility:",
            "Eligible" if result["qualification_eligible"]
            else "Not Eligible"
        )
        print(
            "Screening Status:",
            "SHORTLISTED" if result["shortlisted"] else "REJECTED"
        )


# 7. MAIN PROGRAM
def main():
    try:
        print("========== RESUME SCREENING SYSTEM ==========")

        name = input("Enter candidate name: ").strip()
        if not name:
            raise ValueError("Candidate name cannot be empty.")

        skills_input = input(
            "Enter skills (comma separated): "
        ).strip()

        skills = [
            skill.strip()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        if not skills:
            raise ValueError("Please enter at least one skill.")

        qualification = input(
            "Enter qualification: "
        ).strip()

        if not qualification:
            raise ValueError("Qualification cannot be empty.")

        print("\nSelect Candidate Type")
        print("1. Fresher")
        print("2. Experienced")

        candidate_type = input("Enter your choice (1 or 2): ").strip()

        if candidate_type == "1":
            candidate = FresherCandidate(
                name, skills, qualification
            )

        elif candidate_type == "2":
            experience = float(
                input("Enter experience in years: ")
            )

            if experience < 0:
                raise ValueError("Experience cannot be negative.")

            candidate = ExperiencedCandidate(
                name, skills, qualification, experience
            )

        else:
            raise ValueError("Please enter 1 or 2.")

        # Available jobs and their requirements.
        jobs = [
            Job(
                "Python Developer",
                ["Python", "OOP", "SQL", "Django"],
                0,
                "Any"
            ),
            Job(
                "Data Analyst",
                ["Python", "SQL", "Excel", "Power BI"],
                1,
                "Any"
            ),
            Job(
                "GenAI Developer",
                ["Python", "LLM", "RAG", "LangChain"],
                0,
                "Any"
            ),
            Job(
                "Embedded Tester",
                ["CAN", "CAPL", "CANoe", "UDS"],
                2,
                "Any"
            )
        ]

        candidate.display_details()

        print("\n===== AVAILABLE JOB REQUIREMENTS =====")
        for job in jobs:
            job.display_requirements()

        screening = ResumeScreening(minimum_match=70)

        # Screen the candidate against every available job.
        results = []

        for job in jobs:
            result = screening.screen_candidate(candidate, job)
            results.append(result)

        # Sort jobs by skill percentage, highest match first.
        # If percentages are equal, the number of matched skills
        # is used as the next sorting condition.
        results.sort(
            key=lambda result: (
                result["percentage"],
                len(result["matched_skills"])
            ),
            reverse=True
        )

        # Separate shortlisted and rejected jobs.
        shortlisted_jobs = [
            result for result in results
            if result["shortlisted"]
        ]

        rejected_jobs = [
            result for result in results
            if not result["shortlisted"]
        ]

        # Display the best matching shortlisted jobs first.
        print("\n========== BEST MATCHING JOBS ==========")

        if shortlisted_jobs:
            for result in shortlisted_jobs:
                screening.display_result(candidate, result)
        else:
            print("No jobs shortlisted.")

        # Display rejected jobs below the shortlisted jobs.
        print("\n========== REJECTED JOBS ==========")

        if rejected_jobs:
            for result in rejected_jobs:
                screening.display_result(candidate, result)
        else:
            print("No rejected jobs.")

        # Final summary.
        print("\n========== FINAL SUMMARY ==========")

        print(
            "Shortlisted Jobs:",
            ", ".join(
                result["job"].job_title
                for result in shortlisted_jobs
            ) if shortlisted_jobs else "None"
        )

        print(
            "Rejected Jobs:",
            ", ".join(
                result["job"].job_title
                for result in rejected_jobs
            ) if rejected_jobs else "None"
        )

    except ValueError as error:
        print("\nInput Error:", error)

    except Exception as error:
        print("\nUnexpected Error:", error)


if __name__ == "__main__":
    main()
