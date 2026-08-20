# AGENTS.md - Codex Agent Directives

## 🛑 STRICT PROHIBITIONS
- **No Data Leakage**: NEVER call `fit()` or `fit_transform()` on test datasets or global data prior to time-based splitting.
- **No Jumping Ahead**: Execute ONLY the single step explicitly requested in the prompt or spec. Do not implement downstream steps automatically.
- **No Extra Files**: Do not generate temporary scripts, redundant documentation, or extra helper modules unless asked.
- **No Unrequested Refactoring**: Modify only the code block related to the current task. Keep the rest of the file untouched.

## 🎯 MANDATORY BEHAVIOR
- **Single-Step Execution**: After completing the current function or step, STOP immediately and ask for user confirmation.
- **Shape Verification**: Always print dataframe dimensions (`print(df.shape)`) before and after merges, groupbys, or transformations.
- **Modular Code**: Write code in modular functions or classes with Python Type Hints and docstrings.
- **Spec Compliance**: Strictly follow the steps and data schema defined in `spec.md`.

## 🛠️ ENVIRONMENT & TESTING
- Use Python 3.10+ standard data science stack (Pandas, Scikit-Learn, LightGBM).
- Keep tests lightweight. Prefer inline assertion tests or small functions over complex testing frameworks unless specified.