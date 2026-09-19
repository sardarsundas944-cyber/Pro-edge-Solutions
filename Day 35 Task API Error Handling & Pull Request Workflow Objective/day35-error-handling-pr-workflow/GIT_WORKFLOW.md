# Git Feature Branch & Pull Request Workflow

This documents the steps used to add this week's error handling work through a
proper feature branch and Pull Request, instead of committing straight to main.

## Steps

1. **Create a feature branch from the latest main branch**
```
git checkout main
git pull origin main
git checkout -b feature/error-handling
```

2. **Make the code changes**

Edited `main.py` to add:
- a handler for validation errors (`RequestValidationError`)
- a handler for HTTP errors (`HTTPException`)
- a general fallback handler for unexpected errors
- a check for whether the model loaded successfully before using it

3. **Commit the changes with a clear message**
```
git add main.py
git commit -m "feature: add structured error handling for validation, missing data, and model load failures"
```

4. **Push the feature branch to GitHub**
```
git push origin feature/error-handling
```

5. **Open a Pull Request on GitHub**

- Go to the repository on GitHub
- GitHub will show a banner to compare & create a pull request for the pushed branch
- Base branch: `main`, compare branch: `feature/error-handling`
- Add a title and description explaining what changed and why
- Open the Pull Request

6. **Review the Pull Request**

- Check the diff tab to confirm only the intended changes are included
- Test the branch locally if needed
- Leave review comments if something needs to change, then push more commits
  to the same branch to update the Pull Request automatically

7. **Merge the Pull Request**

- Once approved, click "Merge pull request" on GitHub
- Choose a merge strategy (this project used a regular merge commit)
- Delete the feature branch after merging since it is no longer needed

8. **Update local main branch**
```
git checkout main
git pull origin main
```

## Local proof of this workflow

Since actually pushing to GitHub requires personal repository access and
credentials that this environment does not have, the steps above were run
against a local git repository inside this project folder to prove the same
commands work end to end: a `feature/error-handling` branch was created, the
error handling changes were committed there, and the branch was merged back
into `master` with a merge commit, exactly like a Pull Request merge would
produce. See `screenshots/git_commit_log.png` and `screenshots/git_branch.png`
for the real output of these commands.

To finish this for real, run the same `git push` and open the Pull Request on
your own GitHub repository using the steps above.
