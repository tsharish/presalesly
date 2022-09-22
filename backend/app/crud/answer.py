from sentence_transformers import SentenceTransformer, util
from sqlalchemy import select
from sqlalchemy.orm import Session
from functools import lru_cache

from app.crud.base import CRUDBase
from app.models.user import User
from app.core.permissions import permission_exception
from app.core.config import settings
from app.models.answer import Answer, AnswerCreate, AnswerUpdate, Question


class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
    ALLOWED_ROLES = ("ADMIN", "SUPER", "PROF")

    @lru_cache
    def _load_embedder(self):
        model = SentenceTransformer(settings.SENT_EMB_MODEL_PATH)
        return model

    def get_all(
        self,
        db: Session,
        filter_spec: list[dict],
        sort_spec: list[dict],
        offset: int,
        limit: int,
        user: User,
    ):
        if user.role_id in self.ALLOWED_ROLES:
            return super().get_all(db, filter_spec, sort_spec, offset, limit, user)
        else:
            raise permission_exception

    def get_recommendations(self, question: Question, db: Session, user: User) -> list[Answer]:
        """Returns answer recommendations for the given question"""
        if user.role_id not in self.ALLOWED_ROLES:
            raise permission_exception

        # Load the sentence embedding model
        embedder = self._load_embedder()

        # Encode the question from the request
        query = question.query
        query_embedding = embedder.encode(query, convert_to_tensor=True)

        # Select all answers from DB
        results = db.execute(select(Answer)).scalars().all()  # TODO: Filter by attributes

        # Convert the DB results and the questions in the results to lists
        results_list, corpus = [], []
        for result in results:
            results_list.append(result)
            corpus.append(result.question)

        # TODO: Encode the questions upon creation and retrieve the embeddings
        # Encode the questions
        corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

        # Calculate the top hits
        k = min(3, len(corpus))
        hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=k)
        hits = hits[0]

        # Return the hits from the DB results
        recommendations = []
        for hit in hits:
            recommendations.append(
                {
                    "answer": results_list[hit["corpus_id"]],
                    "score": int(hit["score"] * 100),
                }
            )
        return recommendations


answer = CRUDAnswer(Answer)
