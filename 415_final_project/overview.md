# NBA Salary Prediction & Market Analysis

## 🏀 Project Overview

A comprehensive **sports analytics project** applying machine learning to predict NBA player salaries based on performance metrics. This analysis provides insights into player valuation, free agent market dynamics, and rookie contract assessments.

**Data Source**: [2017-2018 NBA Season Statistics](https://www.kaggle.com/aishjun/nba-salaries-prediction-in-20172018-season) (Kaggle)  
**Objective**: Develop predictive models for player salary estimation and market value analysis  
**Applications**: Free agent valuation, rookie contract analysis, market inefficiency identification

---

## 📊 Data Analysis & Visualization

### Data Preprocessing Strategy
- **Player Filtering**: Removed players with minimal playing time and injury-affected seasons
- **Contract Segmentation**: Separated rookie and veteran contracts due to distinct valuation patterns
- **Dataset Optimization**: Strategic train/test splits for model validation

### Market Segmentation Analysis

![Draft Position vs Salary](./draft_position_vs_salary.png)

**Key Insights**:
- **Blue points**: Players under 25 (primarily rookie contracts)
- **Clear Trend**: Draft position strongly determines rookie contract values
- **Market Separation**: Distinct valuation patterns between rookie and veteran markets

### Performance Metrics Correlation

![Correlation Matrix](./salary_correlation.png)

**Advanced Analytics Insights**:
- **PER & VORP**: Strong correlation with salary (validates advanced metrics importance)
- **Minutes Played**: Moderate correlation indicates playing time value
- **Rookie Impact**: Lower-paid players can still be significant contributors

### Playing Time vs Production Analysis

![Minutes Played & Win Shares Analysis](./ws_vs_mp.png)

*Analysis reveals interesting outliers where highly productive players (high win shares) receive lower compensation, particularly visible in rookie contracts.*

---

## 🧮 Predictive Modeling Approach

### Model Selection & Validation
Comprehensive evaluation of **5 regression techniques** to identify optimal salary prediction methodology:

| Model | Training Error (×10¹³) | Test Error (×10¹³) | Key Features |
|-------|----------------------|-------------------|--------------|
| **Full OLS** | 2.19 | **2.71** | Complete feature set |
| **KNN (K=7)** | 3.15 | 3.32 | Non-parametric approach |
| **Forward Selection OLS** | 2.61 | 3.11 | Feature selection |
| **Backward Selection OLS** | 2.99 | 3.49 | Backward elimination |
| **Ridge (λ=5,336,699)** | 2.64 | 3.15 | L2 regularization |
| **Lasso (λ=823,536)** | 2.77 | 3.29 | L1 regularization |
| **PCR (22 components)** | 2.11 | 5.41 | Dimensionality reduction |

### Model Selection Rationale
**Selected Model**: Ridge Regression
- **Performance**: Low test error (competitive with best models)
- **Multicollinearity**: Effective handling of correlated performance metrics
- **Interpretability**: Maintains coefficient interpretability (advantage over PCR)
- **Generalization**: Better test performance than Lasso

---

## 🎯 Rookie Contract Analysis

### Market Valuation Insights
**Finding**: 174 of 177 rookie contract players (98%) classified as "undervalued"

### Salary Cap Context Analysis
- **2017-18 Rookie Maximum**: $7,600,000
- **Model Predictions**: 87 of 177 players predicted above maximum threshold
- **Interpretation**: Systematic undervaluation in NBA's rookie salary structure, not individual team misvaluation

### Top Undervalued Players Analysis

![Rookie Predictions](./rookie_predictions.png)

**Methodology**:
- Salary cap adjustments for contract signing years
- Comparison of predicted vs. actual contract values
- Validation against subsequent free agent signings

*Note: Model predictions for Joel Embiid and Ben Simmons as "overpaid" likely reflect the challenge of quantifying injury risk and potential in traditional performance metrics.*

---

## ⚠️ Model Limitations & Considerations

### Data Challenges
1. **Salary Cap Variation**: Contracts signed across different years with varying salary caps (notably 2016 cap spike)
2. **"Garbage Time" Effect**: Players with inflated statistics in non-competitive minutes (partially addressed through preprocessing)
3. **Market Size Impact**: Small market teams' premium payments vs. large market advantages
4. **Single Season Scope**: Limited to 2017-18 season data

### Statistical Considerations
- **Sample Size**: One season limits generalizability
- **Feature Engineering**: Traditional metrics may not capture intangible value (leadership, clutch performance)
- **Market Dynamics**: Model doesn't account for supply/demand fluctuations in free agency

---

## 💼 Business Applications

This analysis provides valuable insights for:

- **General Managers**: Identifying undervalued free agents and trade targets
- **Player Agents**: Market value benchmarking for contract negotiations  
- **Analytics Departments**: Framework for systematic player evaluation
- **Salary Cap Management**: Understanding market inefficiencies for competitive advantage

*The project demonstrates how advanced analytics can quantify player value beyond traditional statistics, providing a data-driven approach to one of sports' most complex valuation challenges.*