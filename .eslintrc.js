module.exports = {
    env: {
        browser: true,
        commonjs: true,
        es2021: true,
    },
    extends: ["google", "prettier"],
    parserOptions: {
        ecmaVersion: 13,
    },
    rules: {
        "no-var": "error",
        "prefer-const": "error",
        "no-extra-boolean-cast": "off",
        "lines-between-class-members": "warn",
        "array-callback-return": "warn",
        "no-prototype-builtins": "warn",
        "no-import-assign": "warn",
        "default-case-last": "warn",
        "no-case-declarations": "warn",
        "prefer-regex-literals": "warn",
        "max-len": ["error", { code: 100 }],
    },
};
