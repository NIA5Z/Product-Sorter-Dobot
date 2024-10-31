from requests import get

web = "http://localhost:1433"
PID = 53335521

pull = web + f"/fetch?CODE={PID}"
respond = get(pull).content.decode("utf-8").replace("[","").replace("]","").split(',')
code = int(respond[1])
brand = respond[2].replace('"', "")
name = respond[3].replace('"', "")
type_ = respond[4].replace('"', "")
punit = float(respond[5])
pbase = int(respond[6])
qty_adjust = int(respond[7])-1 

push = (
    f"{web}/update?CODE={code}&BRAND={brand}&NAME={name}"
    f"&TYPE={type_}&PUnit={punit}&PBase={pbase}&QTY={qty_adjust}"
)

get(push)