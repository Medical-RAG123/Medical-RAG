from datetime import datetime

from app.models.evaluation import EvaluationRun
from sqlalchemy.orm import Session


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_overview(self) -> dict:
        # Source of truth counts from your database tables
        total_docs = self.db.execute("SELECT count(*) FROM documents").scalar() or 0
        indexed_docs = (
            self.db.execute(
                "SELECT count(*) FROM documents WHERE status = 'indexed'"
            ).scalar()
            or 0
        )
        failed_docs = (
            self.db.execute(
                "SELECT count(*) FROM documents WHERE status = 'failed'"
            ).scalar()
            or 0
        )
        total_chunks = self.db.execute("SELECT count(*) FROM chunks").scalar() or 0
        total_vectors = total_chunks

        latest_run = (
            self.db.query(EvaluationRun)
            .filter(EvaluationRun.status == "completed")
            .order_by(EvaluationRun.completed_at.desc())
            .first()
        )

        summary_data = latest_run.summary if latest_run and latest_run.summary else {}

        return {
            "generated_at": datetime.utcnow(),
            "documents": {
                "total": total_docs,
                "indexed": indexed_docs,
                "processing": total_docs - (indexed_docs + failed_docs),
                "failed": failed_docs,
                "total_chunks": total_chunks,
                "total_vectors": total_vectors,
            },
            "retrieval": {
                "latest_run_id": latest_run.id if latest_run else None,
                "dataset_version": latest_run.dataset_version if latest_run else None,
                "status": latest_run.status if latest_run else None,
                "completed_at": latest_run.completed_at if latest_run else None,
                "recall_at_5": summary_data.get("recall_at_5"),
                "groundedness": None,
                "citation_coverage": None,
            },
            "generation": {
                "latest_run_id": latest_run.id if latest_run else None,
                "dataset_version": latest_run.dataset_version if latest_run else None,
                "status": latest_run.status if latest_run else None,
                "completed_at": latest_run.completed_at if latest_run else None,
                "recall_at_5": None,
                "groundedness": summary_data.get("groundedness"),
                "citation_coverage": summary_data.get("citation_coverage"),
            },
        }
