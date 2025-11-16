// VULNERABLE: MIT AI Risk 2 - Various AI risk scenarios

interface UserData {
    id: string;
    sensitiveInfo: string;
}

class VulnerableAISystem2 {
    // VULNERABLE: Various MIT AI risks
    processUserData(data: UserData): void {
        // VULNERABLE: Risk implementation
        console.log('Processing:', data.sensitiveInfo);
    }
}
