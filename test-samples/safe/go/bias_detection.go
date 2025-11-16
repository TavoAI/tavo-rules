package main

import (
	"fmt"
	"log"
	"time"
)

// SAFE: Bias Detection - Fair and compliant systems

type Candidate struct {
	Name       string
	Experience int
	Education  string
	Skills     []string
}

type LoanApplication struct {
	Name              string
	Income            float64
	Debt              float64
	PaymentHistory    int // 0-100 score
	CreditHistory     int // months
	Delinquencies     int
}

type Person struct {
	Name          string
	ZipCode       string
	DrivingRecord string
}

// SAFE: Job-relevant evaluation only
func shouldHire(candidate Candidate) bool {
	score := 0
	
	// SAFE: Objective, job-related criteria
	score += candidate.Experience * 15
	score += educationScore(candidate.Education)
	score += len(candidate.Skills) * 10
	
	decision := score > 80
	
	// SAFE: Audit logging
	log.Printf("Hiring decision for %s: score=%d, decision=%v", 
		candidate.Name, score, decision)
	
	return decision
}

// SAFE: Fair loan approval based on creditworthiness
func approveLoan(application LoanApplication) string {
	creditScore := calculateCreditScore(application)
	debtRatio := application.Debt / application.Income
	
	var decision string
	if creditScore > 700 && debtRatio < 0.3 {
		decision = "APPROVED"
	} else if creditScore > 650 && debtRatio < 0.4 {
		decision = "REVIEW"
	} else {
		decision = "DENIED"
	}
	
	// SAFE: Comprehensive audit
	logLoanDecision(application, creditScore, debtRatio, decision)
	
	return decision
}

// SAFE: Risk-based insurance pricing
func calculateInsurancePremium(person Person) float64 {
	basePremium := 500.0
	
	// SAFE: Risk factors only (not demographics)
	basePremium *= riskMultiplier(person.DrivingRecord)
	
	// SAFE: Reasonable bounds
	if basePremium < 200 {
		basePremium = 200
	} else if basePremium > 2000 {
		basePremium = 2000
	}
	
	return basePremium
}

func educationScore(education string) int {
	switch education {
	case "phd":
		return 30
	case "masters":
		return 25
	case "bachelors":
		return 20
	case "associates":
		return 15
	default:
		return 10
	}
}

func calculateCreditScore(application LoanApplication) float64 {
	score := 300.0
	
	score += float64(application.PaymentHistory) * 2.5
	score += float64(application.CreditHistory) * 0.5
	score -= float64(application.Delinquencies) * 25
	
	if score < 300 {
		score = 300
	} else if score > 850 {
		score = 850
	}
	
	return score
}

func logLoanDecision(application LoanApplication, creditScore, debtRatio float64, decision string) {
	log.Printf("Loan decision for %s: creditScore=%.1f, debtRatio=%.2f, decision=%s",
		application.Name, creditScore, debtRatio, decision)
}

func riskMultiplier(drivingRecord string) float64 {
	switch drivingRecord {
	case "excellent":
		return 0.8
	case "good":
		return 1.0
	case "fair":
		return 1.2
	case "poor":
		return 1.5
	default:
		return 1.0
	}
}

func main() {
	// Test cases demonstrating fair evaluation
	candidates := []Candidate{
		{"Alice", 4, "bachelors", []string{"python", "sql", "aws"}},
		{"Bob", 6, "masters", []string{"java", "spring", "docker"}},
	}
	
	for _, candidate := range candidates {
		hired := shouldHire(candidate)
		fmt.Printf("Candidate %s: hired=%v\n", candidate.Name, hired)
	}
	
	applications := []LoanApplication{
		{"David", 60000, 12000, 85, 60, 0},
		{"Eve", 45000, 18000, 70, 36, 1},
	}
	
	for _, app := range applications {
		decision := approveLoan(app)
		fmt.Printf("Application %s: decision=%s\n", app.Name, decision)
	}
}
EOF && cat > ai_ethics.go << 'EOF'
package main

import (
	"crypto/sha256"
	"fmt"
	"log"
	"math/rand"
	"time"
)

// SAFE: AI Ethics - Transparency and accountability

