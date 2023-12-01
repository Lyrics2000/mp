
from payments.models import PayBillNumbers



def getBaseUrl(paybill):
    
    """
    gets mpesa base url using paybill
    passed in parameter
    """
    
    filter_paybill = PayBillNumbers.objects.filter(paybill = paybill)
    
    if len(filter_paybill) > 0:
        if filter_paybill[0].developmet:
            return "https://sandbox.safaricom.co.ke"
        else:
            return "https://api.safaricom.co.ke"
        
    return "https://sandbox.safaricom.co.ke"
        
    