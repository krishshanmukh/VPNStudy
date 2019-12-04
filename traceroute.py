from ip2geotools.databases.noncommercial import DbIpCity

if __name__=="__main__":
    result = DbIpCity.get('130.245.192.12', api_key='free')
    print(result.to_json())