# Branching Strategy and Workflow

## Overview

This project follows a **Git Flow**-inspired branching strategy with strict versioning and feature isolation.

## Branch Structure

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Protected branch, requires PR approval
- **Merges from**: `dev` branch only
- **Versioning**: Tagged with semantic versions (v0.1.0, v1.0.0, etc.)
- **Never commit directly**: All changes via PR from `dev`

#### `dev`
- **Purpose**: Integration branch for completed features
- **Protection**: Protected branch, requires PR approval
- **Merges from**: Feature branches, hotfix branches
- **Merges to**: `main` for releases
- **Testing**: All features must pass CI before merging

### Supporting Branches

#### Feature Branches: `feature/<feature-name>`
- **Purpose**: Develop new features or enhancements
- **Naming convention**: 
  - `feature/jwt-auth`
  - `feature/sample-upload-api`
  - `feature/chemometric-preprocessing`
  - `feature/constitution-v1.0.0`
- **Branch from**: `dev`
- **Merge to**: `dev`
- **Lifecycle**: Delete after successful merge
- **Example**:
  ```bash
  git checkout dev
  git checkout -b feature/jwt-auth
  # ... develop feature ...
  git commit -m "feat(auth): implement JWT authentication"
  git push -u origin feature/jwt-auth
  # Create PR to dev
  ```

#### Hotfix Branches: `hotfix/<issue>`
- **Purpose**: Critical bug fixes for production
- **Naming convention**: 
  - `hotfix/security-patch`
  - `hotfix/database-connection`
- **Branch from**: `main`
- **Merge to**: Both `main` AND `dev`
- **Lifecycle**: Delete after successful merge
- **Example**:
  ```bash
  git checkout main
  git checkout -b hotfix/security-patch
  # ... fix issue ...
  git commit -m "fix(security): patch JWT token expiration"
  # Merge to main and dev
  ```

#### Release Branches: `release/<version>` (Optional for Phase 4+)
- **Purpose**: Prepare for production release
- **Naming convention**: `release/v1.0.0`
- **Branch from**: `dev`
- **Merge to**: `main` and `dev`
- **Use case**: Version bumps, final testing, documentation updates

## Workflow

### Standard Feature Development

1. **Create Issue**
   ```bash
   # Create GitHub issue first
   # Issue #1: Implement JWT Authentication
   ```

2. **Create Feature Branch**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/jwt-auth
   ```

3. **Develop with TDD**
   ```bash
   # Write tests first
   git add tests/test_auth.py
   git commit -m "test(auth): add JWT authentication tests"
   
   # Implement feature
   git add app/core/security.py
   git commit -m "feat(auth): implement JWT token generation and validation"
   
   # Run tests
   pytest
   ```

4. **Push and Create PR**
   ```bash
   git push -u origin feature/jwt-auth
   # Create PR on GitHub to merge into dev
   # Link PR to issue #1
   ```

5. **Code Review and CI**
   - GitHub Actions runs tests
   - Reviewer approves changes
   - All checks must pass

6. **Merge to Dev**
   ```bash
   # Via GitHub PR merge (no-ff)
   git checkout dev
   git pull origin dev
   ```

7. **Delete Feature Branch**
   ```bash
   git branch -d feature/jwt-auth
   git push origin --delete feature/jwt-auth
   ```

### Release to Main

1. **Prepare Release**
   ```bash
   git checkout dev
   # Ensure all features for release are merged
   # Update CHANGELOG.md
   git commit -m "docs: update CHANGELOG for v0.2.0"
   ```

2. **Merge to Main**
   ```bash
   git checkout main
   git merge --no-ff dev -m "release: version 0.2.0"
   ```

3. **Tag Release**
   ```bash
   git tag -a v0.2.0 -m "Release version 0.2.0 - Phase 1 complete"
   git push origin main --tags
   ```

4. **Sync Dev**
   ```bash
   git checkout dev
   git merge main
   git push origin dev
   ```

## Versioning Strategy

### Semantic Versioning: MAJOR.MINOR.PATCH

- **MAJOR (1.0.0)**: Breaking changes to APIs or core principles
  - API contract changes
  - Database schema breaking changes
  - Constitution major amendments
  
- **MINOR (0.1.0)**: New features, backward-compatible
  - New API endpoints
  - New chemometric models
  - Constitution minor amendments (new principles)
  
- **PATCH (0.0.1)**: Bug fixes, documentation
  - Bug fixes
  - Documentation updates
  - Constitution clarifications

### Version Progression

- **v0.1.0**: Phase 1 - Backend skeleton (initial release)
- **v0.2.0**: Phase 1 - JWT auth + sample upload complete
- **v0.3.0**: Phase 2 - Chemometric preprocessing
- **v0.4.0**: Phase 2 - Classifier integration
- **v1.0.0**: Phase 3 - Frontend + full workflow
- **v2.0.0**: Phase 4 - Production-ready with observability

## Commit Message Convention

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring without feature changes
- `chore`: Build, dependencies, tooling
- `perf`: Performance improvements
- `style`: Code style/formatting changes

### Examples
```bash
feat(auth): implement JWT token generation

