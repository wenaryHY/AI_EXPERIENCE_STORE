# AI Experience Store

This repository stores **AI-generated experience documents** from multiple devices or sessions.  
It supports **automatic merge, versioning, branch-based management, and PRs** via GitHub Actions.

## Directory Structure

AI_EXPERIENCE_STORE/
├─ .github/workflows/auto-update-experience-docs.yml # Workflow definition
├─ experience_jsons/ # All raw JSON experience files
│ ├─ 00.json
│ ├─ 01.json
│ └─ ...
├─ scripts/
│ └─ merge_experience_docs.py # Python merge script
├─ requirements.txt # Python dependencies
└─ README.md


## Workflow

- Trigger: manual (`workflow_dispatch`) or push to `master`
- Steps:
    1. Checkout repository
    2. Setup Python 3.11
    3. Install dependencies from `requirements.txt`
    4. Merge JSON experience files into `experience_master.json`
    5. Push changes to a timestamped branch
    6. Create PR to `master` automatically

## How to Use

1. Add new JSON files in `experience_jsons/`
2. Trigger workflow manually or push to `master`
3. Review and merge the PR to update `experience_master.json`

## Notes

- Each entry in `experience_master.json` has:
    - `timestamp`: UTC time of generation
    - `source_file`: original JSON file
    - `task_context`: short description of the task
    - `principle`: the experience or rule
- Workflow keeps history via branches, so old experiences are traceable.