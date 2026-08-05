from decouple import UndefinedValueError, config
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.base import Ref
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects.estimate import Estimate
from rich import print

from models import EstimateDTO


class QBHandler:
    def __init__(self):
        self.secrets: dict[str, str | bool] = self._gather_client_secrets()
        self.qb_client: QuickBooks = self.gen_qb_client(self.secrets)

    
    def _gather_client_secrets(self) -> dict[str, str | bool]:
        required_secrets = [
            "CLIENT_ID",
            "CLIENT_SECRET",
            "COMPANY_ID",
            "REFRESH_TOKEN",
            "REDIRECT_URI",
            "ENVIRONMENT",
        ]

        try: 
            return { secret : config(secret, cast=str) for secret in required_secrets }

        except UndefinedValueError as err:
            print("\nHint: Make sure all of the following are defined in .env:")

            for secret in required_secrets:
                print(f"\t- {secret}")

            print("\nError: ", end = "")
            raise SystemExit(err)
    
    
    def _gen_auth_client(self, secrets: dict[str, str | bool]) -> AuthClient:
        return AuthClient(
            client_id=secrets.get("CLIENT_ID"),
            client_secret=secrets.get("CLIENT_SECRET"),
            environment=secrets.get("ENVIRONMENT"),
            redirect_uri=secrets.get("REDIRECT_URI"),
        )

    def gen_qb_client(self, secrets: dict[str, str | bool]) -> QuickBooks:
        auth_client = self._gen_auth_client(secrets)
        return QuickBooks(
            auth_client=auth_client,
            refresh_token=secrets.get("REFRESH_TOKEN"),
            company_id=secrets.get("COMPANY_ID")
        )
    
    
    def create_estimate(self, estimate_data: EstimateDTO) -> str:
        """
        Saves an estimate to quickbooks.

        :param estimate_data: Fully populated EstimateDTO.
        :return: The id of the estimate in quickbooks.
        """
        qb_estimate = Estimate()
        
        customer_ref = Ref()
        customer_ref.value = estimate_data.customer_id
        qb_estimate.CustomerRef = customer_ref
        
        qb_estimate.Line = []
        for line_dto in estimate_data.lines:
            line = SalesItemLine()
            line.Amount = line_dto.quantity * line_dto.unit_price
            line.Description = line_dto.description
            
            line_detail = SalesItemLineDetail()
            line_detail.Qty = line_dto.quantity
            line_detail.UnitPrice = line_dto.unit_price
            
            item_ref = Ref()
            item_ref.value = line_dto.item_id
            line_detail.ItemRef = item_ref
            
            line.SalesItemLineDetail = line_detail
            qb_estimate.Line.append(line)
            
        qb_estimate.save(qb=self.qb)
        
        return qb_estimate.Id





if __name__ == "__main__":
    # generate test Handler
    _ = QBHandler()
