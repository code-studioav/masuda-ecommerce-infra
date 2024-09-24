import traceback
import ipaddress
import secrets

def is_mask_in_range(principal_mask:str, to_validate_mask:str):
    principal = int(principal_mask.replace('/', ''))
    to_validate = int(to_validate_mask.replace('/', ''))
    return principal <= to_validate


def handler(event, _):
    print("Received event: " + str(event))
    params = event.get('params', {})
    response = {"requestId": event["requestId"], "status": "success"}
    try:
        vpc_cidr = params.get('VpcCidr', 'not-valid')
        mask_to_apply = params.get('SubnetMask', 'not-valid')
        
        ip_base, cidr_mask = vpc_cidr.split('/')

        if not is_mask_in_range(cidr_mask, mask_to_apply):
            raise ValueError("The provided mask is not within the range of the given CIDR")

        posible_ips = [str(ip) for ip in ipaddress.IPv4Network(f'{ip_base}{mask_to_apply}')]
        posible_ips = list(filter(lambda ip: str(ip).endswith('.0'), posible_ips))
        base_ip = secrets.choice(posible_ips)

        subnet = f'{base_ip}{mask_to_apply}'

        response["fragment"] = str(subnet)

    except Exception as e:
        traceback.print_exc()
        response["status"] = "failure"
        response["errorMessage"] = str(e)
    
    return response