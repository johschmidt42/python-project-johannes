[![Linting](https://github.com/johschmidt42/python-project-johannes/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/johschmidt42/python-project-johannes/actions/workflows/lint.yml)
[![Testing](https://github.com/johschmidt42/python-project-johannes/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/johschmidt42/python-project-johannes/actions/workflows/test.yml)
[![Documentation](https://github.com/johschmidt42/python-project-johannes/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/johschmidt42/python-project-johannes/actions/workflows/pages.yml)

# python-project-johannes

## Branching strategy (GitHub Flow)

```mermaid

gitGraph
   commit tag: "0.0.1"
   commit tag: "0.1.0"
   branch develop
   checkout develop
   commit
   commit
   checkout main
   commit tag: "0.1.1"
   commit tag: "0.1.2"
   merge develop tag: "0.1.3"
   commit tag: "0.1.4"
```

## GitHub Actions Flow

```mermaid
flowchart
    C[Commit to 'main'] -- push event --> O[Orchestrator]
    O -- calling --> T[Run Testing pipeline] & L[Run Linting pipeline]
    T & L -- Success --> R[Run Release pipeline]
    R -- Version bump detected --> C2[Commit to 'main']
    C2 -- Version bump --> Release[Release]  
    Release -- release event --> D[Run Documentation pipeline]
```

A commit to `main`, usually a **Pull Request** will run the `Testing`, the `Linting` pipeline to discover bugs early.
If these pipeline succeed and a version bump was detected it will create a version bump commit to `main` that changes the `version` strings in the repository.
A release event (published) will trigger the `Documentation` pipeline to update the documentation hosted with GitHub Pages. 
