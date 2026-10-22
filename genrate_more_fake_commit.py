#!/usr/bin/env python3
"""
Automatically create a GitHub repository from the current directory
and backdate-commit files.

Workflow:
  1. Remove existing .git directory.
  2. Create xyz.txt containing "hello".
  3. Initialize Git repository.
  4. Commit xyz.txt as the first commit.
  5. Rename branch to main.
  6. Create GitHub repository automatically using gh.
  7. Add SSH remote automatically.
  8. Push initial commit.
  9. Use current directory as source directory.
  10. Ask for first backdated commit date.
  11. Commit each project file individually.
  12. Remove xyz.txt.
  13. Show number of commits created so far.
  14. Optionally create extra auto-generated commits in README.md.
  15. Show final commit count.
  16. Push all commits to GitHub.
"""

import os
import shutil
import subprocess
from datetime import datetime, timedelta


# ============================================================
# CONFIGURATION
# ============================================================

GAP_DAYS = 2

INITIAL_FILE = "xyz.txt"
INITIAL_CONTENT = "hello\n"

GITHUB_USERNAME = "csb3799"

REPOSITORY_VISIBILITY = "public"


# ============================================================
# COMMIT COUNTER
# ============================================================

# The initial "first commit" will be created below.
created_commit_count = 0


# ============================================================
# HELPER FUNCTION
# ============================================================

def run_command(command, cwd=None, env=None):
    """
    Run a command and stop the script if it fails.
    """

    print(f"$ {' '.join(command)}")

    subprocess.run(
        command,
        check=True,
        cwd=cwd,
        env=env,
    )


# ============================================================
# CURRENT REPOSITORY DIRECTORY
# ============================================================

REPO_DIR = os.path.abspath(".")


# ============================================================
# GET REPOSITORY NAME FROM DIRECTORY
# ============================================================

repo_name = os.path.basename(
    os.path.normpath(REPO_DIR)
)

if not repo_name:

    print(
        "ERROR: Could not determine repository name "
        "from current directory."
    )

    exit(1)


# ============================================================
# DISPLAY INFORMATION
# ============================================================

print()
print("=" * 70)
print("AUTOMATED GITHUB REPOSITORY SETUP")
print("=" * 70)

print()
print(f"Project directory : {REPO_DIR}")
print(f"Repository name   : {repo_name}")
print(f"GitHub account    : {GITHUB_USERNAME}")
print(f"Visibility        : {REPOSITORY_VISIBILITY}")


# ============================================================
# VERIFY GITHUB CLI
# ============================================================

print()
print("=" * 70)
print("CHECKING GITHUB CLI")
print("=" * 70)

if shutil.which("gh") is None:

    print()
    print("ERROR: GitHub CLI 'gh' is not installed.")
    print()
    print("Install GitHub CLI and run:")
    print("    gh auth login")
    print()

    exit(1)

print()
print("GitHub CLI found.")


# ============================================================
# VERIFY GITHUB AUTHENTICATION
# ============================================================

print()
print("Checking GitHub authentication...")

