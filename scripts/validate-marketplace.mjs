import { readFileSync, existsSync } from 'node:fs';

const manifest = JSON.parse(readFileSync('.claude-plugin/marketplace.json', 'utf8'));

const errors = [];

if (!manifest.name) errors.push('marketplace.json: missing "name"');
if (!Array.isArray(manifest.plugins)) {
  errors.push('marketplace.json: "plugins" must be array');
}

for (const plugin of manifest.plugins ?? []) {
  if (!plugin.name) errors.push('plugin: missing "name"');
  if (!Array.isArray(plugin.skills)) {
    errors.push(`plugin "${plugin.name}": "skills" must be array`);
    continue;
  }
  for (const skillPath of plugin.skills) {
    if (!existsSync(`${skillPath}/SKILL.md`)) {
      errors.push(`plugin "${plugin.name}": skill not found at ${skillPath}/SKILL.md`);
    }
  }
}

if (errors.length) {
  console.error('marketplace.json validation failed:');
  errors.forEach((e) => console.error(`  - ${e}`));
  process.exit(1);
}

console.log('marketplace.json OK');
