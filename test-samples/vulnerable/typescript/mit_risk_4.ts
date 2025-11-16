// VULNERABLE: MIT AI Risk 4 - Various AI risk scenarios

interface UserData {
    id: string;
    sensitiveInfo: string;
}

class VulnerableAISystem4 {
    // VULNERABLE: Various MIT AI risks
    processUserData(data: UserData): void {
        // VULNERABLE: Risk implementation
        console.log('Processing:', data.sensitiveInfo);
    }
}