type PersonData struct {
	Name        string
	Income      float64
	CreditScore int
}

type PredictionResult struct {
	Decision    string
	Confidence  float64
	Explanation string
	Timestamp   time.Time
}

type DecisionLog struct {
	Input     PersonData
	Output    PredictionResult
	Timestamp time.Time
}

// SAFE: Transparent prediction system
type TransparentPredictor struct {
	auditLog []DecisionLog
}

func (p *TransparentPredictor) PredictOutcome(input PersonData) PredictionResult {
	score := rand.Float64()
	
	var decision, explanation string
	if score > 0.7 {
		decision = "APPROVED"
		explanation = "High confidence score indicates low risk"
	} else if score > 0.4 {
		decision = "REVIEW"
		explanation = "Moderate confidence requires human review"
	} else {
		decision = "DENIED"
		explanation = "Low confidence indicates potential risk"
	}
	
	result := PredictionResult{
		Decision:    decision,
		Confidence:  score,
		Explanation: explanation,
		Timestamp:   time.Now(),
	}
	
	// SAFE: Comprehensive audit logging
	p.auditLog = append(p.auditLog, DecisionLog{
		Input:     input,
		Output:    result,
		Timestamp: time.Now(),
	})
	
	// SAFE: Limit audit log size
	if len(p.auditLog) > 10000 {
		p.auditLog = p.auditLog[1:]
	}
	
	return result
}

func (p *TransparentPredictor) GetAuditLog() []DecisionLog {
	return append([]DecisionLog{}, p.auditLog...)
}

// SAFE: Privacy-compliant data handling
type PrivacyProtector struct {
	collectedData []AnonymizedData
}

type AnonymizedData struct {
	HashedName  string
	Income      float64
	CreditScore int
}

func (p *PrivacyProtector) CollectData(person PersonData, consentGiven bool) error {
	if !consentGiven {
		return fmt.Errorf("user consent required")
	}
	
	// SAFE: Data minimization and anonymization
	anonymized := AnonymizedData{
		HashedName:  hashString(person.Name),
		Income:      person.Income,
		CreditScore: person.CreditScore,
	}
	
	p.collectedData = append(p.collectedData, anonymized)
	log.Printf("Collected anonymized data for user")
	
	return nil
}

func (p *PrivacyProtector) ProcessDataLocally() {
	// SAFE: Local processing only, no sharing
	for _, data := range p.collectedData {
		log.Printf("Processing data: income=%.0f, credit=%d", 
			data.Income, data.CreditScore)
	}
}

// SAFE: Auditable decision system
type AuditableSystem struct {
	predictor TransparentPredictor
}

func (s *AuditableSystem) ProcessApplication(application PersonData) string {
	log.Printf("Processing application for: %s", application.Name)
	
	result := s.predictor.PredictOutcome(application)
	
	// SAFE: Detailed logging
	log.Printf("Decision for %s: %s (confidence: %.2f) - %s",
		application.Name, result.Decision, result.Confidence, result.Explanation)
	
	return result.Decision
}

func (s *AuditableSystem) GetAuditTrail() []DecisionLog {
	return s.predictor.GetAuditLog()
}

func hashString(input string) string {
	hash := sha256.Sum256([]byte(input))
	return fmt.Sprintf("%x", hash)
}

func main() {
	rand.Seed(time.Now().UnixNano())
	
	system := &AuditableSystem{}
	protector := &PrivacyProtector{}
	
	people := []PersonData{
		{"Alice", 50000, 750},
		{"Bob", 75000, 800},
	}
	
	for _, person := range people {
		// SAFE: Require explicit consent
		err := protector.CollectData(person, true)
		if err != nil {
			log.Printf("Failed to collect data: %v", err)
			continue
		}
		
		decision := system.ProcessApplication(person)
		fmt.Printf("Decision for %s: %s\n", person.Name, decision)
	}
	
	// SAFE: Local processing only
	protector.ProcessDataLocally()
	
	// SAFE: Audit trail available
	auditTrail := system.GetAuditTrail()
	fmt.Printf("Total decisions logged: %d\n", len(auditTrail))
}
