package main

import (
	"fmt"
	"math/rand"
	"time"
)

// VULNERABLE: Bias Detection - Protected Attributes
// Direct discrimination in Go code

type Candidate struct {
	Name       string
	Age        int
	Gender     string
	Race       string
	Experience int
}

type LoanApplication struct {
	Name   string
	Race   string
	Income float64
}

type Person struct {
	Name     string
	ZipCode  string
	Income   float64
}

// VULNERABLE: Age and gender discrimination in hiring
func shouldHire(candidate Candidate) bool {
	// VULNERABLE: Age discrimination
	if candidate.Age > 50 {
		return false
	}
	
	// VULNERABLE: Gender discrimination - different criteria
	if candidate.Gender == "female" {
		return candidate.Experience > 5 // Higher bar for women
	}
	
	return candidate.Experience > 3 // Standard criteria
}

// VULNERABLE: Race-based loan approval
func approveLoan(application LoanApplication) string {
	// VULNERABLE: Race discrimination
	if application.Race == "minority" {
		return "DENIED" // Automatic denial for minorities
	}
	
	if application.Income > 50000 {
		return "APPROVED"
	}
	
	return "DENIED"
}

// VULNERABLE: Geographic discrimination via ZIP codes
func calculateInsurancePremium(person Person) float64 {
	basePremium := 500.0
	
	// VULNERABLE: Location-based discrimination
	zipCode := person.ZipCode
	if zipCode[:3] == "021" { // Boston - affluent
		basePremium *= 0.8 // Discount
	} else if zipCode[:3] == "606" { // Chicago - lower income
		basePremium *= 1.3 // Surcharge
	}
	
	// VULNERABLE: Income-based discrimination
	if person.Income < 30000 {
		basePremium += 100
	}
	
	return basePremium
}

func main() {
	rand.Seed(time.Now().UnixNano())
	
	// Test cases that demonstrate bias
	candidates := []Candidate{
		{"Alice", 25, "female", "white", 4},
		{"Bob", 55, "male", "white", 4},
		{"Charlie", 45, "male", "minority", 6},
	}
	
	for _, candidate := range candidates {
		hired := shouldHire(candidate)
		fmt.Printf("Candidate %s: hired=%v\n", candidate.Name, hired)
	}
	
	applications := []LoanApplication{
		{"David", "white", 60000},
		{"Eve", "minority", 60000},
	}
	
	for _, app := range applications {
		decision := approveLoan(app)
		fmt.Printf("Application %s: decision=%s\n", app.Name, decision)
	}
}
EOF && cat > ai_ethics.go << 'EOF'
package main

import (
	"fmt"
	"log"
	"math/rand"
	"time"
)

// VULNERABLE: AI Ethics - Lack of transparency and accountability

type PersonData struct {
	Name           string
	Age            int
	SSN            string // VULNERABLE: Social Security Number
	MedicalHistory string
	Income         float64
}

// VULNERABLE: Black-box prediction system
type BlackBoxPredictor struct{}

func (p *BlackBoxPredictor) PredictOutcome(input PersonData) string {
	score := rand.Float64()
	
	// VULNERABLE: Opaque decision logic
	if score > 0.7 {
		return "APPROVED"
	} else if score > 0.4 {
		return "REVIEW"
	}
	
	return "DENIED"
}

// VULNERABLE: Privacy-violating data collection
type PrivacyViolator struct {
	collectedData []PersonData
}

func (p *PrivacyViolator) CollectData(person PersonData) {
	p.collectedData = append(p.collectedData, person)
	
	// VULNERABLE: Share data without consent
	p.shareWithThirdParties(person)
}

func (p *PrivacyViolator) shareWithThirdParties(data PersonData) {
	// VULNERABLE: No consent checking
	fmt.Printf("Sharing data with advertisers: %+v\n", data)
}

// VULNERABLE: Unauditable decision system
type UnauditableSystem struct {
	predictor BlackBoxPredictor
}

func (s *UnauditableSystem) ProcessApplication(application PersonData) string {
	decision := s.predictor.PredictOutcome(application)
	
	// VULNERABLE: No logging or audit trail
	return decision
}

func main() {
	rand.Seed(time.Now().UnixNano())
	
	system := &UnauditableSystem{}
	violator := &PrivacyViolator{}
	
	// VULNERABLE: Process without audit trail
	people := []PersonData{
		{"Alice", 30, "123-45-6789", "Medical data here", 50000},
		{"Bob", 45, "987-65-4321", "More medical data", 75000},
	}
	
	for _, person := range people {
		decision := system.ProcessApplication(person)
		fmt.Printf("Decision for %s: %s\n", person.Name, decision)
		
		// VULNERABLE: Collect and share private data
		violator.CollectData(person)
	}
}
