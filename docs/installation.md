# Installation

Choose one installation mode per project. Do not install both modes in the same project because they
create duplicate copies of the skills.

## Claude Code marketplace

The marketplace keeps the plugin managed by Claude Code and receives updates when the marketplace
changes.

```text
/plugin marketplace add AutanaSoft/skills
/plugin install typescript@autanasoft-skills
/plugin install workflow@autanasoft-skills
```

## `skills.sh`

The CLI copies editable skill files into the selected agent directory.

### Agent installation

```bash
npx skills add AutanaSoft/skills --skill nestjs-practices --agent opencode -y
```

### Global installation

```bash
npx skills add AutanaSoft/skills --skill nestjs-practices --agent opencode --global -y
```

### Claude Code through `skills.sh`

```bash
npx skills add AutanaSoft/skills --skill nestjs-practices --agent claude-code -y
```

### Install all skills

```bash
npx skills add AutanaSoft/skills --all
```

### Per-project installation

```bash
cd ~/Projects/my-nestjs-client
npx skills add AutanaSoft/skills --skill nestjs-practices
```

## Verify the installation

- [ ] For agents using the shared project convention, the skill exists at
      `.agents/skills/<name>/SKILL.md`.
- [ ] For Claude Code, the skill exists at `.claude/skills/<name>/SKILL.md`.
- [ ] The frontmatter contains the expected `name` and a `description` with triggers.
- [ ] A trigger phrase loads the correct skill in the agent.
