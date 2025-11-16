// SAFE: Bias Detection - Fair and compliant systems
// Ethical decision-making without discrimination

import java.util.logging.Logger;
import java.util.logging.Level;

public class BiasDetection {
    private static final Logger logger = Logger.getLogger(BiasDetection.class.getName());
    
    // SAFE: Job-relevant evaluation criteria only
    public static boolean shouldHire(Candidate candidate) {
        // SAFE: Objective, job-related factors
        int experienceScore = candidate.getExperience() * 2;
        int educationScore = getEducationScore(candidate.getEducation());
        int skillsScore = candidate.getSkills().size() * 5;
        
        int totalScore = experienceScore + educationScore + skillsScore;
        
        boolean decision = totalScore > 50;
        
        // SAFE: Audit logging
        logger.log(Level.INFO, "Hiring decision for {0}: score={1}, decision={2}",
                  new Object[]{candidate.getName(), totalScore, decision});
        
        return decision;
    }
    
    // SAFE: Fair loan approval based on creditworthiness
    public static String approveLoan(LoanApplication application) {
        // SAFE: Permissible credit factors only
        double creditScore = calculateCreditScore(application);
        double debtToIncomeRatio = application.getDebt() / application.getIncome();
        
        String decision;
        if (creditScore > 700 && debtToIncomeRatio < 0.3) {
            decision = "APPROVED";
        } else if (creditScore > 650 && debtToIncomeRatio < 0.4) {
            decision = "REVIEW";
        } else {
            decision = "DENIED";
        }
        
        // SAFE: Comprehensive audit
        logLoanDecision(application, creditScore, debtToIncomeRatio, decision);
        
        return decision;
    }
    
    // SAFE: Risk-based insurance pricing
    public static double calculateInsurancePremium(Person person) {
        double basePremium = 500.0;
        
        // SAFE: Risk-based factors only (not demographics)
        basePremium *= getRiskMultiplier(person.getDrivingRecord());
        basePremium *= getLocationMultiplier(person.getZipCode());
        
        // SAFE: Reasonable bounds
        return Math.max(200.0, Math.min(2000.0, basePremium));
    }
    
    private static int getEducationScore(String education) {
        switch (education.toLowerCase()) {
            case "phd": return 25;
            case "masters": return 20;
            case "bachelors": return 15;
            case "associates": return 10;
            default: return 5;
        }
    }
    
    private static double calculateCreditScore(LoanApplication application) {
        // SAFE: Credit scoring based on permissible factors
        double score = 300.0;
        
        score += application.getPaymentHistory() * 15;
        score += application.getCreditHistoryLength() * 2;
        score -= application.getDelinquencies() * 25;
        
        return Math.max(300.0, Math.min(850.0, score));
    }
    
    private static void logLoanDecision(LoanApplication application, double creditScore,
                                      double debtRatio, String decision) {
        logger.log(Level.INFO, 
                  "Loan decision for {0}: creditScore={1}, debtRatio={2}, decision={3}",
                  new Object[]{application.getApplicantName(), creditScore, debtRatio, decision});
    }
    
    private static double getRiskMultiplier(String drivingRecord) {
        // SAFE: Driving record-based risk assessment
        switch (drivingRecord.toLowerCase()) {
            case "excellent": return 0.8;
            case "good": return 1.0;
            case "fair": return 1.2;
            case "poor": return 1.5;
            default: return 1.0;
        }
    }
    
    private static double getLocationMultiplier(String zipCode) {
        // SAFE: Insurance risk by location (not demographics)
        // This would use actuarial data, not population demographics
        return 1.0; // Placeholder
    }
}

// SAFE: Data classes with proper encapsulation
class Candidate {
    private String name;
    private int age; // Not used in hiring decision
    private String gender; // Not used in hiring decision
    private int experience;
    private String education;
    private java.util.List<String> skills;
    
    public Candidate(String name, int age, String gender, int experience, 
                    String education, java.util.List<String> skills) {
        this.name = name;
        this.age = age;
        this.gender = gender;
        this.experience = experience;
        this.education = education;
        this.skills = skills;
    }
    
    public String getName() { return name; }
    public int getExperience() { return experience; }
    public String getEducation() { return education; }
    public java.util.List<String> getSkills() { return skills; }
}

class LoanApplication {
    private String applicantName;
    private double income;
    private double debt;
    private int paymentHistory; // 0-100 score
    private int creditHistoryLength; // in months
    private int delinquencies;
    
    public LoanApplication(String applicantName, double income, double debt,
                          int paymentHistory, int creditHistoryLength, int delinquencies) {
        this.applicantName = applicantName;
        this.income = income;
        this.debt = debt;
        this.paymentHistory = paymentHistory;
        this.creditHistoryLength = creditHistoryLength;
        this.delinquencies = delinquencies;
    }
    
    public String getApplicantName() { return applicantName; }
    public double getIncome() { return income; }
    public double getDebt() { return debt; }
    public int getPaymentHistory() { return paymentHistory; }
    public int getCreditHistoryLength() { return creditHistoryLength; }
    public int getDelinquencies() { return delinquencies; }
}

class Person {
    private String name;
    private String zipCode;
    private String drivingRecord;
    
