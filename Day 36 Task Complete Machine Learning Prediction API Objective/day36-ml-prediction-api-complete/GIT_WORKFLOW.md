# Git Feature Branch & Pull Request Workflow - Week 6 Capstone

This documents how this final Week 6 project was delivered through a feature
branch and Pull Request, instead of committing straight to main.

## Steps

1. **Start from the latest main branch**
```
git checkout main
git pull origin main
```

2. **Create a feature branch for this week's work**
```
git checkout -b feature/complete-ml-api
```

3. **Build the complete API on the feature branch**

`main.py` on this branch includes:
- Health check and prediction endpoints
- Pydantic request and response models
- Structured error handling for validation, missing data, and model load failures
- Logging middleware and event logging saved to `logs/api.log`

4. **Commit the work with a clear message**
```
git add main.py
git commit -m "feature: add complete ML prediction API with validation, error handling, and logging"
```

5. **Push the branch and open a Pull Request**
```
git push origin feature/complete-ml-api
```
On GitHub: compare `feature/complete-ml-api` into `main`, add a description of
what was built this week, and open the Pull Request.

6. **Review**

Check the diff, confirm the endpoints work as expected, and address any review
comments by pushing more commits to the same branch.

7. **Merge**

Once approved, merge the Pull Request into `main` and delete the feature branch.

8. **Sync local main**
```
git checkout main
git pull origin main
```

## Local proof of this workflow

This environment does not have push access to a personal GitHub repository, so
the same commands were run against a local git repository inside this project
folder to prove they work end to end: a `feature/complete-ml-api` branch was
created, the full API was committed there, and it was merged back into
`master` with a real merge commit. See `screenshots/git_commit_log.png` for
the actual output of `git log` on this repository.

To finish this for real, add your GitHub repository as a remote and push:
```
git remote add origin <your-repo-url>
git push -u origin master
git push origin feature/complete-ml-api
```
Then open and merge the Pull Request on GitHub using the steps above.
