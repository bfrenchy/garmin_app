# garmin_app

Product support web app for Garmin

## Running .py files as packages

This works if you run `python -m tests.test_app`, but not any other way.
Supposedly it should work on GitHub too.

* `from sifter_support_shared.functions.doc_loader import load_document`

## Updating the Submodule on Mac OS

If the submodule is updated, you can fetch the changes and update your local copy with the following commands:

```bash
git submodule update --remote --merge
```

This command fetches the latest changes in the submodule, and merges them into your local copy. If you want to checkout a particular commit of the submodule, you can use:

```bash
git submodule update --remote --checkout <commit-hash>
```

## Handy Git Commands for Mac OS

Here are some handy git commands that may come in handy on Mac OS:

```bash
git status # Shows the status of changes as untracked, modified, or staged.
git add . # Adds all changes to the staging area.
git commit -m "Your message" # Commits the changes in the staging area with a message.
git push origin <branch-name> # Pushes the changes to the specified branch.
git pull origin <branch-name> # Pulls the latest changes from the specified branch.
git checkout -b <branch-name> # Creates a new branch and switches to it.
git branch -d <branch-name> # Deletes the specified branch.
```

## Managing and Using Branches

Here are some commands for managing and using branches:

* `git branch`: List all local branches.
* `git branch -a`: List all local and remote branches.
* `git branch <branch_name>`: Create a new branch.
* `git checkout <branch_name>`: Switch to a different branch.
* `git merge <branch_name>`: Merge a branch into the current branch.
* `git branch -d <branch_name>`: Delete a branch.
* `git push origin <branch_name>`: Push a branch to the remote repository.
* `git pull origin <branch_name>`: Pull the latest changes from a specific branch.