gh_auth = subprocess.run(
    ["gh", "auth", "status"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

if gh_auth.returncode != 0:

    print()
    print("ERROR: GitHub CLI is not authenticated.")
    print()
    print("Run:")
    print("    gh auth login")
    print()

    exit(1)

print("GitHub authentication verified.")


# ============================================================
# REMOVE EXISTING .git
# ============================================================

print()
print("=" * 70)
print("RESETTING LOCAL GIT REPOSITORY")
print("=" * 70)

git_dir = os.path.join(
    REPO_DIR,
    ".git"
)

if os.path.exists(git_dir):

    print()
    print("Removing existing .git directory...")

    shutil.rmtree(git_dir)

    print(".git removed successfully.")

else:

    print()
    print("No existing .git directory found.")


# ============================================================
# REMOVE EXISTING xyz.txt
# ============================================================

initial_file_path = os.path.join(
    REPO_DIR,
    INITIAL_FILE
)

if os.path.exists(initial_file_path):

    print()
    print(f"Removing existing {INITIAL_FILE}...")

    os.remove(initial_file_path)


# ============================================================
# CREATE xyz.txt
# ============================================================

print()
print(f"Creating {INITIAL_FILE}...")

with open(
    initial_file_path,
    "w"
) as f:

    f.write(INITIAL_CONTENT)

print(
    f"{INITIAL_FILE} created with content: hello"
)


# ============================================================
# GIT INIT
# ============================================================

print()
print("Initializing Git repository...")

run_command(
    [
        "git",
        "init"
    ],
    cwd=REPO_DIR
)


# ============================================================
# GIT ADD xyz.txt
# ============================================================

print()
print("Adding xyz.txt...")

run_command(
    [
        "git",
        "add",
        INITIAL_FILE
    ],
    cwd=REPO_DIR
)


# ============================================================
# FIRST COMMIT
# ============================================================

print()
print("Creating initial commit...")

run_command(
    [
        "git",
        "commit",
        "-m",
        "first commit"
    ],
    cwd=REPO_DIR
)

created_commit_count += 1


# ============================================================
# RENAME BRANCH TO MAIN
# ============================================================

print()
print("Renaming branch to main...")

run_command(
    [
        "git",
        "branch",
        "-M",
        "main"
    ],
    cwd=REPO_DIR
)


# ============================================================
# CREATE GITHUB REPOSITORY
# ============================================================

print()
print("=" * 70)
print("CREATING GITHUB REPOSITORY")
print("=" * 70)

print()

print(
    f"Creating GitHub repository: "
    f"{GITHUB_USERNAME}/{repo_name}"
)

create_result = subprocess.run(
    [
        "gh",
        "repo",
        "create",
        repo_name,
        "--public"
    ],
    cwd=REPO_DIR
)

if create_result.returncode != 0:

    print()
    print("ERROR: GitHub repository creation failed.")
    print()
    print(
        f"Repository '{repo_name}' may already exist."
    )
    print()

    exit(1)

print()
print("GitHub repository created successfully.")


# ============================================================
# ADD SSH REMOTE
# ============================================================

remote_url = (
    f"git@github.com:"
    f"{GITHUB_USERNAME}/"
    f"{repo_name}.git"
)

print()
print("=" * 70)
print("CONFIGURING GIT REMOTE")
print("=" * 70)

print()
print(f"Remote URL: {remote_url}")

run_command(
    [
        "git",
        "remote",
        "add",
        "origin",
        remote_url
    ],
    cwd=REPO_DIR
)


# ============================================================
# INITIAL PUSH
# ============================================================

print()
print("=" * 70)
print("PUSHING INITIAL COMMIT")
print("=" * 70)

print()

run_command(
    [
        "git",
        "push",
        "-u",
        "origin",
        "main"
    ],
    cwd=REPO_DIR
)

print()
print("Initial commit pushed successfully.")


# ============================================================
# SOURCE DIRECTORY
# ============================================================

source_dir = REPO_DIR

print()
print("=" * 70)
print("BACKDATED FILE IMPORT")
print("=" * 70)

print()
print(f"Source directory: {source_dir}")


# ============================================================
# INPUT: FIRST COMMIT DATE
# ============================================================

start_date = input(
    "\nEnter first commit date "
    "(YYYY-MM-DD HH:MM:SS): "
).strip()

try:

    commit_date = datetime.strptime(
        start_date,
        "%Y-%m-%d %H:%M:%S"
    )

except ValueError:

    print()
    print("Invalid date format.")
    print(
        "Example: 2025-01-01 10:30:00"
    )

    exit(1)


# ============================================================
# GET FILE LIST
# ============================================================

files = []

for root, dirs, filenames in os.walk(source_dir):

    # Never enter .git
    dirs[:] = [
        d
        for d in dirs
        if d != ".git"
    ]

    for f in filenames:

        full_path = os.path.join(
            root,
            f
        )

        rel_path = os.path.relpath(
            full_path,
            source_dir
        )

        # xyz.txt is handled separately
        if rel_path == INITIAL_FILE:
            continue

        files.append(rel_path)


# Sort files for deterministic order
files.sort()


# ============================================================
# FILE COUNT
# ============================================================

if not files:

    print()
    print(
        "No additional files found "
        "in source directory."
    )

else:

    print()
    print(
        f"Found {len(files)} files "
        f"in '{source_dir}'."
    )


# ============================================================
# COMMIT EACH FILE
# ============================================================

for rel_path in files:

    date_string = commit_date.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    env = os.environ.copy()

    env["GIT_AUTHOR_DATE"] = date_string
    env["GIT_COMMITTER_DATE"] = date_string


    print()
    print("-" * 70)

    print(
        f"Committing: {rel_path}"
    )

    print(
        f"Date      : {date_string}"
    )


    # --------------------------------------------------------
    # ADD FILE
    # --------------------------------------------------------

    subprocess.run(
        [
            "git",
            "add",
            "--",
            rel_path
        ],
        check=True,
        cwd=REPO_DIR
    )


    # --------------------------------------------------------
    # CHECK STAGED CHANGES
    # --------------------------------------------------------

    diff_check = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet"
        ],
        cwd=REPO_DIR
    )


    if diff_check.returncode == 0:

        print(
            "  (no changes — "
            "already committed, skipping)"
        )

        commit_date += timedelta(
            days=GAP_DAYS
        )

        continue


    # --------------------------------------------------------
    # COMMIT
    # --------------------------------------------------------

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"Add {os.path.basename(rel_path)}"
        ],
        check=True,
        cwd=REPO_DIR,
        env=env
    )

    created_commit_count += 1


    # --------------------------------------------------------
    # INCREASE DATE
    # --------------------------------------------------------

    commit_date += timedelta(
        days=GAP_DAYS
    )


