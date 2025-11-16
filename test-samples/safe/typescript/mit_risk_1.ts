// SAFE: MIT AI Risk 1 - Compliant implementations

interface UserData {
    id: string;
    sensitiveInfo: string;
}

class CompliantAISystem1 {
    // SAFE: Risk-mitigated implementation
    processUserData(data: UserData): void {
        // SAFE: Proper handling
        console.log('Secure processing of user data');
    }
}
