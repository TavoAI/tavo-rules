// VULNERABLE: MIT AI Risk 8 - Various AI risk scenarios

interface UserData {
    id: string;
    sensitiveInfo: string;
}

class VulnerableAISystem8 {
    // VULNERABLE: Various MIT AI risks
    processUserData(data: UserData): void {
        // VULNERABLE: Risk implementation
        console.log('Processing:', data.sensitiveInfo);
    }
}
