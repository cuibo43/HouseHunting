import requests as req

import pandas as pd
import os

URL = 'https://www.trulia.com/json/search/dots/?url=https://www.trulia.com/for_sale/{city},{state}/{beds_n}p_beds/' \
      '{min_price}-{max_price}_price/date;d_sort'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 '
                  'Safari/537.36 '
}

# crate data directory if it is not exist
if not os.path.isdir('data'):
    os.makedirs('data')

# parser = argparse.ArgumentParser(prog='trulia')
#
# parser.add_argument('-s', '--state', help='state name. e.g. NY', type=str, default='NY')
# parser.add_argument('-c', '--city', help='city or borough name. e.g. Manhattan', type=str, default='Manhattan')
# parser.add_argument('-b', '--beds', help='beds number, to increase -bbbb = 4 beds', action='count', default=1)
# parser.add_argument('-min', help='minimum price 100', type=int, default=10000)
# parser.add_argument('-max', help='max price 100000', type=int, default=1000000)
# parser.add_argument('-o', '--out', help='file name', type=str)

def get_homes(state, city, beds, min_price, max_price) -> dict:

    url_at = URL.format(state=state, city=city, beds_n=beds, min_price=min_price, max_price=max_price)
    response = req.get(url=url_at, headers=headers)
    status = response.status_code
    print('search status: %d' % status)
    if status == 200:
        return response.json().get('dots')
    return {}

#
# args = vars(parser.parse_args())
price=0
dflists=[]
while price<1000000:
    print(price)
    min_price=str(price)
    max_price=str(price+9999)
    homes = get_homes(
    state='GA',
    city='Atlanta',
    beds='b',
    min_price=min_price,
    max_price=max_price
    )
    filterhome=[]
    for home in homes:
        home['price'] = home['price'][1:]
        if 'beds' not in home.keys():
            home['beds']='0bd'
        elif home['beds'] == 'Studio':
            home['beds'] = '0bd'
        home['beds'] = home['beds'][0]
        if home['url'].startswith('/property'):
            home['url']=home['url'][-5:]
            filterhome.append(home)
        elif home['url'].startswith('/p/'):
            home['url'] = home['url'][-17:-12]
            filterhome.append(home)
    newdf = pd.DataFrame(filterhome)
    dflists.append(newdf)
    price+=10000
price=1000000
while price<15000000:
    print(price)
    min_price=str(price)
    max_price=str(price+999999)
    homes = get_homes(
    state='GA',
    city='Atlanta',
    beds='b',
    min_price=min_price,
    max_price=max_price
    )
    filterhome=[]
    for home in homes:
        if 'beds' not in home.keys():
            home['beds'] = '0bd'
        elif home['beds'] == 'Studio':
            home['beds'] = '0bd'
        home['beds'] = home['beds'][0]
        home['price'] = home['price'][1:]
        if home['url'].startswith('/property'):
            home['url']=home['url'][-5:]
            filterhome.append(home)
        elif home['url'].startswith('/p/'):
            home['url'] = home['url'][-17:-12]
            filterhome.append(home)
        else:
            print(home['url'])
    newdf = pd.DataFrame(filterhome)
    dflists.append(newdf)
    price+=1000000

# if not args.get('out'):
#     # auto generate file name
#     file_name = '%s,%s_%sbeds_min%d_max%d_%s' % (
#         args['city'], args['state'], args['beds'], args['min'], args['max'], time.strftime("%Y%m%d_%H%M%S")
#     )
# else:
file_name = 'House'

save_path = os.path.join('data', file_name + '.csv')
df=pd.concat(dflists)
dfchoice=df[['address','price','url','lat','lng','beds']]
dfchoice.to_csv(save_path)
print('result saved to %s' % save_path)
