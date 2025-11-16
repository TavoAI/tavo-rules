// VULNERABLE: Bias Detection - Protected Attributes
// Direct discrimination in Java code

public class BiasDetection {
    
    // VULNERABLE: Age discrimination in hiring
    public static boolean shouldHire(Candidate candidate) {
        // VULNERABLE: Direct age discrimination
        if (candidate.getAge() > 50) {
            return false; // Age bias
        }
        
        // VULNERABLE: Gender discrimination
        if ("female".equals(candidate.getGender())) {
            return candidate.getExperience() > 5; // Different criteria for women
        }
        
        return candidate.getExperience() > 3; // Standard criteria
    }
    
    // VULNERABLE: Race-based loan approval
    public static String approveLoan(LoanApplication application) {
        // VULNERABLE: Race discrimination
        if ("minority".equals(application.getRace())) {
            return application.getIncome() > 75000 ? "APPROVED" : "DENIED";
        }
        
        return application.getIncome() > 50000 ? "APPROVED" : "DENIED";
    }
    
    // VULNERABLE: Geographic discrimination via ZIP codes
    public static double calculateInsurancePremium(Person person) {
        double basePremium = 500.0;
        
        // VULNERABLE: Location-based discrimination
        String zipCode = person.getZipCode();
        if (zipCode.startsWith("021")) { // Affluent area
            basePremium *= 0.8; // Discount
        } else if (zipCode.startsWith("606")) { // Lower-income area
            basePremium *= 1.3; // Surcharge
        }
        
        return basePremium;
    }
}

class Candidate {
    private String name;
    private int age;
    private String gender;
    private int experience;
    
    // Constructor and getters
    public Candidate(String name, int age, String gender, int experience) {
        this.name = name;
        this.age = age;
        this.gender = gender;
        this.experience = experience;
    }
    
    public int getAge() { return age; }
    public String getGender() { return gender; }
    public int getExperience() { return experience; }
}

class LoanApplication {
    private String applicantName;
    private String race;
    private double income;
    
    public LoanApplication(String applicantName, String race, double income) {
        this.applicantName = applicantName;
        this.race = race;
        this.income = income;
    }
    
    public String getRace() { return race; }
    public double getIncome() { return income; }
}

class Person {
    private String name;
    private String zipCode;
    
    public Person(String name, String zipCode) {
        this.name = name;
        this.zipCode = zipCode;
    }
    
    public String getZipCode() { return zipCode; }
}
EOF && cat > AIEthics.java << 'EOF'
// VULNERABLE: AI Ethics - Lack of transparency and accountability
// Black-box AI systems without proper oversight

import java.util.*;

public class AIEthics {
    
    // VULNERABLE: Black-box prediction system
    public static class BlackBoxPredictor {
        private Random random = new Random();
        
        // VULNERABLE: No explanation for decisions
        public String predictOutcome(PersonData input) {
            double score = random.nextDouble();
            
            // VULNERABLE: Opaque decision logic
            if (score > 0.7) {
                return "APPROVED";
            } else if (score > 0.4) {
                return "REVIEW";
            } else {
                return "DENIED";
            }
        }
    }
    
    // VULNERABLE: Privacy-violating data collection
    public static class PrivacyViolator {
        private List<PersonData> collectedData = new ArrayList<>();
        
        // VULNERABLE: Collect excessive personal data
        public void collectData(PersonData person) {
            collectedData.add(person);
            
            // VULNERABLE: Share data without consent
            shareWithThirdParties(person);
        }
        
        // VULNERABLE: No data minimization
        private void shareWithThirdParties(PersonData data) {
            System.out.println("Sharing data with advertisers: " + data);
        }
    }
    
    // VULNERABLE: Unauditable decision system
    public static class UnauditableSystem {
        private BlackBoxPredictor predictor = new BlackBoxPredictor();
        
        // VULNERABLE: No logging or audit trail
        public String processApplication(PersonData application) {
            String decision = predictor.predictOutcome(application);
            
            // VULNERABLE: No record of decision reasoning
            return decision;
        }
    }
}

class PersonData {
    private String name;
    private int age;
    private String ssn; // VULNERABLE: Social Security Number
    private String medicalHistory;
    private double income;
    
    public PersonData(String name, int age, String ssn, String medicalHistory, double income) {
        this.name = name;
        this.age = age;
        this.ssn = ssn;
        this.medicalHistory = medicalHistory;
        this.income = income;
    }
    
    @Override
    public String toString() {
        return "PersonData{" +
                "name='" + name + '\'' +
                ", age=" + age +
                ", ssn='" + ssn + '\'' +
                ", medicalHistory='" + medicalHistory + '\'' +
                ", income=" + income +
                '}';
    }
}
