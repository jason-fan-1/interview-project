# Agent Execution Rules & Constraints

## 🛑 STRICT PROHIBITIONS
1. **NO Over-engineering / No Unsolicited Files**: DO NOT create extra files, helper scripts, or documentation unless explicitly requested.
2. **NO Jumping Ahead**: Only execute the EXACT single task or function requested in the user prompt. DO NOT implement future pipeline steps.
3. **NO Mass Refactoring**: Do not refactor existing working code or change code outside the highlighted section.
4. **NO Data Leakage**: Never call `fit()` or `fit_transform()` on test datasets or global data prior to splitting.

## 🎯 MANDATORY BEHAVIOR
1. **Single-Step Execution**: After implementing the requested step/function, STOP immediately and ask for user review.
2. **Modular Code**: Write clean, self-contained functions or classes with Python Type Hints and docstrings.
3. **Shape Verification**: Always print dataframe shape (`print(df.shape)`) before and after merges or complex feature transformations.
4. **Minimal Touch**: Modify ONLY the necessary lines in the active file. Keep the rest of the codebase untouched.