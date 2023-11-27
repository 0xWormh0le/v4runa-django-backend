# Varuna Backend API

## Requirements
- [Python 3.7 or above](https://www.python.org/downloads/)
- [Postgresql](https://www.postgresql.org/download/)
- [pipenv](https://github.com/pypa/pipenv)

## Installation

### On local environment
1. Go into the pipenv

    $ pipenv shell

2. Install packages

    $ pipenv install

3. Copy `.env.example` file to `.env` and fill in the env variables to configure database.

4. Run migrations

    $ ./manage.py migrate

5. Run server

    $ ./manage.py runserver


## Development Flow

Here are the steps of the process you need to follow in order to integrate new code or a new feature into the project:

1. Transition the status of the card that describes the feature you will be working on in our JIRA project to be In Progress.
2. Create a local branch to get started using git: git checkout -b <feature|bug|task>/<jira-number>-<short-description>. For instance, this could be a branch name: feature/96-add-navigation-sidebar.
    - The first part indicates whether it is new feature, bug or documentation, while the second part it is just the JIRA card number followed by some short description.
3. Develop the new feature while doing atomic commits to your local branch using git commit.
4. After you are done, rebase your branch against the remote develop so your new commits are applied on top of any changes that occurred. As you rebase, you'll need to locally fix the conflicts on your branch for each commit applied.
5. Before creating the Pull Request, you need to make sure the tests pass. Git hooks should be employed to enforce this.
    - npm test
6. Now you are ready to create a new Pull Request with your changes:
    - Push your changes to origin using git push -u origin <your-branch-name>
    - Then go to https://github.com/Varunatech/iCCR/compare?expand=1 and select your branch on the compare: dropdown. You'll be using develop as the base branch. Press View pull request after that.
    - If you see a green sign "Able to merge", go to the next step. If you see a red sign "Can't automatically merge", you will need to resolve the conflicts in your branch with the destination branch. See: https://github.com/genome/docs/wiki/How-do-I-fix-my-pull-request-if-it-cannot-be-automatically-merged%3F
    - Add a small comment with your changes, and add the Reviewers using the column on the right. Finally, press the button to create the PR.
7. After this happens, a new message will be automatically posted to the #frontend channel in Slack. Moreover, the reviewers will be notified by email. Notice the develop branch is set as a protected branch in Github so you'll need at least one approval before you can merge.
8. Your code will be reviewed, you can update the branch with new changes after you get some feedback.
9. After the Pull Request is approved, merge it using the UI on Github (you can also remove the branch directly from the same page, which is also convenient). Your code will land to the develop branch (and eventually deployed into the staging environment). Delete the feature branch after successful merge.
10. Finally, remember to transition your JIRA card to Done.
