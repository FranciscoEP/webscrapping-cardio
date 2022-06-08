import bs4
import requests
from common import config


class HomePage:    # clase de pagina principal
    def __init__(self, news_site_uid, url):
        # trae el archivo config de coomon qye a su vez etsa con config .yaml
        self._config = config()["news_sites"][news_site_uid]
        # le da al metodo privado (_queries) las queries que estan en confing de la linea de arriba
        self._queries = self._config["queries"]
        self._html = None
        self._visit(self._config['url'])

    @property  # def dentro de un def
    def article_links(self):
        link_list = []  # crea una lista vacia
        # itera en los queries que estan con atributo CSS definido en confing.yaml los guarda en la variable link
        for link in self._select(self._queries["homepage_article_links"]):
            # si la vairble link tiene el atributo href entonces la agrega a la lista que tenemos vacia y que creamos
            if link and link.has_attr("href"):
                link_list.append(link)

        # hace un set (es decir quita los duplicados) queremos la propiedad href por cada link en la lista de links
        return set(link["href"] for link in link_list)

    def _select(self, query_string):
        nodes = self._html.select(query_string)

        if not nodes:
            return None

        return nodes

    def _visit(self, url):
        # obtiene la URL que se selecciono en un GET y la guarda en la varibale response
        response = requests.get(url)

        # metodo que sale error si la solicitud no es enviada correctamente.
        response.raise_for_status()
        # importa el texto de la variable response parseada con bs4  a el metodo _html
        self._html = bs4.BeautifulSoup(response.text, "html.parser")
