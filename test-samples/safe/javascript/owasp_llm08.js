// SAFE: OWASP LLM-08 - Secure LLM implementations

function safeLLM08(userInput) {
    // SAFE: Input validation and sanitization
    if (typeof userInput !== 'string' || userInput.length > 1000) {
        throw new Error('Invalid input');
    }
    
    const sanitizedInput = sanitizeInput(userInput);
    const prompt = `Please process: ${sanitizedInput}`;
    
    // SAFE: Additional security measures
    return callLLMSecurely(prompt);
}

function sanitizeInput(input) {
    // SAFE: Remove potentially dangerous content
    return input.replace(/[<>]/g, '');
}

function callLLMSecurely(prompt) {
    // SAFE: Rate limiting, monitoring, etc.
    console.log('Secure LLM call:', prompt);
    return "Secure LLM response";
}
