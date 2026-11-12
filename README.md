# Resume Screening System using Python OOP

A beginner-friendly Python mini-project that screens a candidate against predefined job requirements. It compares skills, calculates a match percentage, checks experience and qualification eligibility, and displays shortlisted jobs before rejected jobs.

## Features

- Collects candidate name, skills, qualification, and experience level through the terminal.
- Screens against four predefined jobs: Python Developer, Data Analyst, GenAI Developer, and Embedded Tester.
- Calculates skill match percentage using case-insensitive, exact skill matching.
- Checks experience and qualification eligibility for each job.
- Shortlists jobs when skill match is **at least 70%** and both eligibility checks pass.
- Ranks jobs by skill match percentage, showing shortlisted jobs first and rejected jobs afterward.
- Handles invalid inputs with exception handling.

## OOP Concepts Used

| Concept | Implementation |
| --- | --- |
| Encapsulation | Private candidate attributes and getter methods in `Candidate` |
| Inheritance | `FresherCandidate` and `ExperiencedCandidate` inherit from `Candidate` |
| Polymorphism | Both candidate subclasses override `check_experience()` |
| Abstraction | `ScreeningProcess` defines an abstract `screen_candidate()` method, implemented by `ResumeScreening` |

## Requirements

- Python 3.8 or later
- No third-party libraries required

## How to Run

1. Clone this repository or download the Python file.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python Resume_Screening_System_Final.py
   ```

4. Enter your name, comma-separated skills, qualification, and candidate type (`1` for Fresher or `2` for Experienced). Experienced candidates are also prompted for years of experience.

## Example Input

```text
Enter candidate name: Arun
Enter skills (comma separated): Python, OOP, SQL, Django, LLM, RAG, LangChain
Enter qualification: BSc Computer Science
Enter your choice (1 or 2): 1
```

## Example Screening Summary

```text
========== BEST MATCHING JOBS ==========
Job: Python Developer
Matched Skills: Python, OOP, SQL, Django
Skill Match: 100.0 %
Experience Eligibility: Eligible
Qualification Eligibility: Eligible
Screening Status: SHORTLISTED

Job: GenAI Developer
Matched Skills: Python, LLM, RAG, LangChain
Skill Match: 100.0 %
Experience Eligibility: Eligible
Qualification Eligibility: Eligible
Screening Status: SHORTLISTED

========== REJECTED JOBS ==========
Job: Data Analyst
Skill Match: 50.0 %
Screening Status: REJECTED

Job: Embedded Tester
Skill Match: 0.0 %
Screening Status: REJECTED

========== FINAL SUMMARY ==========
Shortlisted Jobs: Python Developer, GenAI Developer
Rejected Jobs: Data Analyst, Embedded Tester
```

## How Skill Matching Works

The matching percentage is calculated as:

```text
Skill Match (%) = (Number of Matched Required Skills / Total Required Skills) * 100
```

For example, matching 3 out of 4 required skills gives a **75%** match.

A job is **shortlisted** only when all three conditions are satisfied:

1. Skill match is at least 70%.
2. The candidate meets the job's minimum experience requirement.
3. The candidate meets the job's qualification requirement.

The jobs in the current example use `Any` as the qualification requirement. A fresher is eligible only for jobs requiring 0 years of experience.
