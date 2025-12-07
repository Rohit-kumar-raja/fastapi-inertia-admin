# Branching Guidelines:
We are following mixup of `Github Flow` + `Git Flow` branching strategy. we have two main branches:
  - `main`: This branch is always stable and contains the latest release.
  - `develop`: This branch is used for development purposes.

## For Features and Bugs:
- To start working on a new feature or bug, create a new branch from `dev` branch.
- Branch name should be in the format `feature/<feature-name>` or `bugfix/<bug-name>`.
- Once the feature or bug is complete, create a pull request to `develop` branch.
- Once the pull request is merged, delete the feature or bug branch.

## For Hotfixes:
- For hotfixes, create a branch from `main` branch and create a pull request to `main` branch.
- Once the pull request is merged, delete the hotfix branch.

Note: if multiple developers are working on the same feature/bugfix/hotfix, they can create a branch like:
`feature/<feature-name>-<developer-name>`
`bugfix/<bug-name>-<developer-name>`
`hotfix/<hotfix-name>-<developer-name>`
