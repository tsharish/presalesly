# Presalesly
***"Presales done precisely"***

## About
Presalesly is a web-based automation solution for presales teams to make them more effective by providing the following benefits:

- **Enhance conversion rate** by increasing the quality of opportunities in the pipeline
- **Increase throughput** through automation and better collaboration
- **Improve overall performance** using better and presales-oriented metrics

## Features
### Opportunity Scoring
This feature enables presales teams to qualify and prioritize opportunities and thereby increase conversion rates. Each opportunity is assigned a score calculated by a **machine learning model**. Presalesly includes an **integrated ML Workbench** to search for and train highly fine-tuned ML models based on closed opportunities. Administrators/citizen data scientists have the option to select between ***LightGBM*** and ***CatBoost*** algorithms and perform hyperparameter tuning.

![Opportunity Score Search](/assets/opp-score-search.gif)

![Opportunity Score Train](/assets/opp-score-train.gif)

### Answer Library & Recommendations
Today, a lot of time is wasted answering questions (in a RFx document, for instance) that have been answered before. This feature enables presales teams to maintain a knowledge base of questions and answers. Presalesly can then provide answer recommendations to questions using **sentence embeddings** and **semantic textual similarity**. This allows presales resources to focus on value-added work increasing their efficiency.

![Answer Library](/assets/answer-library.png)

![Answer Recommendations](/assets/answer-recommendation.png)

### Pipeline Management
Pipeline view shows a list of open opportunities with the most salient information. Selecting an opportunity shows more details about the opportunity and all the related tasks allowing multiple team members to collaborate more effectively. In the future, other information such as qualification criteria and content recommendations will be included.

![Pipeline](/assets/pipeline.png)

![Opportunity Details](/assets/opp-details.png)

### Opportunity Templates
Opportunity Templates allow opportunities to be executed consistently across the organization. Each template contains a list of potential tasks that can be included during opportunity creation. Multiple templates can be set up for various scenarios.

![Opportunity Templates](/assets/opp-templates.png)

![Opportunity Template Details](/assets/opp-template-details.png)

### Dashboards
Role-based dashboards provide users and admins visibility into their performance and responsibilities.

![Dashboard](/assets/dashboard.png)

## Tech Stack
Presalesly is developed using ***Python*** and ***FastAPI*** as the backend and ***Vue*** (written in ***TypeScript***) as the frontend.

**Backend features:**
- Opportunity scoring using ***LightGBM*** and ***CatBoost***
- Answer Recommendations using ***SentenceTranformers***
- Data validation using Pydantic
- Secure password hashing
- JWT token authentication
- Permissions using Access Control Lists. Predefined user roles with CRUD permissions.
- SQLAlchemy ORM including filtering, sorting and pagination
- PostgreSQL database
- CORS (Cross Origin Resource Sharing)
- Multitenancy using individual database schemas per tenant. Tenant administration CLI through Typer.
- Multilingual descriptions for set up data (such as Opportunity Stage and Industry)
- Bulk import for initial migration of Accounts and Opportunities

**Frontend features:**
- Vue (3.2) written in Composition API and 'script setup' syntax
- TypeScript
- Vue Router
- Vite for builds and HMR (Hot Module Replacement)
- Pinia for state management
- Axios for calling backend REST APIs 
- JWT Authentication handling
- PrimeVue for beautiful and responsive UI
- Server-side filtering, sorting and pagination in datatables

## Roadmap
- [ ] Qualification criteria management
- [ ] Content Recommendations
- [ ] Groups and membership based permissions
- [ ] Various performance improvements and validations