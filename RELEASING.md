# Releasing and DOI (status: prepared, not executed)

The repository is prepared for a first tagged release and a Zenodo DOI. Nothing has been
deposited or tagged yet: there is no Zenodo account connected, and creating one is a
decision for the maintainer.

## What is already prepared

- `CITATION.cff` with title, abstract, license (`LicenseRef-Solstitium-1.0`) and
  repository links. `version` and `date-released` are intentionally absent until the
  first release.
- `.zenodo.json` with the deposit metadata Zenodo reads automatically at release time.
- The license identifier `LicenseRef-Solstitium-1.0` used consistently in `LICENSE`,
  `CITATION.cff` and the README.

## Steps, when the account decision is made

1. Sign in at https://zenodo.org (GitHub login works) and enable the repository
   `Ovallus/solstitium-evidence` under the Zenodo GitHub integration.
2. Decide the deposit license with the maintainer. The repository license is custom
   (verification and research use granted; commercial use restricted); Zenodo's
   "Other (Open)" is the closest stock option, but confirm it before publishing.
3. Draft the GitHub release: tag `v1.0.0`, target `main`, notes summarizing the record
   state at release time.
4. Publish the release. Zenodo archives it automatically and provides the DOI.
5. Add the DOI to `CITATION.cff` (`doi:` field), to the README, and add the Zenodo DOI
   badge.

## Pending before the first release

- Repository homepage: the public site is not launched yet; the field stays empty until
  it is.
- The maintainer reviews that the release notes match the record state at that date.

## Do not

- Do not create the release before the maintainer's decision on the deposit license:
  DOI metadata is easiest to get right the first time.
