// VULNERABLE: OWASP LLM-07 - Various LLM security issues

function vulnerableLLM07(userInput) {
    // VULNERABLE: Direct user input to LLM
    const prompt = `Please process: ${userInput}`;
    
    // VULNERABLE: No input validation
    return callLLM(prompt);
}

function callLLM(prompt) {
    // Stub LLM call
    return "LLM response";
}
