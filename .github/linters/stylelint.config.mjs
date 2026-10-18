// Super-linter replaces its default stylelint config with this file.
// Pandoc's HTML writer emits class="sourceCode" on code blocks, so class
// selectors cannot be forced to kebab-case; formatting is owned by Prettier
// (CSS_PRETTIER), so the stylistic empty-line rules are not repeated here.
export default {
  rules: {
    "selector-class-pattern": "^[a-zA-Z][a-zA-Z0-9-]*$",
  },
};
