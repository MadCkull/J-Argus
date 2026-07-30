---
name: job-application-assistant
description: >
  Assists with job applications: evaluating job postings, tailoring CVs, writing
  cover letters, and preparing for interviews. This is a cross-runtime pointer
  skill — it delegates to the canonical workflow specification maintained in
  .claude/skills/job-application-assistant/. Triggers on keywords like: job posting,
  job application, CV, cover letter, resume, interview prep, job fit, career,
  application, apply, ansøgning, stilling
context: fork
---

# Job Application Assistant (Cross-Runtime Pointer)

This skill delegates to the canonical workflow specification. Follow these steps:

## Step 1: Load the Canonical Spec

Read `.claude/skills/job-application-assistant/SKILL.md` and follow the workflow
defined there. That file references 8 companion specification files in the same
directory — read each one as the workflow requires:

| File | Purpose |
|------|---------|
| `01-candidate-profile.md` | Education, experience, skills, publications, awards |
| `02-behavioral-profile.md` | Behavioral assessment, strengths, ideal environments |
| `03-writing-style.md` | Tone, structure, do's and don'ts |
| `04-job-evaluation.md` | Scoring framework for job fit |
| `05-cv-templates.md` | LaTeX CV structure and tailoring rules |
| `06-cover-letter-templates.md` | LaTeX cover letter structure and tailoring rules |
| `07-interview-prep.md` | STAR examples, tough questions, roleplay guidelines |
| `08-application-forms.md` | Portal free-text fields: self-introduction, project entries, character-limited pitches |

All paths are relative to `.claude/skills/job-application-assistant/`.

## Step 2: Load the Candidate Profile

Read `CLAUDE.md` (repo root) for the candidate's full profile, goals, and
workflow rules.

## Step 3: Translate Tool Names

The canonical spec uses Claude Code tool names. See `.agents/TOOL_GLOSSARY.md`
for the mapping to your runtime's equivalents.

## Quick Commands

The user may request individual steps without the full workflow:
- "Evaluate this job posting" — Step 1 (Evaluate Fit) only
- "Write a CV for [company]" — Step 2 (Tailor CV) only
- "Write a cover letter for [role] at [company]" — Step 3 (Cover Letter) only
- "Help me prepare for an interview at [company]" — Step 4 (Interview Prep) only
- "What jobs should I look for?" — Career strategy discussion
