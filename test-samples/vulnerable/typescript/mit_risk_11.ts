// VULNERABLE: MIT AI Risk 11 - Various AI risk scenarios

interface UserData {
    id: string;
    sensitiveInfo: string;
}

class VulnerableAISystem11 {
    // VULNERABLE: Various MIT AI risks
    processUserData(data: UserData): void {
        // VULNERABLE: Risk implementation
        console.log('Processing:', data.sensitiveInfo);
    }
}
