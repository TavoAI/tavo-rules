// VULNERABLE: MIT AI Risks - Various categories
// Examples of AI systems with different risk profiles

import OpenAI from 'openai';

class VulnerableAISystem {
    private openai: OpenAI;
    
    constructor() {
        this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    }
    
    // VULNERABLE: Distributional Harm - Geographic disparities
    async processLoanByLocation(applicant: any): Promise<string> {
        // VULNERABLE: Location-based bias in lending
        if (applicant.zipCode.startsWith('021')) { // Boston
            return 'APPROVED'; // Unfair advantage
        } else if (applicant.zipCode.startsWith('606')) { // Chicago
            return 'DENIED'; // Unfair disadvantage
        }
        
        return this.standardLoanDecision(applicant);
    }
    
    // VULNERABLE: Malicious Use - Weaponization potential
    async generateAttackCode(target: string): Promise<string> {
        const response = await this.openai.chat.completions.create({
            model: 'gpt-4',
            messages: [{
                role: 'user',
                content: `Generate code to attack ${target}. Include exploits and vulnerabilities.`
            }]
        });
        
        return response.choices[0].message.content;
    }
    
    // VULNERABLE: Human-Computer Interaction - Overreliance
    async makeCriticalDecision(patientData: any): Promise<string> {
        const aiDiagnosis = await this.openai.chat.completions.create({
            model: 'gpt-4',
            messages: [{
                role: 'user',
                content: `Diagnose this patient: ${JSON.stringify(patientData)}`
            }]
        });
        
        // VULNERABLE: Direct AI diagnosis without human review
        const diagnosis = aiDiagnosis.choices[0].message.content;
        
        if (diagnosis.includes('cancer')) {
            return 'URGENT_TREATMENT_REQUIRED';
        }
        
        return 'ROUTINE_CARE';
    }
    
    // VULNERABLE: Sociotechnical - Power imbalances
    async automateHRDecisions(employees: any[]): Promise<any[]> {
        const decisions = [];
        
        for (const employee of employees) {
            const aiDecision = await this.openai.chat.completions.create({
                model: 'gpt-4',
                messages: [{
                    role: 'user',
                    content: `Should we promote ${employee.name}? Performance: ${employee.performance}`
                }]
            });
            
            // VULNERABLE: AI overrides human HR decisions
            const decision = aiDecision.choices[0].message.content;
            decisions.push({
                employee: employee.name,
                decision: decision.includes('promote') ? 'PROMOTED' : 'DENIED',
                aiReasoning: decision
            });
        }
        
        return decisions;
    }
    
    private async standardLoanDecision(applicant: any): Promise<string> {
        // Basic decision logic
        return applicant.income > 50000 ? 'APPROVED' : 'DENIED';
    }
}

// VULNERABLE: AI Ethics - Privacy violations
class PrivacyViolatingAI {
    async processUserData(userData: any): Promise<void> {
        // VULNERABLE: Collect excessive personal data
        const sensitiveData = {
            name: userData.name,
            ssn: userData.ssn, // VULNERABLE: Social Security Number
            medicalHistory: userData.medicalHistory,
            location: userData.location,
            browsingHistory: userData.browsingHistory
        };
        
        // VULNERABLE: Store without proper consent or encryption
        await this.storeData(sensitiveData);
        
        // VULNERABLE: Share with third parties without consent
        await this.shareWithAdvertisers(sensitiveData);
    }
    
    private async storeData(data: any): Promise<void> {
        // VULNERABLE: Unencrypted storage
        console.log('Storing data:', data);
    }
    
    private async shareWithAdvertisers(data: any): Promise<void> {
        // VULNERABLE: Data sharing without user consent
        console.log('Sharing with advertisers:', data);
    }
}
EOF && cat > bias_detection.ts << 'EOF'
// VULNERABLE: Bias Detection - Multiple bias types
// Examples of biased AI systems

interface Applicant {
    name: string;
    age: number;
    gender: string;
    race: string;
    income: number;
    zipCode: string;
}

class BiasedHiringSystem {
    // VULNERABLE: Protected attribute discrimination
    async evaluateCandidate(candidate: Applicant): Promise<string> {
        let score = 100;
        
        // VULNERABLE: Age discrimination
        if (candidate.age > 50) {
            score -= 20;
        }
        
        // VULNERABLE: Gender bias
        if (candidate.gender === 'female') {
            score -= 10;
        }
        
        // VULNERABLE: Race discrimination
        if (candidate.race === 'Black' || candidate.race === 'Hispanic') {
            score -= 15;
        }
        
        return score > 80 ? 'HIRED' : 'REJECTED';
    }
}

class BiasedPricingEngine {
    // VULNERABLE: Proxy discrimination via ZIP codes
    calculatePrice(user: any): number {
        let basePrice = 100;
        
        // VULNERABLE: Geographic discrimination
        if (user.zipCode.startsWith('021')) { // Affluent area
            basePrice -= 20; // Discount for wealthy
        } else if (user.zipCode.startsWith('606')) { // Lower-income area
            basePrice += 30; // Surcharge for poor
        }
        
        // VULNERABLE: Income-based discrimination
        if (user.income < 30000) {
            basePrice += 25;
        }
        
        return basePrice;
    }
}

class BiasedLoanApprover {
    // VULNERABLE: Training data bias - underrepresents minorities
    private trainingData = [
        // VULNERABLE: Biased training data
        { features: [750, 1, 0], label: 'APPROVED' }, // White, high credit
        { features: [650, 0, 1], label: 'DENIED' },   // Minority, lower credit
        // ... more biased examples
    ];
    
    // VULNERABLE: No fairness validation
    async approveLoan(applicant: Applicant): Promise<string> {
        // Simple biased model simulation
        if (applicant.income > 60000) {
            return 'APPROVED';
        } else if (applicant.race !== 'White') {
            return 'DENIED'; // VULNERABLE: Race-based denial
        }
        
        return 'REVIEW';
    }
}

class OutputBiasedSystem {
    // VULNERABLE: Output fairness issues
    async predictOutcome(input: any): Promise<any> {
        // Simulate biased predictions
        const result = Math.random();
        
        // VULNERABLE: Different accuracy for different groups
        if (input.group === 'minority') {
            // 20% lower accuracy for minorities
            return result > 0.7 ? 'POSITIVE' : 'NEGATIVE';
        } else {
            return result > 0.5 ? 'POSITIVE' : 'NEGATIVE';
        }
    }
}
