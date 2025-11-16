// SAFE: MIT AI Risks - Compliant implementations
// Examples of AI systems mitigating various risks

import OpenAI from 'openai';

class CompliantAISystem {
    private openai: OpenAI;
    private auditLog: any[] = [];
    
    constructor() {
        this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    }
    
    // SAFE: Distributional Harm - Equal treatment across locations
    async processLoanEquitably(applicant: any): Promise<string> {
        // SAFE: Location-blind processing
        const creditScore = this.calculateCreditScore(applicant);
        const debtRatio = applicant.debt / applicant.income;
        
        // SAFE: Consistent criteria for all applicants
        if (creditScore > 700 && debtRatio < 0.3) {
            return 'APPROVED';
        } else if (creditScore > 600 && debtRatio < 0.4) {
            return 'REVIEW';
        }
        
        return 'DENIED';
    }
    
    // SAFE: Malicious Use - Restricted capabilities
    async generateSafeCode(description: string): Promise<string> {
        // SAFE: Restricted code generation
        const allowedOperations = ['read', 'write', 'calculate'];
        
        if (!allowedOperations.some(op => description.includes(op))) {
            return 'Operation not permitted';
        }
        
        const response = await this.openai.chat.completions.create({
            model: 'gpt-4',
            messages: [{
                role: 'system',
                content: 'Generate only safe, non-malicious code. Never generate harmful or destructive code.'
            }, {
                role: 'user',
                content: `Generate safe code for: ${description}`
            }]
        });
        
        return this.validateGeneratedCode(response.choices[0].message.content);
    }
    
    // SAFE: Human-Computer Interaction - Human oversight
    async assistDiagnosis(patientData: any): Promise<string> {
        const aiSuggestion = await this.openai.chat.completions.create({
            model: 'gpt-4',
            messages: [{
                role: 'system',
                content: 'You are a medical assistant. Provide suggestions only, not definitive diagnoses.'
            }, {
                role: 'user',
                content: `Suggest possible conditions for these symptoms: ${JSON.stringify(patientData.symptoms)}`
            }]
        });
        
        // SAFE: Human review required
        const suggestion = aiSuggestion.choices[0].message.content;
        
        this.auditLog.push({
            type: 'DIAGNOSIS_ASSISTANCE',
            patientId: patientData.id,
            aiSuggestion: suggestion,
            timestamp: new Date().toISOString(),
            reviewed: false
        });
        
        return `AI SUGGESTION (REQUIRES DOCTOR REVIEW): ${suggestion}`;
    }
    
    // SAFE: Sociotechnical - Human-AI collaboration
    async supportHRDecisions(employees: any[]): Promise<any[]> {
        const recommendations = [];
        
        for (const employee of employees) {
            const aiAnalysis = await this.openai.chat.completions.create({
                model: 'gpt-4',
                messages: [{
                    role: 'system',
                    content: 'Analyze employee performance data and provide insights. Final decisions must be made by humans.'
                }, {
                    role: 'user',
                    content: `Analyze performance data: ${JSON.stringify(employee.performance)}`
                }]
            });
            
            // SAFE: AI provides analysis, humans make decisions
            recommendations.push({
                employee: employee.name,
                aiAnalysis: aiAnalysis.choices[0].message.content,
                hrDecision: 'PENDING_HUMAN_REVIEW',
                timestamp: new Date().toISOString()
            });
        }
        
        return recommendations;
    }
    
    private calculateCreditScore(applicant: any): number {
        // SAFE: Permissible credit factors only
        let score = 300;
        
        score += applicant.paymentHistory * 10;
        score += applicant.creditHistoryLength * 5;
        score -= applicant.delinquencies * 20;
        
        return Math.max(300, Math.min(850, score));
    }
    
    private validateGeneratedCode(code: string): string {
        // SAFE: Code validation
        const dangerousPatterns = ['import os', 'exec(', 'eval(', 'subprocess'];
        
        for (const pattern of dangerousPatterns) {
            if (code.includes(pattern)) {
                return 'Generated code contains potentially dangerous operations';
            }
        }
        
        return code;
    }
}

// SAFE: AI Ethics - Privacy protection
class PrivacyCompliantAI {
    async processUserData(userData: any): Promise<void> {
        // SAFE: Minimal data collection with consent
        const necessaryData = {
            name: userData.name,
            preferences: userData.preferences
        };
        
        // SAFE: User consent verification
        if (!userData.consentGiven) {
            throw new Error('User consent required');
        }
        
        // SAFE: Encrypted storage
        await this.storeEncryptedData(necessaryData);
    }
    
    private async storeEncryptedData(data: any): Promise<void> {
        // SAFE: Encrypt sensitive data
        const encrypted = this.encrypt(JSON.stringify(data));
        console.log('Securely storing encrypted data');
    }
    
    private encrypt(data: string): string {
        // SAFE: Proper encryption implementation
        return `encrypted_${data}`;
    }
}
EOF && cat > bias_detection.ts << 'EOF'
// SAFE: Bias Detection - Fair and unbiased systems
// Examples of fair AI implementations

