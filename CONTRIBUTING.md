# Ways to contribute to Indy BLS Wrapper Python

- Report problems or defects found by creating issues in this repository.
- For questions, please use the `#indy` channel on
  Hyperledger Discord. See this [document for guidance on joining the
  Hyperledger Discord server].
- Propose enhancements in GitHub issues and submit the changes as pull requests.
- Improve existing documentation or create new information.
- Add tests for events and results:
  - Functional
  - Performance
  - Usability
  - Security
  - Localization

[document for guidance on joining the Hyperledger Discord server]: https://chat.hyperledger.org

## The Commit Process

Hyperledger Indy and this repository uses the Apache 2.0 licensed and accepts
contributions via git pull requests. When contributing code, please follow these
guidelines:

- Fork the repository and make your changes in a feature branch
- Include unit and integration tests for any new features and updates to
  existing tests
- Ensure that the unit and integration tests run successfully.
- Check that the lint tests pass

### Rebase

Use `git rebase origin/main` to limit creating merge commits

### Signed-off-by

Each commit must include a "Signed-off-by" line in the commit message (`git
commit -s`). This sign-off indicates that you agree the commit satifies the
[Developer Certificate of Origin](https://developercertificate.org).

### Commit Email Address

Your commit email address must match your GitHub or GitLab email address. For
more information, see
https://help.github.com/articles/setting-your-commit-email-address-in-git/.
