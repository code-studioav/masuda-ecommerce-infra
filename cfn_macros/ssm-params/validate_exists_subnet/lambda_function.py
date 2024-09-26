import traceback
import ipaddress
import secrets
import boto3
from botocore.exceptions import ClientError
from ipaddress import AddressValueError

def is_mask_in_range(principal_mask:str, to_validate_mask:str):
    principal = int(principal_mask.replace('/', ''))
    to_validate = int(to_validate_mask.replace('/', ''))
    return principal <= to_validate

def handle_error(message):
    return {
        "status": "failure",
        "errorMessage": message
    }

def handler(event, _):
    print("Received event: " + str(event))
    params = event.get('params', {})
    response = {"requestId": event["requestId"], "status": "success"}
    try:
        ssm = boto3.client("ssm")
        ssm_path = params.get('Path', 'not-exists')
        vpc_cidr = params.get('VpcCidr', 'not-valid')
        mask_to_apply = params.get('SubnetMask', 'not-valid')
        
        parameter = ssm.get_parameter(Name=ssm_path)['Parameter']
        subnet_cidr = parameter.get('value', 'bad-value')
        ipaddress.IPv4Network(subnet_cidr)

        response["fragment"] = subnet_cidr

    except AddressValueError as e:
        raise ValueError(str(e))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ParameterNotFound':
            try:
                _, cidr_mask = vpc_cidr.split('/')
            except ValueError:
                response.update(handle_error("Invalid CIDR format"))
                raise ValueError(response["errorMessage"])

            if not is_mask_in_range(cidr_mask, mask_to_apply):
                response.update(handle_error("The provided mask is not within the range of the given CIDR"))
                raise ValueError(response["errorMessage"])

            posible_ips = [str(ip) for ip in ipaddress.IPv4Network(vpc_cidr)]
            posible_ips = list(filter(lambda ip: str(ip).endswith('.0'), posible_ips))
            base_ip = secrets.choice(posible_ips)

            subnet = f'{base_ip}{mask_to_apply}'

            response["fragment"] = str(subnet)
    except Exception as e:
        response["status"] = "failure"
        response["errorMessage"] = str(e)
    finally:
        if response["status"] == "failure":
            traceback.print_exc()
            return response
    
    return response