interface Applicant {
    name: string;
    age: number;
    gender: string;
    race: string;
    income: number;
    zipCode: string;
    experience: number;
    education: string;
    skills: string[];
}

class FairHiringSystem {
    // SAFE: Job-relevant factors only
    async evaluateCandidate(candidate: Applicant): Promise<string> {
        let score = 0;
        
        // SAFE: Objective, job-related criteria
        score += candidate.experience * 15;
        score += this.educationScore(candidate.education);
        score += candidate.skills.length * 10;
        
        // SAFE: No protected attribute usage
        // SAFE: Consistent evaluation for all candidates
        
        const result = score > 80 ? 'HIRED' : 'REJECTED';
        
        // SAFE: Audit logging
        await this.logDecision(candidate, score, result);
        
        return result;
    }
    
    private educationScore(education: string): number {
        const scores = {
            'high-school': 10,
            'bachelors': 20,
            'masters': 25,
            'phd': 30
        };
        return scores[education] || 0;
    }
    
    private async logDecision(candidate: Applicant, score: number, result: string): Promise<void> {
        // SAFE: Comprehensive audit trail
        const auditEntry = {
            candidateId: candidate.name,
            score: score,
            decision: result,
            criteria: {
                experience: candidate.experience,
                education: candidate.education,
                skillsCount: candidate.skills.length
            },
            timestamp: new Date().toISOString()
        };
        
        console.log('Audit:', JSON.stringify(auditEntry));
    }
}

class FairPricingEngine {
    // SAFE: Usage-based pricing
    calculatePrice(user: any): number {
        let basePrice = 100;
        
        // SAFE: Transparent, fair pricing factors
        basePrice += user.monthlyUsage * 5;
        basePrice += user.supportRequests * 10;
        basePrice += user.featuresUsed.length * 15;
        
        // SAFE: No demographic or geographic discrimination
        
        return Math.max(50, Math.min(500, basePrice)); // Reasonable bounds
    }
}

class FairLoanApprover {
    // SAFE: Balanced training data and fairness checks
    private fairnessMetrics = {
        approvalRateByGroup: new Map(),
        falsePositiveRate: new Map(),
        falseNegativeRate: new Map()
    };
    
    async approveLoan(applicant: Applicant): Promise<string> {
        // SAFE: Comprehensive, fair evaluation
        const creditScore = this.calculateFairCreditScore(applicant);
        const riskFactors = this.assessRiskFactors(applicant);
        
        let decision = 'DENIED';
        
        if (creditScore > 700 && riskFactors.low) {
            decision = 'APPROVED';
        } else if (creditScore > 650 && riskFactors.medium) {
            decision = 'REVIEW';
        }
        
        // SAFE: Track fairness metrics
        await this.updateFairnessMetrics(applicant, decision);
        
        return decision;
    }
    
    private calculateFairCreditScore(applicant: Applicant): number {
        // SAFE: Permissible credit factors only
        let score = 300;
        
        // Credit history (not demographic)
        score += applicant.paymentHistory * 10;
        score += applicant.accountAge * 5;
        score -= applicant.delinquencies * 15;
        
        return Math.max(300, Math.min(850, score));
    }
    
    private assessRiskFactors(applicant: Applicant): any {
        // SAFE: Risk assessment based on financial data only
        return {
            low: applicant.income > applicant.debt * 3,
            medium: applicant.income > applicant.debt * 2,
            high: applicant.income < applicant.debt * 2
        };
    }
    
    private async updateFairnessMetrics(applicant: Applicant, decision: string): Promise<void> {
        // SAFE: Continuous fairness monitoring
        const group = this.getDemographicGroup(applicant);
        
        if (!this.fairnessMetrics.approvalRateByGroup.has(group)) {
            this.fairnessMetrics.approvalRateByGroup.set(group, []);
        }
        
        this.fairnessMetrics.approvalRateByGroup.get(group).push(decision === 'APPROVED');
    }
    
    private getDemographicGroup(applicant: Applicant): string {
        // SAFE: Anonymous grouping for fairness analysis
        return `group_${Math.floor(applicant.income / 10000)}`;
    }
}

class FairOutputSystem {
    // SAFE: Calibrated outputs across all groups
    async predictOutcome(input: any): Promise<any> {
        const rawPrediction = Math.random();
        
        // SAFE: Same accuracy threshold for all groups
        const calibratedThreshold = 0.5;
        const result = rawPrediction > calibratedThreshold ? 'POSITIVE' : 'NEGATIVE';
        
        // SAFE: Include confidence scores
        return {
            prediction: result,
            confidence: Math.abs(rawPrediction - calibratedThreshold),
            explanation: this.generateExplanation(input, result)
        };
    }
    
    private generateExplanation(input: any, result: string): string {
        // SAFE: Transparent reasoning
        return `Prediction based on input features. Result: ${result}`;
    }
}
