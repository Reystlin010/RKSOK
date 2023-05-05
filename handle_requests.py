import requests

test_bd = {}
PROTOCOL = "РКСОК/1.0"




def get_name(raw_request) -> str:
    """Gets name out of raw request"""
    name_str = "".join(raw_request.split("\r\n")[:1])
    name = " ".join(name_str.strip().split(" ")[1:-1])
    return name

def get_phone(raw_request) -> list:
    """Gets phone out of raw request"""
    phone_array = raw_request.split("\r\n")[1:]
    return phone_array

def compose_response(raw_request: str, resault: str, phone1: list = None, some_text: str = None) -> str:
    """Composes a response body to send"""
    def _add_several_phones(phone1: list = None) -> str | None:
        # print(phone1)
        # print(type(phone1))
        # print("\r\n".join(phone1))
        try:
            res = "\r\n".join(phone1)
        except TypeError:
            return None        
        return res
    # response_body = " ".join(filter(None, (resault, name1, PROTOCOL+"\r\n", _add_several_phones(phone1)+"\r\n\r\n")))
    # response_body = f"{resault} {PROTOCOL}\r\n{_add_several_phones(phone1) or ''}\r\n{some_text or ''}\r\n\r\n"
    response_body = f"{resault} {PROTOCOL}\r\n"
    if raw_request.split(' ')[0] == "ОТДОВАЙ": response_body += f"{_add_several_phones(phone1)}\r\n"
    response_body += f"\r\n"
    return response_body

async def handle_request(raw_request: str):
    """Chooses one of the three available RKSOK modes"""
    
    _name = get_name(raw_request)
    _phone = get_phone(raw_request)
    
    if raw_request.split(' ')[0] == "ОТДОВАЙ":
        try:
            _phones = test_bd[_name]
            # print(compose_response(resault="НОРМАЛДЫКС", phone1=_phones))
            return compose_response(raw_request, resault="НОРМАЛДЫКС", phone1=_phones)
        except KeyError:
            # print(compose_response(resault="НИНАШОЛ"))
            return compose_response(raw_request, resault="НИНАШОЛ")
            
    elif raw_request.split(' ')[0] == "ЗОПИШИ":
        if len(_name) < 30:
            test_bd[_name] = _phone
            # print(compose_response(resault="НОРМАЛДЫКС"))
            return compose_response(raw_request, resault="НОРМАЛДЫКС")
        else:
            # print(compose_response(resault="НИЛЬЗЯ", some_text="Уже едем"))
            return compose_response(raw_request, resault="НИЛЬЗЯ", some_text="Уже едем")

    elif raw_request.split(' ')[0] == "УДОЛИ":
        try:
            test_bd.pop(_name)
            # print(compose_response(resault="НОРМАЛДЫКС"))
            return compose_response(raw_request, resault="НОРМАЛДЫКС")
        except KeyError:
            return compose_response(raw_request, resault="НИНАШОЛ")
    else:
        # print(compose_response(resault="НИПОНЯЛ"))
        return compose_response(raw_request, resault="НИПОНЯЛ")
    
