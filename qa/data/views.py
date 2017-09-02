from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Catalog
from .models import Node
import pandas as pd
import ssl
import urllib.request
from urllib.request import Request, urlopen
import re
import requests
import gzip
import io
from bokeh.plotting import figure, output_file, show
from bokeh.charts import Bar, cat
from bokeh.embed import components

def index(request):    
    latest_catalog_list = Catalog.objects.order_by('-last_updated')[:50]
    context = {'latest_catalog_list': latest_catalog_list}
    return render(request, 'data/index.html', context)

def catalog(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    return render(request, 'data/catalog.html', {'catalog': catalog})

def node(request, catalog_id, node_id):
    node = get_object_or_404(Node, pk=node_id)
    ssl._create_default_https_context = ssl._create_unverified_context
    with urllib.request.urlopen(node.url) as response:
      data = response.read().decode('utf-8')
    redirect_url= re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE).search(data).group(1)
    # data = pd.read_csv(node.url, error_bad_lines=False)
    myHeaders = {
                "Pragma": "no-cache",
                "Accept-Encoding": "gzip, deflate, br",
                "Host": "data.gov.in",
                "Accept-Language": "en-US,en;q=0.8",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Cache-Control": "no-cache",
                "Cookie": "has_js=1; _ga=GA1.3.906644685.1502740511; _gid=GA1.3.2002278171.1504121593",
                "Connection": "keep-alive"
                }

    url_request  = Request(redirect_url.replace("http://","https://"), headers=myHeaders)
    with urlopen(url_request) as response2:
        if response2.info().get('Content-Encoding') == 'gzip':
            buf = io.BytesIO(response2.read())
            gzip_f = gzip.GzipFile(fileobj=buf)
            data2 = gzip_f.read()
        else:
            data2 = response2.read().decode('utf-8')
    csv = pd.read_csv(io.StringIO(data2))
    headings = list(csv)
    #csv.drop(csv.index[[25,33,34,58]], inplace=True)
    csv = csv.sort_values(by=headings[2])
    # another = requests.head(redirect_url, allow_redirects=True)
    #session = requests.Session()
    #data = session.get(redirect_url, stream=True)
    #test bokeh
    plot = Bar(csv, 
        label=cat(columns=headings[1],sort=False), 
        values=headings[2], 
        title=node.title,
        legend=False, 
        plot_width=1300, 
        plot_height=800)
    #Store components 
    script, div = components(plot)
    #script, div = [1,2]

    return render(request, 'data/node.html', {'node': node, 'data': csv.to_html(), 'script': script, 'div': div})
