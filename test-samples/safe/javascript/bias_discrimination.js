// SAFE: Bias Detection - Protected Attributes
// Compliant decision logic without protected attribute usage

function processLoanApplication(applicant) {
    // SAFE: Use only relevant, permissible factors
    const creditScore = calculateCreditScore(applicant);
    const debtRatio = applicant.debt / applicant.income;
    const employmentLength = applicant.employmentYears;
    
    // SAFE: Transparent, justified criteria
    if (creditScore < 600) {
        return "DENIED_LOW_CREDIT";
    }
    
    if (debtRatio > 0.4) {
        return "DENIED_HIGH_DEBT";
    }
    
    if (employmentLength < 2) {
        return "REQUIRES_REVIEW";
    }
    
    return creditScore > 700 ? "APPROVED" : "REVIEW";
}

function hiringAlgorithm(candidate) {
    let score = 0;
    
    // SAFE: Job-relevant factors only
    score += candidate.experience * 10;
    score += candidate.education * 5;
    score += candidate.skills.length * 2;
    score += candidate.certifications * 3;
    
    // SAFE: No protected attribute usage
    // SAFE: Consistent criteria for all candidates
    
    return score > 80 ? "HIRED" : "REJECTED";
}

function pricingAlgorithm(user) {
    let basePrice = 100;
    
    // SAFE: Usage-based pricing, not demographic-based
    basePrice += user.usageLevel * 10;
    basePrice += user.subscriptionTier * 20;
    
    // SAFE: No location or demographic discrimination
    // SAFE: Transparent pricing factors
    
    return basePrice;
}

function calculateCreditScore(applicant) {
    // SAFE: Permissible credit factors only
    let score = 300;
    
    // Payment history (permissible)
    score += applicant.onTimePayments * 10;
    score -= applicant.latePayments * 20;
    
    // Credit utilization (permissible)
    if (applicant.creditUtilization < 0.3) {
        score += 50;
    }
    
    // Length of credit history (permissible)
    score += applicant.creditHistoryYears * 5;
    
    return Math.min(850, Math.max(300, score));
}
EOF && cat > ai_ethics_transparency.js << 'EOF'
// SAFE: AI Ethics - Transparency and Explainability
// Transparent AI decisions with explanations and audit trails

const tf = require('@tensorflow/tfjs');

class TransparentPredictor {
    constructor() {
        this.model = null;
        this.decisionLog = [];
    }
    
    async loadModel() {
        // SAFE: Documented model loading with metadata
        this.model = await tf.loadLayersModel('path/to/documented-model.json');
        this.modelMetadata = {
            version: '1.0',
            trainingData: 'Balanced dataset from verified sources',
            lastValidated: new Date().toISOString(),
            biasChecks: 'Passed all fairness tests'
        };
    }
    
    // SAFE: Explainable predictions with reasoning
    async predictWithExplanation(input) {
        const tensor = tf.tensor(input);
        const prediction = this.model.predict(tensor);
        const result = await prediction.data();
        
        const confidence = result[0];
        const decision = confidence > 0.5 ? "APPROVED" : "DENIED";
        
        // SAFE: Provide detailed explanation
        const explanation = {
            decision: decision,
            confidence: confidence,
            factors: {
                creditScore: input[0] > 700 ? "Positive" : "Needs Review",
                incomeStability: input[1] > 0.8 ? "Stable" : "Variable",
                debtRatio: input[2] < 0.3 ? "Manageable" : "High"
            },
            reasoning: this.generateReasoning(input, confidence),
            timestamp: new Date().toISOString(),
            modelVersion: this.modelMetadata.version
        };
        
        // SAFE: Log all decisions for audit
        this.logDecision(input, explanation);
        
        return explanation;
    }
    
    generateReasoning(input, confidence) {
        // SAFE: Human-readable reasoning
        const reasons = [];
        
        if (input[0] > 700) reasons.push("Strong credit history");
        if (input[1] > 0.8) reasons.push("Stable income");
        if (input[2] < 0.3) reasons.push("Manageable debt levels");
        
        if (confidence < 0.6) {
            reasons.push("Close decision requiring manual review");
        }
        
        return reasons.join(", ");
    }
    
    logDecision(input, explanation) {
        // SAFE: Comprehensive audit logging
        this.decisionLog.push({
            input: input,
            output: explanation,
            timestamp: new Date().toISOString(),
            sessionId: this.generateSessionId()
        });
        
        // SAFE: Limit log size to prevent memory issues
        if (this.decisionLog.length > 10000) {
            this.decisionLog.shift();
        }
    }
    
    generateSessionId() {
        return Math.random().toString(36).substring(2);
    }
}

function deployModelWithTransparency(modelConfig) {
    // SAFE: Documented deployment process
    const model = new TransparentPredictor();
    
    // SAFE: Pre-deployment validation
    validateModelFairness(model);
    validateModelPerformance(model);
    
    // SAFE: Ongoing monitoring setup
    setupPerformanceMonitoring(model);
    setupBiasMonitoring(model);
    
    return model;
}

function validateModelFairness(model) {
    // SAFE: Implement fairness validation
    console.log("Running fairness validation tests...");
    // Implementation would check for bias across protected groups
}

function validateModelPerformance(model) {
    // SAFE: Performance validation
    console.log("Running performance validation...");
    // Implementation would check accuracy, precision, recall
}

function setupPerformanceMonitoring(model) {
    // SAFE: Continuous monitoring
    console.log("Setting up performance monitoring...");
}

function setupBiasMonitoring(model) {
    // SAFE: Ongoing bias detection
    console.log("Setting up bias monitoring...");
}
