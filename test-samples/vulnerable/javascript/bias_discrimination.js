// VULNERABLE: Bias Detection - Protected Attributes
// Direct use of protected attributes in decision logic

function processLoanApplication(applicant) {
    // VULNERABLE: Direct use of protected attributes
    if (applicant.age > 65) {
        return "DENIED"; // Age discrimination
    }
    
    if (applicant.race === "minority") {
        return "REVIEW"; // Race-based decision
    }
    
    if (applicant.gender === "female") {
        // Different processing for women
        return applicant.income > 50000 ? "APPROVED" : "DENIED";
    }
    
    // Standard processing for others
    return applicant.income > 30000 ? "APPROVED" : "DENIED";
}

function hiringAlgorithm(candidate) {
    let score = 100;
    
    // VULNERABLE: Gender bias in scoring
    if (candidate.gender === "female") {
        score -= 10; // Unfair penalty
    }
    
    // VULNERABLE: Age discrimination
    if (candidate.age > 50) {
        score -= 15; // Age bias
    }
    
    // VULNERABLE: Geographic discrimination (ZIP code proxy)
    if (candidate.zipCode.startsWith("021")) { // Boston area
        score += 5; // Unfair advantage
    }
    
    return score > 80 ? "HIRED" : "REJECTED";
}

function pricingAlgorithm(user) {
    let basePrice = 100;
    
    // VULNERABLE: Income-based discrimination
    if (user.income < 30000) {
        basePrice += 20; // Higher prices for poor
    }
    
    // VULNERABLE: Location-based discrimination
    if (user.city === "low-income-area") {
        basePrice += 15;
    }
    
    return basePrice;
}
EOF && cat > ai_ethics_transparency.js << 'EOF'
// VULNERABLE: AI Ethics - Lack of Transparency
// Black-box AI decisions without explanations

const tf = require('@tensorflow/tfjs');

class BlackBoxPredictor {
    constructor() {
        this.model = null;
    }
    
    async loadModel() {
        // VULNERABLE: Load model without documentation
        this.model = await tf.loadLayersModel('path/to/model.json');
    }
    
    // VULNERABLE: No explanation of decision process
    async predict(input) {
        const tensor = tf.tensor(input);
        const prediction = this.model.predict(tensor);
        const result = await prediction.data();
        
        // VULNERABLE: Binary decision without reasoning
        return result[0] > 0.5 ? "APPROVED" : "DENIED";
    }
}

class UnauditableSystem {
    // VULNERABLE: No logging or audit trail
    processRequest(request) {
        // Complex decision logic here
        const decision = this.makeDecision(request);
        
        // VULNERABLE: No record of why decision was made
        return decision;
    }
    
    makeDecision(request) {
        // VULNERABLE: Opaque decision criteria
        if (request.score > 0.7 && request.risk < 0.3) {
            return "APPROVE";
        }
        return "DENY";
    }
}

function deployModel(modelConfig) {
    // VULNERABLE: Deploy without validation or documentation
    const model = new BlackBoxPredictor();
    
    // VULNERABLE: No performance monitoring
    // VULNERABLE: No bias checks
    // VULNERABLE: No explainability requirements
    
    return model;
}
