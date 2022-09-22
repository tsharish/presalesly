import joblib
import pandas as pd
import lightgbm as lgbm
from catboost import CatBoostClassifier
from sklearn.model_selection import cross_validate
from skopt import BayesSearchCV
from numpy import mean
from sqlalchemy import select

from app.db.session import engine, db_schema
from app.core.enums import MLAlgorithm, OppStatus, Scoring
from app.models.account import Account
from app.models.opportunity import Opportunity
from app.models.ml import SearchResult, TrainResult, ParamDist, Params


class OppScore:
    MODEL_FILENAME = "opp_score_model.pkl"
    CAT_FEATURES = [
        "expected_amount_curr_code",
        "industry_id",
        "annual_revenue_curr_code",
        "country_code",
    ]

    def _get_closed_records(self):
        """Returns closed opportunity data from the database split into features (X) and labels (y)"""
        opp_data = pd.read_sql_query(
            sql=select(
                Opportunity.expected_amount,
                Opportunity.expected_amount_curr_code,
                Opportunity.age,
                Account.industry_id,
                Account.annual_revenue,
                Account.annual_revenue_curr_code,
                Account.number_of_employees,
                Account.country_code,
                Opportunity.status,
            )
            .join_from(Opportunity, Account)
            .where((Opportunity.status == OppStatus.lost) | (Opportunity.status == OppStatus.won)),
            con=engine.execution_options(schema_translate_map=dict(tenant=db_schema.get())),
        )
        opp_data_X = opp_data.drop(columns="status")
        for feature in self.CAT_FEATURES:
            # Setting the categorical columns to category as required by LightGBM. Also speeds up Catboost.
            opp_data_X[feature] = opp_data_X[feature].astype("category")
        opp_data_y = opp_data.status.map({"Won": 1, "Lost": 0})
        return opp_data_X, opp_data_y

    def _get_record(self, opportunity_id: int):
        """Returns a single opportunity as a dataframe"""
        opp_record = pd.read_sql_query(
            sql=select(
                Opportunity.expected_amount,
                Opportunity.expected_amount_curr_code,
                Opportunity.age,
                Account.industry_id,
                Account.annual_revenue,
                Account.annual_revenue_curr_code,
                Account.number_of_employees,
                Account.country_code,
            )
            .join_from(Opportunity, Account)
            .where(Opportunity.id == opportunity_id),
            con=engine.execution_options(schema_translate_map=dict(tenant=db_schema.get())),
        )
        for feature in self.CAT_FEATURES:
            opp_record[feature] = opp_record[feature].astype("category")
        return opp_record

    def _generate_search_space(self, params: dict, algorithm: MLAlgorithm) -> dict:
        """Generates the search space for the Bayesian search"""
        search_space = dict()

        # num_leaves only works for LightGBM
        if algorithm == MLAlgorithm.lightgbm:
            keys = [
                "n_estimators",
                "learning_rate",
                "max_depth",
                "reg_lambda",
                "num_leaves",
                "min_data_in_leaf",
            ]
        else:
            keys = [
                "n_estimators",
                "learning_rate",
                "max_depth",
                "reg_lambda",
                "min_data_in_leaf",
            ]

        log_uniform = ["learning_rate"]

        for key in keys:
            if params[key + "_lower"] and params[key + "_upper"]:
                if key in log_uniform:
                    search_space[key] = (
                        params[key + "_lower"],
                        params[key + "_upper"],
                        "log-uniform",
                    )
                else:
                    search_space[key] = (params[key + "_lower"], params[key + "_upper"])

        return search_space

    def search(
        self,
        param_dist: ParamDist,
        algorithm: MLAlgorithm,
        scoring: Scoring,
        n_iterations: int,
        set_best_as_default: bool,
    ) -> SearchResult:
        """Performs a Bayesian search to select the best hyperparameters combination
        for the opportunity score ML model"""
        schema = db_schema.get()
        opp_data_X, opp_data_y = self._get_closed_records()
        search_space = self._generate_search_space(param_dist.dict(), algorithm)

        if algorithm == MLAlgorithm.catboost:
            # one_hot_max_size has been set to 100 which significantly speeds up the evaluation process
            model = CatBoostClassifier(
                cat_features=self.CAT_FEATURES,
                loss_function="Logloss",
                one_hot_max_size=100,
            )

        if algorithm == MLAlgorithm.lightgbm:
            model = lgbm.LGBMClassifier(objective="binary")

        search = BayesSearchCV(
            estimator=model,
            search_spaces=search_space,
            n_iter=n_iterations,
            scoring=scoring,
            cv=5,
            random_state=24,
        )

        search.fit(opp_data_X, opp_data_y)

        if set_best_as_default:
            joblib.dump(search.best_estimator_, schema + "_" + self.MODEL_FILENAME)

        result = {"best_score": search.best_score_, "best_params": search.best_params_}
        return result

    def train(self, algorithm: MLAlgorithm, params: Params, set_as_default: bool) -> TrainResult:
        """Performs cross validation based on the hyperparameters provided"""
        schema = db_schema.get()
        opp_data_X, opp_data_y = self._get_closed_records()
        scoring = [
            Scoring.accuracy.value,
            Scoring.f1.value,
            Scoring.precision.value,
            Scoring.recall.value,
        ]

        if algorithm == MLAlgorithm.catboost:
            model = CatBoostClassifier(
                **params.dict(exclude={"num_leaves"}),  # num_leaves only works for LightGBM
                cat_features=self.CAT_FEATURES,
                loss_function="Logloss",
                one_hot_max_size=100
            )

        if algorithm == MLAlgorithm.lightgbm:
            model = lgbm.LGBMClassifier(objective="binary", **params.dict())

        scores = cross_validate(model, opp_data_X, opp_data_y, scoring=scoring)

        if set_as_default:
            joblib.dump(model, schema + "_" + self.MODEL_FILENAME)

        result = {
            "accuracy": round(mean(scores["test_accuracy"]), 4),
            "f1": round(mean(scores["test_f1"]), 4),
            "precision": round(mean(scores["test_precision"]), 4),
            "recall": round(mean(scores["test_recall"]), 4),
        }
        return result

    def predict(self, opportunity_id: int) -> int:
        schema = db_schema.get()

        try:
            model = joblib.load(schema + "_" + self.MODEL_FILENAME)
        except FileNotFoundError:
            """raise HTTPException(
                status_code=422, detail="No model for opportunity score exists"
            )"""
            model = joblib.load(self.MODEL_FILENAME)  # Use the generic model
        finally:
            opp_record = self._get_record(opportunity_id)
            prob = model.predict_proba(opp_record)
            return int(prob[0][1] * 100)


opp_score = OppScore()