# ============================================================
# REMOVE xyz.txt
# ============================================================

remove_path = os.path.join(
    REPO_DIR,
    INITIAL_FILE
)

if os.path.exists(remove_path):

    date_string = commit_date.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    env = os.environ.copy()

    env["GIT_AUTHOR_DATE"] = date_string
    env["GIT_COMMITTER_DATE"] = date_string


    print()
    print("-" * 70)

    print(
        f"Removing  : {INITIAL_FILE}"
    )

    print(
        f"Date      : {date_string}"
    )


    # --------------------------------------------------------
    # GIT RM
    # --------------------------------------------------------

    subprocess.run(
        [
            "git",
            "rm",
            "--",
            INITIAL_FILE
        ],
        check=True,
        cwd=REPO_DIR
    )


    # --------------------------------------------------------
    # CHECK STAGED CHANGES
    # --------------------------------------------------------

    diff_check = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet"
        ],
        cwd=REPO_DIR
    )


    if diff_check.returncode == 0:

        print(
            "  (nothing staged — "
            "already removed/committed, skipping)"
        )

    else:

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"Remove {INITIAL_FILE}"
            ],
            check=True,
            cwd=REPO_DIR,
            env=env
        )

        created_commit_count += 1


    commit_date += timedelta(
        days=GAP_DAYS
    )

else:

    print(
        f"'{INITIAL_FILE}' not found in repo, "
        "skipping removal."
    )


# ============================================================
# SHOW CURRENT COMMIT COUNT
# ============================================================

print()
print("=" * 70)
print("COMMIT SUMMARY")
print("=" * 70)

print()

print(
    f"Commits created so far: "
    f"{created_commit_count}"
)

print()

print(
    "If you have a target total, "
    "subtract the number above from it "
    "to determine how many extra commits to add."
)


# ============================================================
# OPTIONAL: EXTRA AUTO-GENERATED COMMITS
# ============================================================

