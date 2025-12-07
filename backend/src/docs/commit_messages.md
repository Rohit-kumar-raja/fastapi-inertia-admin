# Commit Message Guidelines
- Use the following format for commit messages:
```bash
<type>: <subject>
```
- `<type>`: Type of the commit (e.g., feat, fix, docs, style, refactor, test, revert)
- `<subject>`: Short description of the change

| Type     | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| feat     | A new feature or enhancement                                                |
| fix      | A bug fix                                                                    |
| docs     | Documentation changes                                                        |
| style    | Changes that do not affect the meaning of the code (white-space, formatting)|
| refactor | Code changes that neither fixes a bug nor adds a feature                    |
| test     | Adding missing tests or correcting existing tests                           |
| revert   | Reverting changes                                                           |


#### Examples:
single line commit message:
```bash
git commit -m "feat: add new feature"
```

multi-line commit message:
```bash
git commit
feat: add authentication feature using JWT

This commit introduces JWT-based authentication to secure API endpoints.
It includes token generation and middleware for token validation.

Related issue: #123
```