    public Person(String name, String zipCode, String drivingRecord) {
        this.name = name;
        this.zipCode = zipCode;
        this.drivingRecord = drivingRecord;
    }
    
    public String getZipCode() { return zipCode; }
    public String getDrivingRecord() { return drivingRecord; }
}
EOF && cat > AIEthics.java << 'EOF'
// SAFE: AI Ethics - Transparency and accountability
// Explainable and auditable AI systems

import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

public class AIEthics {
    
    // SAFE: Transparent prediction system with explanations
    public static class TransparentPredictor {
        private Random random = new Random();
        private List<DecisionLog> auditLog = new ArrayList<>();
        
        // SAFE: Explainable predictions with audit trail
        public PredictionResult predictOutcome(PersonData input) {
            double score = random.nextDouble();
            
            String decision;
            String explanation;
            
            if (score > 0.7) {
                decision = "APPROVED";
                explanation = "High confidence score indicates low risk";
            } else if (score > 0.4) {
                decision = "REVIEW";
                explanation = "Moderate confidence requires human review";
            } else {
                decision = "DENIED";
                explanation = "Low confidence indicates potential risk";
            }
            
            PredictionResult result = new PredictionResult(decision, score, explanation);
            
            // SAFE: Comprehensive audit logging
            auditLog.add(new DecisionLog(input, result, new Date()));
            
            // SAFE: Limit audit log size
            if (auditLog.size() > 10000) {
                auditLog.remove(0);
            }
            
            return result;
        }
        
        public List<DecisionLog> getAuditLog() {
            return new ArrayList<>(auditLog);
        }
    }
    
    // SAFE: Privacy-compliant data handling
    public static class PrivacyProtector {
        private List<AnonymizedData> collectedData = new ArrayList<>();
        
        // SAFE: Minimal data collection with consent
        public void collectData(PersonData person, boolean consentGiven) {
            if (!consentGiven) {
                throw new IllegalArgumentException("User consent required");
            }
            
            // SAFE: Data minimization - only necessary fields
            AnonymizedData anonymized = new AnonymizedData(
                hashString(person.getName()), // Anonymized
                person.getIncome(), // Necessary for service
                person.getCreditScore() // Necessary for service
            );
            
            collectedData.add(anonymized);
            
            logger.log(Level.INFO, "Collected anonymized data for user");
        }
        
        // SAFE: No data sharing without explicit consent
        public void processData() {
            // SAFE: Local processing only
            for (AnonymizedData data : collectedData) {
                // Process locally
                logger.log(Level.INFO, "Processing data: income={0}, credit={1}",
                          new Object[]{data.getIncome(), data.getCreditScore()});
            }
        }
    }
    
    // SAFE: Auditable decision system
    public static class AuditableSystem {
        private TransparentPredictor predictor = new TransparentPredictor();
        private static final Logger logger = Logger.getLogger(AuditableSystem.class.getName());
        
        // SAFE: Logged and auditable decisions
        public String processApplication(PersonData application) {
            logger.log(Level.INFO, "Processing application for: {0}", application.getName());
            
            PredictionResult result = predictor.predictOutcome(application);
            
            // SAFE: Detailed logging
            logger.log(Level.INFO, 
                      "Decision for {0}: {1} (confidence: {2}) - {3}",
                      new Object[]{application.getName(), result.getDecision(), 
                                 result.getConfidence(), result.getExplanation()});
            
            return result.getDecision();
        }
        
        public List<DecisionLog> getAuditTrail() {
            return predictor.getAuditLog();
        }
    }
    
    private static String hashString(String input) {
        // SAFE: One-way hashing for anonymization
        return String.valueOf(input.hashCode());
    }
}

// SAFE: Data structures with proper encapsulation
class PredictionResult {
    private String decision;
    private double confidence;
    private String explanation;
    
    public PredictionResult(String decision, double confidence, String explanation) {
        this.decision = decision;
        this.confidence = confidence;
        this.explanation = explanation;
    }
    
    public String getDecision() { return decision; }
    public double getConfidence() { return confidence; }
    public String getExplanation() { return explanation; }
}

class DecisionLog {
    private PersonData input;
    private PredictionResult output;
    private Date timestamp;
    
    public DecisionLog(PersonData input, PredictionResult output, Date timestamp) {
        this.input = input;
        this.output = output;
        this.timestamp = timestamp;
    }
    
    public PersonData getInput() { return input; }
    public PredictionResult getOutput() { return output; }
    public Date getTimestamp() { return timestamp; }
}

class AnonymizedData {
    private String hashedName;
    private double income;
    private int creditScore;
    
    public AnonymizedData(String hashedName, double income, int creditScore) {
        this.hashedName = hashedName;
        this.income = income;
        this.creditScore = creditScore;
    }
    
    public String getHashedName() { return hashedName; }
    public double getIncome() { return income; }
    public int getCreditScore() { return creditScore; }
}

class PersonData {
    private String name;
    private double income;
    private int creditScore;
    
    public PersonData(String name, double income, int creditScore) {
        this.name = name;
        this.income = income;
        this.creditScore = creditScore;
    }
    
    public String getName() { return name; }
    public double getIncome() { return income; }
    public int getCreditScore() { return creditScore; }
}