print()
print("=" * 70)
print("EXTRA AUTO-GENERATED COMMITS")
print("=" * 70)

extra_input = input(
    "\nHow many extra auto-generated commits "
    "do you want to add? (0 to skip): "
).strip()


try:

    extra_count = (
        int(extra_input)
        if extra_input
        else 0
    )

except ValueError:

    print(
        "Invalid number. Using 0."
    )

    extra_count = 0


# Prevent negative values
if extra_count < 0:

    print(
        "Negative commit count is not valid. "
        "Using 0."
    )

    extra_count = 0


# ============================================================
# CREATE EXTRA COMMITS
# ============================================================

if extra_count > 0:

    # --------------------------------------------------------
    # EXTRA COMMIT GAP
    # --------------------------------------------------------

    gap_input = input(
        f"Gap between these commits in days "
        f"(default {GAP_DAYS}): "
    ).strip()


    try:

        extra_gap_days = (
            int(gap_input)
            if gap_input
            else GAP_DAYS
        )

    except ValueError:

        print(
            "Invalid gap. "
            f"Using default {GAP_DAYS} days."
        )

        extra_gap_days = GAP_DAYS


    # Prevent negative gap
    if extra_gap_days < 0:

        print(
            "Negative gap is not valid. "
            f"Using {GAP_DAYS} days."
        )

        extra_gap_days = GAP_DAYS


    # --------------------------------------------------------
    # AUTO FILE
    # --------------------------------------------------------

    AUTO_FILE = "README.md"

    auto_path = os.path.join(
        REPO_DIR,
        AUTO_FILE
    )


    if not os.path.exists(auto_path):

        print(
            f"'{AUTO_FILE}' not found in repo, "
            "creating it."
        )

        with open(
            auto_path,
            "a"
        ):
            pass


    print()
    print(
        f"Adding {extra_count} "
        f"auto-generated commit(s) "
        f"to '{AUTO_FILE}'..."
    )

    print()


    # --------------------------------------------------------
    # CREATE EXTRA COMMITS
    # --------------------------------------------------------

    for i in range(
        1,
        extra_count + 1
    ):

        date_string = commit_date.strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # Add an HTML comment to README.md
        with open(
            auto_path,
            "a"
        ) as f:

            f.write(
                f"\n"
                f"<!-- auto-update "
                f"{date_string} -->\n"
            )


        env = os.environ.copy()

        env["GIT_AUTHOR_DATE"] = date_string
        env["GIT_COMMITTER_DATE"] = date_string


        print(
            f"Committing: {AUTO_FILE} "
            f"(auto commit "
            f"{i}/{extra_count})"
        )

        print(
            f"Date      : {date_string}"
        )


        subprocess.run(
            [
                "git",
                "add",
                AUTO_FILE
            ],
            check=True,
            cwd=REPO_DIR
        )


        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"Update {AUTO_FILE}"
            ],
            check=True,
            cwd=REPO_DIR,
            env=env
        )


        created_commit_count += 1


        commit_date += timedelta(
            days=extra_gap_days
        )


else:

    print(
        "\nNo extra auto-generated commits requested."
    )


# ============================================================
# FINAL COMMIT COUNT
# ============================================================

print()
print("=" * 70)
print("FINAL COMMIT SUMMARY")
print("=" * 70)

print()

print(
    f"Total commits created: "
    f"{created_commit_count}"
)


# ============================================================
# FINAL PUSH
# ============================================================

print()
print("=" * 70)
print("PUSHING ALL COMMITS")
print("=" * 70)

print()

run_command(
    [
        "git",
        "push"
    ],
    cwd=REPO_DIR
)


# ============================================================
# DONE
# ============================================================

print()
print("=" * 70)
print("DONE")
print("=" * 70)

print()

print(
    "All commits have been pushed successfully."
)

print()

print(
    "Repository:"
)

print(
    f"https://github.com/"
    f"{GITHUB_USERNAME}/"
    f"{repo_name}"
)

print()
