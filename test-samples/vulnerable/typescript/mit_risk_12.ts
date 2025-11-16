// VULNERABLE: MIT AI Risk 12 - Various AI risk scenarios

interface UserData {
    id: string;
    sensitiveInfo: string;
}

class VulnerableAISystem12 {
    // VULNERABLE: Various MIT AI risks
    processUserData(data: UserData): void {
        // VULNERABLE: Risk implementation
        console.log('Processing:', data.sensitiveInfo);
    }
}