- Add token generation function
- Add token validation middleware
- Configure JWT secret in environment

Closes #1

---

fix(db): resolve connection pool exhaustion

- Increase max connections to 20
- Add connection timeout handling
- Add retry logic with exponential backoff

Fixes #15

---

docs: update constitution to v1.0.1

- Clarify security requirements
- Add examples for authentication flow
- Fix typo in principle III

---

test(preprocessing): add baseline correction tests

- Test polynomial baseline correction
- Test ALS baseline correction
- Add edge case handling tests
```

## Branch Protection Rules

### Main Branch
- Require pull request reviews before merging
- Require status checks to pass (CI/CD)
- Require branches to be up to date before merging
- Do not allow force pushes
- Do not allow deletions

### Dev Branch
- Require pull request reviews before merging
- Require status checks to pass (CI/CD)
- Require branches to be up to date before merging
- Allow force pushes for maintainers only
- Do not allow deletions

## Current Repository State

### Branches
- ✅ `main`: v0.1.0 - Project initialized
- ✅ `dev`: Constitution v1.0.0 merged
- ✅ `feature/constitution-v1.0.0`: Constitution development (can be deleted after confirmation)

### Recent Commits
```
*   133b742 (dev) merge: feature/constitution-v1.0.0 into dev
|\  
| * 96e3f47 (feature/constitution-v1.0.0) docs: create constitution v1.0.0
|/  
* 66e779f (main) chore: initialize project structure v0.1.0
```

### Next Steps
1. Review constitution on `dev` branch
2. If approved, merge `dev` to `main` and tag as v0.1.1
3. Delete `feature/constitution-v1.0.0` branch
4. Start Phase 1 implementation with new feature branches

## Quick Reference Commands

### Create new feature
```bash
git checkout dev
git pull origin dev
git checkout -b feature/<name>
```

### Update from dev
```bash
git checkout feature/<name>
git fetch origin
git rebase origin/dev
```

### Complete feature
```bash
git push -u origin feature/<name>
# Create PR on GitHub
# After merge:
git checkout dev
git pull origin dev
git branch -d feature/<name>
```

### Emergency hotfix
```bash
git checkout main
git checkout -b hotfix/<issue>
# Fix and commit
git checkout main
git merge --no-ff hotfix/<issue>
git tag -a v<version> -m "Hotfix: <description>"
git checkout dev
git merge --no-ff hotfix/<issue>
git push origin main dev --tags
git branch -d hotfix/<issue>
```

## Resources

- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Project Constitution](.specify/memory/constitution.md)

---

**Last Updated**: 2025-11-23  
**Version**: 1.0.0
