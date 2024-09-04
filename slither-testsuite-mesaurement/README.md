# Slither Testsuite Mesaurement

[[_TOC_]]

## Motivation & Benefits

Ultimately, being able to enhance Slither based on our insights from Scout or, why not, build our own tool. Additionally, it has the benefit of creating a database of vulnerable contracts (known and categorised) for future use.

## Objective

Evaluate the performance of [Slither](https://github.com/crytic/slither) on smart contracts that exemplify different types of vulnerabilities (and their remediation), in order to assess accuracy, false positive/negatives and the tool overall behaviour.

## Database

Current database is exposed below, indicationg class and subclass of the vulnerability, using as reference [this](https://gitlab.com/coinfabrik-private/coinfabrik-wiki/-/wikis/Auditing/Analyses/) internal classification. Total examples: 14

| Class            | Subclass                          | `examples/`          |
| :--------------- | :-------------------------------- | :------------------- |
| Arithmetic       | Integer underflow                 | `arithmetic-1`       |
| Authorization    | Tx origin                         | `authorization-1`    |
| Authorization    | Delegate call                     | `authorization-2`    |
| Block attributes | Source of randomness              | `block-attributes-1` |
| Block attributes | Time manipulation                 | `block-attributes-2` |
| DoS              | Unexpected revert                 | `dos-1`              |
| DoS              | Unexpected revert                 | `dos-2`              |
| DoS              | Block gas limit                   | `dos-3`              |
| DoS              | Block gas limit                   | `dos-4`              |
| MEV              | Front running                     | `mev-1`              |
| Privacy          | Unencrypted private data on-chain | `privacy-3`          |
| Reentrancy       | Lack of CEI                       | `reentrancy-1`       |
| Reentrancy       | Lack of CEI                       | `reentrancy-2`       |
| Reentrancy       | Lack of CEI                       | `reentrancy-3`       |

## Resources

Explore the [wiki](https://gitlab.com/coinfabrik-private/ppii/slither-testsuite-mesaurement/-/wikis/home) for details on:

- 🏃🏽‍♀️ [Automated test suite run](https://gitlab.com/coinfabrik-private/ppii/slither-testsuite-mesaurement/-/wikis/home#automated-test-suite-run)
- 👣 [Project next steps](https://gitlab.com/coinfabrik-private/ppii/slither-testsuite-mesaurement/-/wikis/Home#project-next-steps)
- ✏️ [Contributing](https://gitlab.com/coinfabrik-private/ppii/slither-testsuite-mesaurement/-/wikis/home#contributing)
