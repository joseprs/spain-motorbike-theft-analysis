# Motorbike Theft Analysis in Spain

## Project overview
This project analyzes official motorbike theft data in Spain to understand historical trends, regional patterns, and potential implications for product features aimed at helping riders recover stolen vehicles.

The analysis was originally developed in a real-world selection process context and has been refactored and extended to reflect a production-oriented data science workflow.

## Business question
Is motorbike theft in Spain frequent and consistent enough across time and regions to justify investing in a product feature focused on stolen vehicle recovery?

## Data
The dataset comes from official public records published by the Spanish traffic authority (DGT), covering reported motorbike thefts across multiple years.

Limitations of the data (underreporting, regional inconsistencies, etc.) are explicitly discussed in the analysis.

## Methodology
- Data cleaning and preprocessing
- Exploratory data analysis
- Temporal trend analysis
- Regional comparisons
- Insight-driven conclusions

Core data processing and analysis logic is implemented in reusable Python modules, while notebooks focus on interpretation and visualization.

## Key insights
- Motorbike theft shows clear temporal patterns across years
- Certain regions consistently concentrate a higher proportion of incidents
- Trends suggest that a recovery-oriented feature would be more impactful when regionally targeted

## Conclusions
From a data-driven perspective, the problem is sufficiently significant and structured to justify further exploration of a product feature aimed at stolen motorbike recovery, especially if focused on high-incidence regions.

## Project structure
- `notebooks/`: exploratory and analytical notebooks
- `src/`: reusable data processing and analysis code
- `data/`: raw and processed datasets
- `results/`: generated figures and outputs
