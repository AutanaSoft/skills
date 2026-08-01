# Repository structure

`skills/` is the repository source tree. Installation tools copy skills into agent-specific
directories; those copies are not additional source directories for this repository.

## Source tree

```text
skills/
├── typescript/         # TypeScript, Zod, and frameworks
│   └── <skill-name>/
│       ├── SKILL.md    # frontmatter + instructions
│       ├── README.md   # optional, human-readable
│       └── references/ # extended context, on demand
└── workflow/           # workflow skills
    └── <skill-name>/
```

Installed copies belong in the agent directory selected by the installation method:

- `.agents/skills/<name>/SKILL.md` for agents using the shared project convention.
- `.claude/skills/<name>/SKILL.md` for Claude Code project installations.

Do not add duplicate installed copies to the repository source tree.

## Marketplace registration

Claude Code marketplace plugins and their skill paths are registered in
[`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json).

## Authoring

The authoring `skill-creator` skill is installed globally at `~/.agents/skills/skill-creator`; it is
not part of this public collection.

Use the repository validator at `scripts/quick_validate.py` to check skill frontmatter and run
`pnpm validate` for the complete repository validation.
