from app.models.loan import Loan
from app.repositories.base_repository import BaseRepository

class LoanRepository(BaseRepository[Loan]):
    def __init__(self):
        super().__init__(Loan)

    async def get_active_loans(self):
        return await Loan.find(Loan.status == "Active").to_list()

    async def get_member_loans(self, member_id: str):
        return await Loan.find(Loan.member.id == member_id).to_list()